# PyL

A syntax preprocessor for Python. Expands LLM inference boilerplate into working Python. Passes everything else through unchanged.

## Hello World

**hello.pyl** — 20 lines. A coder agent that writes, compiles, and runs C code:

```pyl
def write_file(path: str, content: str) -> str:
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"

def run_command(cmd: str) -> str:
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

coder = {
    "model": "qwen3:8b",
    "tools": [write_file, run_command]
}

response = coder — "Write a hello, world program in C, save it to hello.c, compile it with gcc, and run it."
print(response["message"]["content"])
```

**Run it:**

```bash
python transpiler.py hello.pyl > hello.py
python hello.py
```

**Output:**

```
  → calling write_file({'path': 'hello.c', 'content': '#include <stdio.h>\n...'})
  ← wrote hello.c
  → calling run_command({'cmd': 'gcc hello.c -o hello'})
  ←
  → calling run_command({'cmd': './hello'})
  ← hello, world

The "hello, world" program has been successfully executed!
```

## How It Works

Two-step transpile:

1. Replace `NAME — "prompt"` with `_infer(NAME, "prompt", system="You are NAME.")`
2. Parse the valid Python with `ast`, extract function source, attach `__schema__` attributes

The generated `.py` file is fully inspectable. An intermediate `.tmp.py` is also written after step 1.

## What It Does

| What you write | What it becomes |
|---|---|
| `coder` | System prompt: `"You are coder."` |
| `—` | `_infer()` — the full tool-calling loop |
| `"prompt"` | User message |

The preprocessor also generates tool schemas from function signatures and attaches them as `__schema__` attributes. The full function source becomes the tool description.

## Design Decisions

- No system prompts needed — the agent's name is the prompt  (`coder` → `"You are coder."`)
- No tool prompts needed — the entire function source is used as the tool description
- Only `—` is new syntax — everything else is Python
- No custom runtime — Python is the runtime
- Generated code is fully inspectable

## Current State

This is an early-stage conceptual project. It works for the hello world example, but barely does anything beyond that:

- Only the em-dash (`—`) syntax is implemented
- Tied to Ollama — no other providers
- No streaming, no error handling, no retries
- No memory, no context management, no multi-agent
- Tool schemas are auto-generated from function source only

We're actively building it out. This is a proof of concept, not a production tool.


## Quick Start

```bash
pip install ollama
ollama pull qwen3:8b

python transpiler.py hello.pyl > hello.py
python hello.py
```

## License

MIT
