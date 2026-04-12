"""
PyL — Syntax Expansion for Python LLM Code

Pure tokenizer-based transpiler. The source is already valid Python.
The only new syntax is the em-dash: NAME — "prompt" → infer(NAME, "prompt")
Everything else passes through unchanged.
"""

import sys
import tokenize
import io


class GoldenPathError(Exception):
    """Compiler error — code violates the golden path."""

    pass


def transpile(source: str) -> str:
    """Find em-dash tokens, expand to infer() calls, return Python."""
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))

    # Find all em-dash positions and collect replacements
    replacements = []  # (start_pos, end_pos, replacement_text)
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        # Look for NAME — "STRING"
        if (
            tok.type == tokenize.NAME
            and i + 2 < len(tokens)
            and tokens[i + 1].type == tokenize.NAME
            and tokens[i + 1].string == "—"
            and tokens[i + 2].type == tokenize.STRING
        ):
            name = tok.string
            prompt = tokens[i + 2].string
            # Use original source positions to preserve whitespace
            start = tok.start[1]  # column of NAME
            end = tokens[i + 2].end[1]  # column after STRING
            line_num = tok.start[0]
            replacements.append((line_num, start, end, f"infer({name}, {prompt})"))
            i += 3
            continue
        i += 1

    # Apply replacements line by line
    lines = source.split("\n")
    for line_num, start, end, replacement in replacements:
        lines[line_num - 1] = (
            lines[line_num - 1][:start] + replacement + lines[line_num - 1][end:]
        )

    return runtime() + "\n".join(lines)


def runtime():
    """Generate the runtime helpers."""
    return """import ollama
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

"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python transpiler.py <file.pyl>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, "r") as f:
        source = f.read()

    try:
        python_code = transpile(source)
        print(python_code)
    except GoldenPathError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
