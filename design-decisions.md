# Design Decisions — LLM-Native Language

## Philosophy

- **Remove boilerplate** — that's the entire scope. Move LLM setup, HTTP calls, JSON parsing, schema registration into syntax.
- **Constraints are the feature** — fewer choices = less hallucination, less drift, more predictable LLM output
- **Golden paths only** — the compiler rejects anything outside them. Not a warning. An error.
- **Not a toy** — built for production agentic coders, not experiments
- **Small surface area** — the LLM can master it quickly because there's only one way to do each thing
- **No enforced runtime model** — the transpiler generates Python. No prescribed agent loop. No enforced architecture. The agent loop can come later when we understand what it should be.

## What We Keep (Unchanged)

Traditional programming constructs are solved problems. LLMs already understand them perfectly. No reason to reinvent:

- `if/else`, `for`, `while`
- Functions, modules, types
- Variables, error handling
- Package management (but simpler than Python's)

## What We Add (5 Primitives, One Way Each)

| Primitive | What it is | Boilerplate it removes |
|---|---|---|
| **Inference** | Keyword, not a function | HTTP calls, client setup, JSON parsing, retry loops |
| **Context** | Built-in type, implicit in scope | Manual message lists, truncation logic, summarization |
| **Identity** | Declaration block (`agent { }`) | System prompt string concatenation |
| **Memory** | Language feature (`mem.store`, `mem.retrieve`) | DB setup, embedding pipeline, vector store queries |
| **Tools** | Typed declarations (`tool name() -> T { }`) | JSON schema registration, manual tool wiring |

## Implementation

- **Transpiler** — reads `.lnl` files, validates golden path, generates Python
- **No custom runtime** — Python IS the runtime
- **No custom LLM client** — Python libraries (ollama, openai, etc.) handle the actual calls
- **Validation at transpile time** — if it doesn't follow the golden path, it doesn't produce Python

## What We're NOT Doing (Yet)

- Enforcing an agent loop / cycle model
- Defining how agents should run continuously
- Prescribing multi-agent communication patterns
- Building a custom runtime or interpreter

These are future concerns. Right now: remove boilerplate, generate working code, prove the concept.

## Research-Informed Design Principles

From 9 paradigms studied (Reactive, Dataflow, Actor, Event-Loop, State Machines, BDI Agents, Cyclic Graphs, Neural, AI Agent Loops):

1. Don't make cycles an error case. Make them the default. (FRP failed because cycles were pathological.)
2. The cycle must be **visible, inspectable, and programmable**. (JavaScript's event loop is invisible — that's a mistake.)
3. State machines are too rigid for agents. Use evolving context instead.
4. The interpreter loop should not be fixed. (BDI agents fail here.)
5. Logical timestamps (from Differential Dataflow) make cycles tractable — convergence detection, debugging, termination for free.
6. Nested cycles at multiple timescales, like the brain's layered architecture.

These principles inform future design. They don't constrain the MVP.

## Design Principles

### Self-Documenting Tool Signatures

Tool functions should NOT need docstrings to work. The function name and parameter names ARE the description. The preprocessor auto-generates tool schemas from the signature:

```
write_file(path: str, content: str) → schema: "write_file with path, content"
run_command(cmd: str) → schema: "run_command with cmd"
```

This is a constraint, not a convenience. If the function name isn't clear enough, that's a naming problem, not a documentation problem. The language forces good naming conventions at the fundamental level. No additional comments should be required to make tool calling work.

## Open Questions

1. **Streaming** — how do we handle streaming responses at the language level?
2. **Multi-agent** — what does agent-to-agent communication look like?
3. **Cost/token budgeting** — how do we handle this at compile time?
4. **Model selection** — how does the programmer choose which model to use?
5. **Error handling** — what happens when inference fails?
