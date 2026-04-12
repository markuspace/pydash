"""
Golden Path: LLM Tool Calling in Python

One way to do it. No frameworks. No alternatives.
"""

import ollama
import json
import re

# 1. Define tools as JSON schemas
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Strips markdown code fences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "File content"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return stdout + stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {"type": "string", "description": "Shell command to run"},
                },
                "required": ["cmd"],
            },
        },
    },
]


# 2. Define Python functions that implement the tools
def write_file(path: str, content: str) -> str:
    content = re.sub(r"^```.*$\n?", "", content, flags=re.MULTILINE).strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"


def run_command(cmd: str) -> str:
    import subprocess

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


# 3. Map tool names to functions
TOOL_FUNCTIONS = {
    "write_file": write_file,
    "run_command": run_command,
}


# 4. The infer loop — one way to do it
def infer(system_prompt: str, user_prompt: str, max_turns: int = 5) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    for _ in range(max_turns):
        resp = ollama.chat(
            model="qwen3:8b",
            messages=messages,
            tools=TOOLS,
        )
        msg = resp["message"]

        # No tool calls — we're done
        if "tool_calls" not in msg or not msg["tool_calls"]:
            return msg["content"]

        # Execute each tool call
        messages.append(msg)
        for tc in msg["tool_calls"]:
            name = tc["function"]["name"]
            args = tc["function"]["arguments"]
            if isinstance(args, str):
                args = json.loads(args)
            result = TOOL_FUNCTIONS[name](**args)
            messages.append(
                {
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tc["id"],
                }
            )

    return "Max turns exceeded"


# 5. Use it
SYSTEM_PROMPT = (
    "You are Coder. You write and compiles C programs. Use the tools available to you."
)
USER_PROMPT = (
    "Write a C hello world program to hello.c, compile it with gcc, and run it."
)

result = infer(SYSTEM_PROMPT, USER_PROMPT)
print(result)
