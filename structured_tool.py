"""
Golden Path: Structured tool output.
One function. No schema dict. Type hints ARE the schema.
"""

import ollama


def greet(message: str) -> str:
    return message


resp = ollama.chat(
    model="qwen3:8b",
    messages=[
        {"role": "user", "content": "Call the greet tool with message='Hello, World!'"}
    ],
    tools=[greet],
)

tool_call = resp["message"]["tool_calls"][0]
result = greet(**tool_call.function.arguments)
print(result)
