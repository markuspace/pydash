import ollama

_SYSTEM_PROMPT = "You are Helper. Your role: assist with file operations."

def _infer(prompt, max_turns=5):
    """Call the model with tool support."""
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    for _ in range(max_turns):
        resp = ollama.chat(
            model="phi3:mini",
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
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

_TOOL_READ_FILE = {'type': 'function', 'function': {'name': 'read_file', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path']}}}

_TOOLS = [_TOOL_READ_FILE]

def _call_tool(name, arguments):
    """Execute a tool by name with the given arguments."""
    tools = {
        "read_file": read_file,
    }
    if name not in tools:
        return f"Error: unknown tool '{name}'"
    try:
        return tools[name](**arguments)
    except Exception as e:
        return f"Error: {e}"



content = _infer("Summarize the contents of the file.")
print(content)


