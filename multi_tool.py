"""
Golden Path: Multiple tools with structured output.
Write a C program, compile it, run it.
"""

import ollama
import subprocess


def write_file(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"


def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def run_command(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


TOOLS = [write_file, read_file, run_command]

SYSTEM_PROMPT = (
    "You are a C programmer. You have three tools available: "
    "write_file(path, content), read_file(path), and run_command(cmd). "
    "Use them to write a C hello world program to hello.c, "
    "compile it with gcc, and run it. "
    "Call each tool one at a time. Wait for the result before calling the next."
)

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for turn in range(10):
    resp = ollama.chat(
        model="qwen3:8b",
        messages=messages,
        tools=TOOLS,
    )

    msg = resp["message"]

    # No tool calls — we're done
    if not msg.get("tool_calls"):
        print(f"Final response: {msg.get('content')}")
        break

    # Execute each tool call
    for tc in msg["tool_calls"]:
        name = tc.function.name
        args = tc.function.arguments
        print(f"  Calling {name}({args})")

        tool_fn = {t.__name__: t for t in TOOLS}[name]
        result = tool_fn(**args)
        print(f"  Result: {result}")

        messages.append(msg)
        messages.append(
            {
                "role": "tool",
                "content": str(result),
            }
        )
