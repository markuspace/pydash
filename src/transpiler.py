"""
PyL — Syntax Expansion for Python LLM Code

Pure tokenizer-based transpiler. No regex. No line-by-line parsing.
Expands `agent NAME { prompt: "X" }` and `NAME — "prompt"` calls.
"""

import sys
import tokenize
import io


class GoldenPathError(Exception):
    """Compiler error — code violates the golden path."""

    pass


def transpile(source: str) -> str:
    """Tokenize source, expand PyL syntax, return Python."""
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    output = []
    agents = set()
    i = 0

    while i < len(tokens):
        tok = tokens[i]

        # agent NAME { prompt: "X" } → NAME = Agent(prompt="X")
        if tok.type == tokenize.NAME and tok.string == "agent":
            i, text, name = _expand_agent(tokens, i)
            agents.add(name)
            output.append(text)
            continue

        # agent — "prompt" or agent -- "prompt" → agent("prompt")
        if tok.type == tokenize.NAME and tok.string in agents and i + 2 < len(tokens):
            # em-dash: agent — "prompt"
            if (
                tokens[i + 1].type == tokenize.NAME
                and tokens[i + 1].string == "—"
                and tokens[i + 2].type == tokenize.STRING
            ):
                i, text = _expand_call(tokens, i, tok.string)
                output.append(text)
                continue
            # double-dash: agent -- "prompt"
            if (
                tokens[i + 1].type == tokenize.OP
                and tokens[i + 1].string == "-"
                and i + 3 < len(tokens)
                and tokens[i + 2].type == tokenize.OP
                and tokens[i + 2].string == "-"
                and tokens[i + 3].type == tokenize.STRING
            ):
                i, text = _expand_call_ddash(tokens, i, tok.string)
                output.append(text)
                continue

        # Everything else — pass through
        output.append(_token_text(tok))
        i += 1

    return runtime() + "".join(output)


def _expand_call(tokens, i, agent_name):
    """Expand: agent — "prompt" → agent("prompt")"""
    prompt = tokens[i + 2].string
    return i + 3, f"{agent_name}({prompt})"


def _expand_call_ddash(tokens, i, agent_name):
    """Expand: agent -- "prompt" → agent("prompt")"""
    prompt = tokens[i + 3].string
    return i + 4, f"{agent_name}({prompt})"


def runtime():
    """Generate the runtime helpers."""
    return """import ollama

class Agent:
    def __init__(self, prompt: str = ""):
        self._prompt = prompt

    def __call__(self, prompt: str) -> str:
        resp = ollama.chat(
            model="qwen3:8b",
            messages=[
                {"role": "system", "content": self._prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return resp["message"]["content"]

"""


def _token_text(tok):
    """Get the text representation of a token."""
    if tok.type == tokenize.ENCODING:
        return ""
    return tok.string


def _expand_agent(tokens, i):
    """Expand: agent NAME { prompt: "X" } → NAME = Agent(prompt="X")"""
    agent_tok = tokens[i]
    i += 1

    if i >= len(tokens) or tokens[i].type != tokenize.NAME:
        raise GoldenPathError(
            f"Line {agent_tok.start[0]}: Expected agent name after 'agent'."
        )
    name = tokens[i].string
    i += 1

    if i >= len(tokens) or tokens[i].string != "{":
        raise GoldenPathError(
            f"Line {agent_tok.start[0]}: Expected '{{' after agent name."
        )
    i += 1

    body = {}
    while i < len(tokens) and tokens[i].string != "}":
        tok = tokens[i]
        if tok.type == tokenize.NAME and tok.string == "prompt":
            key = tok.string
            i += 1
            if i < len(tokens) and tokens[i].string == ":":
                i += 1
            if i < len(tokens) and tokens[i].type == tokenize.STRING:
                body[key] = tokens[i].string
                i += 1
        else:
            i += 1

    if i >= len(tokens):
        raise GoldenPathError(f"Line {agent_tok.start[0]}: Unclosed agent block.")
    i += 1

    prompt_val = body.get("prompt", '""')
    text = f"{name} = Agent(prompt={prompt_val})\n"

    return i, text, name


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
