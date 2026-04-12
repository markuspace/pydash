import ollama

_SYSTEM_PROMPT = "You are Coder. Your role: write and compile C programs."

def _infer(prompt, max_turns=5):
    """Call the model with tool support."""
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    for _ in range(max_turns):
        resp = ollama.chat(
            model="qwen2.5-coder:7b",
            messages=messages,
            tools=_TOOLS,
        )
        msg = resp["message"]
        if "tool_calls" not in msg or not msg["tool_calls"]:
            return msg["content"]
        messages.append(msg)
        for tc in msg["tool_calls"]:
            result = _call_tool(tc["function"]["name"], tc["function"]["arguments"])
            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_call_id": tc["id"],
            })
    return "Max turns exceeded"

# Tool definitions
def write_file(path: str, content: str) -> str:
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"

_TOOL_WRITE_FILE = {'type': 'function', 'function': {'name': 'write_file', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string'}, 'content': {'type': 'string'}}, 'required': ['path', 'content']}}}

def run_command(cmd: str) -> str:
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

_TOOL_RUN_COMMAND = {'type': 'function', 'function': {'name': 'run_command', 'parameters': {'type': 'object', 'properties': {'cmd': {'type': 'string'}}, 'required': ['cmd']}}}

_TOOLS = [_TOOL_WRITE_FILE, _TOOL_RUN_COMMAND]

def _call_tool(name, arguments):
    """Execute a tool by name with the given arguments."""
    tools = {
        "write_file": write_file,
        "run_command": run_command,
    }
    if name not in tools:
        return f"Error: unknown tool '{name}'"
    try:
        return tools[name](**arguments)
    except Exception as e:
        return f"Error: {e}"




result = _infer("Write a C hello world program to hello.c, compile it with gcc, and run it. Use the tools available to you.")
print(result)


