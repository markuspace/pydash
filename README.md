# PyL — Syntax Preprocessor for Python LLM Code

PyL adds two keywords to Python: `agent` and `infer`. It expands them into working Python and passes everything else through unchanged.

## The Problem

AI coding assistants fail not because they can't write code, but because they drown in surface area. The gap between a single-function benchmark (~90% success) and a real-world multi-file task (~5% success) is 18x — and the only difference is how many things the LLM has to coordinate: imports, dependencies, build configs, tool schemas, prompt strings, file paths.

PyL compresses LLM boilerplate into minimal syntax. The intent is the code.

## Hello World

```pyl
agent Hello {
    name: "Hello"
    role: "greeting agent"
}

greeting = infer "Say hello to the world."
print(greeting)
```

No `import openai`. No `client = OpenAI()`. No message lists. No JSON parsing. Five lines.

## How It Works

PyL reads `.pyl` files, finds LLM-specific syntax, validates it, expands it into Python, and passes everything else through. Python is the runtime.

```bash
python src/transpiler.py hello.pyl > hello.py
python hello.py
```

PyL only validates its own primitives. Everything else is Python, and Python validates it at runtime.

## Design Principles

- **Remove boilerplate** — every primitive eliminates a layer of setup the LLM shouldn't have to reason about
- **Golden paths only** — one way to use each primitive. PyL rejects invalid LLM syntax.
- **Small surface area** — fewer choices = less hallucination, less drift, more predictable output
- **Syntax preprocessor** — we expand LLM syntax into Python. Everything else is Python.

## Current Primitives

| Keyword | What it does |
|---|---|
| `agent` | Declares identity — expands into system prompt |
| `infer` | Calls an LLM — expands into `ollama.chat()` |

Everything else is Python. `if`, `for`, `while`, functions, variables, imports — all pass through unchanged.

## What's Next

- `tool` — typed capability declarations
- `context` — conversation state as a first-class type
- `memory` — persistence as a language feature
- Streaming responses
- Model selection

## License

MIT
