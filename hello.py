import ollama
import json

def _infer(agent, prompt: str, system: str = "") -> dict:
    messages = [
        {"role": "system", "content": agent.get("system", system)},
        {"role": "user", "content": prompt},
    ]
    tools = agent.get("tools", [])
    tool_map = {fn.__name__: fn for fn in tools}
    tool_schemas = [getattr(fn, "__schema__", {}) for fn in tools]
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
        "description": "def write_file(path: str, content: str) -> str:\n    import re\n    content = re.sub(r'^```.*$\\n?', '', content, flags=re.MULTILINE)\n    content = content.strip()\n    with open(path, \"w\") as f:\n        f.write(content)\n    return f\"wrote {path}\"",
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
        "description": "def run_command(cmd: str) -> str:\n    import subprocess\n    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)\n    return result.stdout + result.stderr",
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

