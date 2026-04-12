import ollama
import json

def infer(agent, prompt: str) -> str:
    messages = [
        {"role": "system", "content": agent.get("system", "")},
        {"role": "user", "content": prompt},
    ]
    tools = agent.get("tools", [])
    tool_map = {fn.__name__: fn for fn in tools}
    for _ in range(5):
        resp = ollama.chat(
            model=agent.get("model", "qwen3:8b"),
            messages=messages,
            tools=tools if tools else None,
        )
        msg = resp["message"]
        if not msg.get("tool_calls"):
            return msg["content"]
        messages.append(msg)
        for tc in msg["tool_calls"]:
            name = tc["function"]["name"]
            args = tc["function"]["arguments"]
            if isinstance(args, str):
                args = json.loads(args)
            result = tool_map[name](**args)
            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_call_id": tc["id"],
            })
    return "Max turns exceeded"

def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def write_file(path: str, content: str) -> str:
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"

def run_command(cmd: str) -> str:
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def write_file(path: str, content: str) -> str:
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"

def run_command(cmd: str) -> str:
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

coder = {
    "system": "You are a C coder. You write working C programs.",
    "model": "qwen3:8b",
    "tools": [read_file, write_file, run_command]
}

output = infer(coder, "Write a hello, world program in C.")
print(output)

