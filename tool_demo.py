import ollama

_SYSTEM_PROMPT = "You are Helper. Your role: assist with file operations."

# Tool definitions
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

_TOOL_READ_FILE = {'type': 'function', 'function': {'name': 'read_file', 'parameters': {'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path']}}}



content = read_file("README.md")
print(content[:200])


