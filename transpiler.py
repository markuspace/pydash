"""
py— — Syntax Expansion for Python LLM Code

Two-step transpiler:
  1. Replace em-dash with _infer() calls → valid Python
  2. Parse with ast, extract function source, attach __schema__ attributes
"""

import sys
import tokenize
import io
import ast
import json


def step1_replace_emdash(source: str) -> str:
    """Replace NAME — "prompt" with _infer(NAME, "prompt", system="You are NAME.")."""
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    replacements = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if (
            tok.type == tokenize.NAME
            and i + 2 < len(tokens)
            and tokens[i + 1].type == tokenize.NAME
            and tokens[i + 1].string == "—"
            and tokens[i + 2].type == tokenize.STRING
        ):
            name = tok.string
            prompt = tokens[i + 2].string
            start = tok.start[1]
            end = tokens[i + 2].end[1]
            line_num = tok.start[0]
            replacements.append(
                (
                    line_num,
                    start,
                    end,
                    f'_infer({name}, {prompt}, system="You are {name}.")',
                )
            )
            i += 3
            continue
        i += 1

    lines = source.split("\n")
    for line_num, start, end, replacement in replacements:
        lines[line_num - 1] = (
            lines[line_num - 1][:start] + replacement + lines[line_num - 1][end:]
        )

    return "\n".join(lines)


def step2_attach_schemas(source: str) -> str:
    """Parse valid Python, extract function source, attach __schema__ attributes."""
    tree = ast.parse(source)
    lines = source.split("\n")
    schema_lines = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            end = node.end_lineno
            func_source = "\n".join(lines[start:end])

            # Build parameter schema from AST
            params = {}
            required = []
            for arg in node.args.args:
                if arg.arg == "self":
                    continue
                type_name = "string"
                if arg.annotation:
                    type_name = ast.unparse(arg.annotation).lower()
                    if type_name == "str":
                        type_name = "string"
                params[arg.arg] = {"type": type_name, "description": arg.arg}
                required.append(arg.arg)

            schema = {
                "type": "function",
                "function": {
                    "name": node.name,
                    "description": f"Python function source. Here is the implementation:\n\n{func_source}",
                    "parameters": {
                        "type": "object",
                        "properties": params,
                        "required": required,
                    },
                },
            }
            schema_lines.append(
                (
                    node.end_lineno,
                    f"{node.name}.__schema__ = {json.dumps(schema, indent=4)}",
                )
            )

    # Insert schema assignments after each function, not at end of file
    output_lines = source.split("\n")
    for line_num, schema_line in reversed(schema_lines):
        output_lines.insert(line_num, schema_line)

    return "\n".join(output_lines)


def runtime():
    """Generate the runtime helpers."""
    return """import ollama
import json

def _infer(agent, prompt: str, system: str = "") -> dict:
    messages = [
        {"role": "system", "content": agent.get("system", system)},
        {"role": "user", "content": prompt},
    ]
    tools = agent.get("tools", [])
    max_turns = agent.get("max_turns", 0)
    tool_map = {fn.__name__: fn for fn in tools}
    tool_schemas = [getattr(fn, "__schema__", {}) for fn in tools]
    turns = 0
    while True:
        resp = ollama.chat(
            model=agent["model"],
            messages=messages,
            tools=tool_schemas if tool_schemas else None,
        )
        turns += 1
        if max_turns and turns >= max_turns:
            return resp
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

"""


def transpile(source: str) -> str:
    """Two-step transpile: em-dash → valid Python → attach schemas."""
    step1 = step1_replace_emdash(source)
    step2 = step2_attach_schemas(step1)
    return runtime() + step2


def main():
    if len(sys.argv) < 2:
        print("Usage: python transpiler.py <file.py->", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, "r") as f:
        source = f.read()

    try:
        step1 = step1_replace_emdash(source)
        # Write intermediate file for inspection
        stem = filepath.rsplit(".", 1)[0]
        temp_path = stem + ".tmp.py"
        with open(temp_path, "w") as f:
            f.write(step1)
        print(f"  → {temp_path} (intermediate)", file=sys.stderr)

        python_code = transpile(source)
        print(python_code)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
