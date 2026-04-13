import ollama
import json

def _infer(agent, prompt: str, system: str = "") -> dict:
    messages = [
        {"role": "system", "content": agent.get("system", system)},
        {"role": "user", "content": prompt},
    ]
    tools = agent.get("tools", [])
    max_turns = agent.get("max_turns", 0)
    tool_map = {fn.__name__: fn for fn in tools}
    tool_schemas = [getattr(fn, "__schema__", {}) for fn in tools]
    turns = 0
    while True:
        resp = ollama.chat(
            model=agent["model"],
            messages=messages,
            tools=tool_schemas if tool_schemas else None,
        )
        turns += 1
        if max_turns and turns >= max_turns:
            return resp
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

def write_file(path: str, content: str) -> str:
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"
write_file.__schema__ = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Python function source. Here is the implementation:\n\ndef write_file(path: str, content: str) -> str:\n    import re\n    content = re.sub(r'^```.*$\\n?', '', content, flags=re.MULTILINE)\n    content = content.strip()\n    with open(path, \"w\") as f:\n        f.write(content)\n    return f\"wrote {path}\"",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path"
                },
                "content": {
                    "type": "string",
                    "description": "content"
                }
            },
            "required": [
                "path",
                "content"
            ]
        }
    }
}

def run_command(cmd: str) -> str:
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
run_command.__schema__ = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Python function source. Here is the implementation:\n\ndef run_command(cmd: str) -> str:\n    import subprocess\n    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)\n    return result.stdout + result.stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "cmd": {
                    "type": "string",
                    "description": "cmd"
                }
            },
            "required": [
                "cmd"
            ]
        }
    }
}

coder = {
    "model": "qwen3:8b",
    "tools": [write_file, run_command]
}

response = _infer(coder, "Write a hello, world program in C, save it to hello.c, compile it with gcc, and run it.", system="You are coder.")
print(response["message"]["content"])

