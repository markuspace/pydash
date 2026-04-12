# Syntax — LLM-Native Language

## Locked Keywords

| Primitive | Keyword | Rationale |
|---|---|---|
| Inference | `infer` | Precise, unambiguous. No confusion with other concepts. |
| Context | `context` | Clear, self-documenting. Worth the extra characters. |
| Identity | `agent` | Declares the entity. Standard across agent frameworks. |
| Memory | `memory` | Clear, natural. Distinct from `context`. |
| Tools | `tool` | Clear, standard. Declares a capability. |

## Traditional Constructs (Unchanged)

- `if`, `else`, `for`, `while`
- `fn` (functions), `mod` (modules), `type` (types)
- `let` (variables), `return`
- Package management (simplified)

## Design Constraint

**One way to do each thing.** No alternatives. The compiler rejects anything outside the golden path. Not a warning — an error.

---

## Hello World

The smallest possible program. An agent that says hello.

```
agent Hello {
    name: "Hello"
    role: "greeting agent"
}

let greeting = infer "Say hello to the world."
print(greeting)
```

That's it. No client initialization. No message lists. No HTTP calls. No JSON parsing.

**What's happening:**
1. `agent Hello { }` — declares identity. Compiled into the system prompt.
2. `infer "..."` — calls the model. Reads `context` implicitly. Returns a string.
3. `print(greeting)` — traditional output.

**What's NOT happening:**
- No `import openai`
- No `client = OpenAI()`
- No `messages = [{"role": "system", "content": "..."}]`
- No `response = client.chat.completions.create(...)`
- No `response.choices[0].message.content`

The boilerplate is gone. The intent is the code.

---

## Test Case: Hello World Transpilation

**Source (`hello.lnl`):**
```
agent Hello {
    name: "Hello"
    role: "greeting agent"
}

let greeting = infer "Say hello to the world."
print(greeting)
```

**Expected transpiled output (`hello.py`):**
```python
import ollama

_SYSTEM_PROMPT = "You are Hello. Your role: greeting agent."

_greeting = ollama.chat(
    model="phi3:mini",
    messages=[
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": "Say hello to the world."}
    ]
)["message"]["content"]

print(_greeting)
```

**Transpiler rules this validates:**
1. `agent { }` block → `_SYSTEM_PROMPT` string with `name` and `role`
2. `infer "prompt"` → `ollama.chat()` call with system + user message
3. `let x = ...` → `_x = ...` (underscore-prefixed variable)
4. `print(x)` → `print(_x)` (pass-through)
5. Implicit `import ollama` at top
6. Hardcoded `model="phi3:mini"` (scaffolding, not a language feature)

The transpiler must produce EXACTLY this output. No more, no less.

---

## Test Case: Hello World Transpilation

**Source (`hello.lnl`):**
```
agent Hello {
    name: "Hello"
    role: "greeting agent"
}

let greeting = infer "Say hello to the world."
print(greeting)
```

**Expected transpiled output (`hello.py`):**
```python
import ollama

_SYSTEM_PROMPT = "You are Hello. Your role: greeting agent."

_greeting = ollama.chat(
    model="phi3:mini",
    messages=[
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": "Say hello to the world."}
    ]
)["message"]["content"]

print(_greeting)
```

**Transpiler rules this validates:**
1. `agent { }` block → `_SYSTEM_PROMPT` string with `name` and `role`
2. `infer "prompt"` → `ollama.chat()` call with system + user message
3. `let x = ...` → `_x = ...` (underscore-prefixed variable)
4. `print(x)` → `print(_x)` (pass-through)
5. Implicit `import ollama` at top
6. Hardcoded `model="phi3:mini"` (scaffolding, not a language feature)

The transpiler must produce EXACTLY this output. No more, no less.
