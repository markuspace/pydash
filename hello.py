import ollama
import json

def infer(agent, prompt: str) -> dict:
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
            return resp
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
            })
    return resp

def write_file(path: str, content: str) -> str:
    """Write content to a file. Strips markdown code fences.

    Args:
        path: File path to write to
        content: Content to write
    """
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"

def run_command(cmd: str) -> str:
    """Run a shell command and return stdout + stderr.

    Args:
        cmd: Shell command to execute
    """
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

coder = {
    "system": "You are a C coder. You write working C programs. Use the tools available to you.",
    "model": "qwen3:8b",
    "tools": [write_file, run_command]
}

output = infer(coder, "Write a hello, world program in C.")
print(output["message"]["content"])

