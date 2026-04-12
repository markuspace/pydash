# LLM-Native Language: Primitive Analysis

## The 5 Primitives × 8 Dimensions

### 1. **Inference** — calling a model is a keyword, not a function

| Dimension | Current (Python/Go) | LLM-Native Language |
|---|---|---|
| **Token Cost** | ~50-100 tokens for setup (client init, message list, params) | ~5-10 tokens: `infer model "gpt-4" from ctx` |
| **Type Safety** | Strings in, strings out. No compile-time validation. | Typed prompts, typed responses, schema validation at compile time. |
| **Runtime** | Sync or async, streaming bolted on. | Async by default, streaming is the natural mode. Blocking is the opt-in. |
| **Composability** | Manual wiring to context, tools, memory. | Composes with all 4 other primitives natively. |
| **Error Handling** | HTTP exceptions, retry loops, timeout management. | Language-level: `rate_limit`, `model_unavailable`, `timeout` — catchable patterns. |
| **State** | Stateless call. | Stateless, but carries Context implicitly. |
| **Security** | API keys in env vars, manual rate limiting. | Model selection constraints, cost budgets, output validation at the type level. |

### 2. **Context** — the conversation window is a first-class type

| Dimension | Current | LLM-Native |
|---|---|---|
| **Token Cost** | Manual message list management, truncation logic, summarization. | `ctx: Context` — auto-manages window, auto-compacts. |
| **Type Safety** | Untyped dicts/lists. Role strings. | Typed roles (`user`, `assistant`, `tool`, `system`), typed content (`text`, `image`, `audio`). |
| **Runtime** | Grows unbounded until you manually truncate. | Mutable, append-only with compaction strategies built in. |
| **Composability** | Passed manually to every call. | Implicit in scope. Inference reads it, Tools write to it, Memory hydrates it. |
| **Error Handling** | Context overflow crashes or silent truncation. | Auto-summarize on overflow. Token budget exceeded → graceful degradation. |
| **State** | Mutable list. | Append-only with explicit compaction. |
| **Security** | Context injection attacks, leaked history. | Privacy boundaries, sensitive data redaction, scope isolation. |

### 3. **Identity** — who the agent IS is declared, not string-concatenated

| Dimension | Current | LLM-Native |
|---|---|---|
| **Token Cost** | System prompt string concatenation. | Declaration block: `agent RoboCode { ... }` |
| **Type Safety** | Free-form text. No validation. | Typed attributes: `name`, `role`, `constraints[]`, `capabilities[]`. |
| **Runtime** | Injected as first message. Static. | Static declaration, injected into Context at init. Can have dynamic extensions. |
| **Composability** | Manually prepended to messages. | Feeds into Context, constrains Inference, declares available Tools. |
| **Error Handling** | Identity drift, constraint bypass. | Compile-time validation of constraints. Runtime constraint violation errors. |
| **State** | Immutable. | Immutable core, extensible edges. |
| **Security** | Prompt injection, role confusion. | Constraint enforcement at the language level. Identity cannot be overridden by user input. |

### 4. **Memory** — persistence is a language feature, not a database call

| Dimension | Current | LLM-Native |
|---|---|---|
| **Token Cost** | DB setup, embedding pipeline, vector store queries. | `mem.store(key, value)`, `mem.retrieve(query, top_k=5)` |
| **Type Safety** | Raw strings or JSON. No schema. | Typed memory slots. Schema validation. Retrieval type hints. |
| **Runtime** | Sync DB calls or async vector lookups. | Async retrieval, auto-indexing, caching, similarity search. |
| **Composability** | Manual integration with context and inference. | Feeds into Context. Retrieved during Inference. Stores Tool results. |
| **Error Handling** | Connection failures, embedding errors, index corruption. | Graceful degradation. Fallback to keyword search if embeddings fail. |
| **State** | Persistent, external. | Persistent, indexed, searchable, forgettable. |
| **Security** | Data leakage, unauthorized access. | Scoped memory, encryption, access control, memory poisoning detection. |

### 5. **Tools** — capabilities are declarations, not JSON schemas

| Dimension | Current | LLM-Native |
|---|---|---|
| **Token Cost** | JSON schema + function implementation + registration. | `tool read_file(path: String) -> String { ... }` — one declaration. |
| **Type Safety** | Untyped JSON. Runtime validation. | Typed inputs, typed outputs, pre/post conditions. |
| **Runtime** | Synchronous execution. Async bolted on. | Sync by default, async support, sandboxing. |
| **Composability** | Registered manually with the LLM client. | Declared in Identity. Called during Inference. Results in Context. Can write to Memory. |
| **Error Handling** | Exceptions, timeouts, invalid input. | Language-level: `permission_denied`, `timeout`, `invalid_input`. |
| **State** | Stateless by default. | Stateless. Can access Memory and Context. |
| **Security** | Unrestricted access. Manual sandboxing. | Sandboxing, permission boundaries, rate limiting, output validation. |

---

## The Network

These aren't independent. They form a cycle:

```
                    ┌─────────────┐
                    │  IDENTITY   │
                    │  (who I am) │
                    └──────┬──────┘
                           │ declares
                           ▼
                    ┌─────────────┐
          ┌────────│   CONTEXT   │────────┐
          │        │ (what I know│        │
          │        │  right now) │        │
          │        └──────┬──────┘        │
          │               │ feeds         │
          │               ▼               │
          │        ┌─────────────┐        │
          │        │  INFERENCE  │        │
          │        │ (what I do) │        │
          │        └──────┬──────┘        │
          │               │ triggers      │
          │               ▼               │
          │        ┌─────────────┐        │
          │        │   TOOLS     │        │
          │        │ (what I use)│        │
          │        └──────┬──────┘        │
          │               │ reads/writes  │
          │               ▼               │
          │        ┌─────────────┐        │
          └───────│   MEMORY    │────────┘
                  │ (what I keep)│
                  └─────────────┘
```

### The Cycle

1. **Identity** declares who the agent is and what Tools it has
2. **Context** holds the current conversation state
3. **Inference** reads Context + Identity, produces responses, triggers Tools
4. **Tools** execute actions, read/write Memory, update Context
5. **Memory** persists long-term state, hydrates Context on retrieval
6. Back to **Context** — the loop continues

### What makes this a language and not a framework

- The primitives are **keywords**, not libraries
- The compiler/validator understands the **semantics** of LLM operations
- Type safety applies to **prompts, responses, and tool contracts**
- The runtime manages **context windows, token budgets, and rate limits** natively
- **Identity** is a compile-time construct, not a runtime string

---

## What We're NOT Reinventing

Traditional programming languages already solve these well:
- **Variables and types** — keep them
- **Control flow** (if/else, loops) — keep them
- **Functions and modules** — keep them
- **Error handling** — keep them, extend with LLM-specific patterns
- **Package management** — keep it, but make it simpler than Python's

What we're adding:
- **Inference** as a first-class keyword
- **Context** as a built-in type
- **Identity** as a declaration block
- **Memory** as a language feature
- **Tools** as typed declarations

---

## Open Questions

1. What does the actual syntax look like?
2. What's the runtime? Interpreter? Compiled? Transpiled to Python/Go?
3. How does the compiler validate prompts and tool contracts?
4. What's the minimal viable subset to implement first?
5. How do we handle streaming responses at the language level?
6. What does multi-agent look like? (Agents calling other agents)
7. How do we handle cost/token budgeting at compile time?
