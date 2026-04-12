# The Big Five — Factors

The specific conditions that forced each paradigm shift. Not the story. Not the analysis. Just the factors.

---

## 1. Abstraction — Assembly → High-Level Expressions

- **Scientific computing demand** — Physicists and engineers needed to program, not assembly specialists
- **Post-WWII / Cold War** — Massive investment in computing for ballistics, cryptography, nuclear research
- **Mathematical formula complexity** — Writing `X = (A + B) * C` in assembly required 6+ instructions
- **Hardware improvements** — Larger memory made compiler overhead acceptable
- **Compiler technology advances** — Proved compilers could match or beat hand-written assembly
- **Labor shortage** — Not enough assembly programmers to meet demand
- **Time pressure** — Scientists couldn't wait months for a single program

---

## 2. Control Flow — `goto` → `if/for/while`

- **Program size growth** — Hundreds of lines → thousands of lines
- **Software crisis** — Projects running years over budget, failing entirely
- **Untraceable code** — Nobody could follow the arrows anymore
- **Correctness proofs** — Formal verification required structured control flow
- **Maintenance burden** — Fixing bugs in spaghetti code took longer than writing it
- **Dijkstra's influence** — "Go To Statement Considered Harmful" (1968) crystallized the problem
- **Academic research** — Structured programming theory proved alternatives existed

---

## 3. OOP — structs + functions → `class`

- **GUI programming** — Every widget has state AND behavior. Coordination exploded.
- **Software complexity crisis** — Programs exceeded tens of thousands of lines. Global state unmanageable.
- **Reusability demands** — "Write once, use many times." Inheritance enabled extension without copying.
- **Simulation needs** — Simula (1967) built for modeling real-world systems. Objects mapped naturally.
- **Hardware improvements** — Computers powerful enough for vtable overhead and dynamic dispatch.
- **Academic research** — Type systems, encapsulation, polymorphism formally studied.
- **Industry adoption** — C++ (1983) mainstreamed it. Java (1995) made it the default.

---

## 4. Async — blocking → `async/await`

- **The internet** — Network I/O is 100,000x slower than CPU. Blocking doesn't scale.
- **Concurrency demands** — Thousands of concurrent connections. Thread-per-request exhausted memory.
- **Callback hell** — Nested functions, backwards-reading code, scattered error handling.
- **Debugging nightmare** — State passed manually between callbacks. Impossible to trace.
- **Node.js proof** — Single-threaded event loops could handle massive concurrency.
- **Multi-core processors** — Parallelism became necessary, not optional.
- **Five-language convergence** — C#, Python, JS, Rust, Swift all added it independently. Inevitable.

---

## 5. AI — manual prompting → LLM-native syntax

- **ChatGPT moment** — AI democratized. Everyone wants to build with LLMs.
- **Agent complexity** — Tools, memory, context, retries, rate limits. Thirty concerns per call.
- **Coordination cost explosion** — HTTP clients, message lists, JSON parsing, tool schemas.
- **LLM API proliferation** — OpenAI, Anthropic, Ollama, open-source models. Integration burden.
- **Production-scale systems** — One-off scripts → production agents. The old way broke.
- **Prompt engineering gap** — System prompt strings as code. Fragile, untestable, drifting.
- **Surface area problem** — Every LLM call adds 30+ mechanical concerns. The gap between intent and mechanics is enormous.

---

## The Pattern

Every shift was forced by multiple factors converging. No single factor caused any of them. The old way worked until the factors aligned — then it broke fundamentally, not incrementally.
