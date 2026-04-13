# py—

A syntax preprocessor for Python. One character — `—` — absorbs the boilerplate of LLM inference.

## The Problem

LLM inference requires:
- HTTP client setup
- Message construction (system + user)
- Tool schema registration
- JSON parsing
- Tool-calling loop
- Result handling

Write `coder — "prompt"`. The preprocessor expands it into all of the above. You write 20 lines. It becomes 103. The surface area is yours to reason in, not manage.

## How It Works

Two-step transpile:

1. `NAME — "prompt"` → `_infer(NAME, "prompt", system="You are NAME.")`
2. AST parse → extract function source → attach `__schema__` attributes

The generated `.py` is fully inspectable. An intermediate `.tmp.py` is also written.

## Hello World

Flow: `hello.py—` → `transpiler` → `hello.py` → output

### 1. hello.py— (20 lines)

```python
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

### 2. hello.py (103 lines)

```python
import ollama
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

def write_file(path: str, content: str) -> str:
    import re
    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)
    content = content.strip()
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"
write_file.__schema__ = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Python function source. Here is the implementation:\n\ndef write_file(path: str, content: str) -> str:\n    import re\n    content = re.sub(r'^```.*$\n?', '', content, flags=re.MULTILINE)\n    content = content.strip()\n    with open(path, \"w\") as f:\n        f.write(content)\n    return f\"wrote {path}\"",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "path"},
                "content": {"type": "string", "description": "content"}
            },
            "required": ["path", "content"]
        }
    }
}

def run_command(cmd: str) -> str:
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
run_command.__schema__ = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Python function source. Here is the implementation:\n\ndef run_command(cmd: str) -> str:\n    import subprocess\n    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)\n    return result.stdout + result.stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "cmd": {"type": "string", "description": "cmd"}
            },
            "required": ["cmd"]
        }
    }
}

coder = {
    "model": "qwen3:8b",
    "tools": [write_file, run_command]
}

response = _infer(coder, "Write a hello, world program in C, save it to hello.c, compile it with gcc, and run it.", system="You are coder.")
print(response["message"]["content"])
```

### 3. Run it

```bash
python transpiler.py hello.py— > hello.py
python hello.py
```

### 4. Output

```
  → calling write_file({'path': 'hello.c', 'content': '#include <stdio.h>\n...'})
  ← wrote hello.c
  → calling run_command({'cmd': 'gcc hello.c -o hello'})
  ←
  → calling run_command({'cmd': './hello'})
  ← hello, world

The "hello, world" program has been successfully executed!
```

## Why the em-dash

It's not valid Python (tokenizer sees it as a NAME), so it's a clean extension. AI writing is notorious for it — the meme, the signature. We gave it a job. One character, minimal surface area. Reads naturally: `coder — "prompt"` = "invoke coder with prompt." Arrow semantics inverted from `->`. Absurd enough to be right.

## Design Decisions

- Variable name is the system prompt (`coder` → `"You are coder."`)
- Function source is the tool description
- Only `—` is new syntax — everything else is Python
- No custom runtime — Python is the runtime
- Generated code is fully inspectable
- Tied to Ollama — other providers need changes to `_infer`

## Current State

Early-stage. Works for hello world. Not much beyond:

- Only em-dash syntax
- No streaming, no retries, no error handling
- No memory, no context management, no multi-agent

## Quick Start

```bash
pip install ollama
ollama pull qwen3:8b

python transpiler.py hello.py— > hello.py
python hello.py
```

## License

MIT