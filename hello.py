import ollama
import json
import inspect

def _build_tool_schema(fn):
    sig = inspect.signature(fn)
    params = {}
    required = []
    for name, param in sig.parameters.items():
        params[name] = {
            "type": "string" if param.annotation in (str, inspect.Parameter.empty) else str(param.annotation).lower().replace("<class '", "").replace("'>", ""),
            "description": name,
        }
        if param.default == inspect.Parameter.empty:
            required.append(name)
    return {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": f"{fn.__name__} with {', '.join(sig.parameters.keys())}",
            "parameters": {
                "type": "object",
                "properties": params,
                "required": required,
            },
        },
    }

def infer(agent, prompt: str) -> dict:
    messages = [
        {"role": "system", "content": agent.get("system", "")},
        {"role": "user", "content": prompt},
    ]
    tools = agent.get("tools", [])
    tool_map = {fn.__name__: fn for fn in tools}
    tool_schemas = [_build_tool_schema(fn) for fn in tools]
    for _ in range(5):
        resp = ollama.chat(
            model=agent.get("model", "qwen3:8b"),
            messages=messages,
            tools=tool_schemas if tool_schemas else None,
        )
        msg = resp["message"]
        if not msg.get("tool_calls"):
            return resp
        messages.append(msg)
        for tc in msg["tool_calls"]:
            name = tc["function"]["name"]
            args = tc["function"]["arguments"]
            print(f"  → calling {name}({args})")
            if isinstance(args, str):
                args = json.loads(args)
            result = tool_map[name](**args)
            print(f"  ← {result}")
            messages.append({
                "role": "tool",
                "content": str(result),
            })
    return resp

def write_file(path: str, content: str) -> str:
    """write_file with path, content"""
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"

def run_command(cmd: str) -> str:
    """run_command with cmd"""
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

coder = {
    "system": "You are a C coder. You write working C programs. Use the tools available to you.",
    "model": "qwen3:8b",
    "tools": [write_file, run_command]
}

output = infer(coder, "Write a hello, world program in C, save it to hello.c, compile it with gcc, and run it.")
print(output["message"]["content"])

