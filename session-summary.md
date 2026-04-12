# Session Summary — LLM-Native Language Design

## What We Built

### PyL — Syntax Preprocessor for Python LLM Code
- **What it is:** A transpiler that expands compressed LLM syntax into working Python.
- **File extension:** `.pyl`
- **Implementation:** Python script using regex/token-level parsing. No external dependencies.
- **Current primitives:** `agent { }` and `infer "..."`
- **Hello world works:** Five lines of `.pyl` → working Python → runs with Ollama/phi3:mini
- **Location:** `/home/robomark/Projects/lnl/`
- **Files:** `src/transpiler.py`, `hello.pyl`, `hello.py`, `README.md`, `LICENSE`, `.gitignore`

### Design Decisions
- **Not a language, not a runtime:** A syntax preprocessor. We generate Python. Python is the runtime.
- **Scope boundary:** Only LLM boilerplate. `if/for/while`, functions, types, imports — all Python.
- **Golden path:** One way to do each thing. The preprocessor rejects invalid LLM syntax.
- **Pass-through:** Everything that isn't `agent` or `infer` passes through as Python unchanged.

## The Framework

### The Unifying Principle
Every paradigm shift in programming follows the same pattern: **translator of intent into mechanics.** The gap between what you want to say and what you have to type shrinks. The tool absorbs the mechanical complexity so you can stay at the level of intent.

### The Surface Area Thesis
Every independent thing an LLM must get right is a multiplicative failure probability. The gap between HumanEval (~90%) and MobileDev-Bench (~5%) is 18x — and the only difference is surface area. PyL's purpose is to shrink the surface area between intent and mechanics for LLM programming.

### Our Bold Claim
**"Strings Are The Wrong Type For Intelligence."** We're treating LLM interaction as text manipulation — string concatenation, JSON parsing, HTTP clients — when it should be a first-class language construct. The old way isn't wrong. It just can't scale.

## The Big Five — Paradigm Shifts

### 1. Abstraction — `=`
**The story:** Assembly got us the first computers. Direct, honest, fast. Then scientists came — physicists who thought in formulas, not registers. `X = (A + B) * C` meant six assembly instructions. FORTRAN (1957) closed the gap. The compiler figured out the registers.
**Wave:** Origin (1954, Backus proposes) → Early adopters (1956, internal demo) → Crest (1957, FORTRAN manual) → Late majority (1960s) → Laggards (1970s+, bootloaders/drivers).
**Emotional center:** Vindication. Backus proved the skeptics wrong.
**Code:** `LOAD A, R1; ADD B, R1; STORE R1, TEMP; LOAD C, R2; MUL TEMP, R2; STORE R2, X` → `X = (A + B) * C`
**Historical driver:** WWII → Cold War. Government-funded computing for ballistics and nuclear weapons.
**Cultural driver:** Scientists needed to program, not assembly specialists.
**Technological driver:** Larger memory. Compilers proved they could match hand-written assembly.

### 2. Control Flow — `for`
**The story:** `goto` got us to the moon. Apollo guidance software ran on it. Then programs grew to thousands of lines. The arrows multiplied. Nobody could trace them. Dijkstra's "Go To Statement Considered Harmful" (1968) crystallized it: you can't prove correctness of code you can't trace.
**Wave:** Origin (1966, Böhm-Jacopini theorem) → Early adopters (1968, Dijkstra) → Crest (1972, C language) → Late majority (1980s) → Laggards (1990s+, C error handling/state machines).
**Emotional center:** Diagnosis. Dijkstra named a crisis.
**Code:** `i = 0; loop: if (i >= n) goto end; ...; i = i + 1; goto loop; end:` → `for (i = 0; i < n; i++) { ... }`
**Historical driver:** The Space Race. NASA needed reliable guidance software.
**Cultural driver:** Computing moved from lab to institution. Engineers, not mathematicians, writing code.
**Technological driver:** Programs grew from hundreds to thousands of lines.

### 3. Encapsulation — `class`
**The story:** Structs and separate functions built the world. Unix, C. Data here, behavior there. Then came GUIs. Every widget had state AND behavior. Passing the struct to every function became a coordination nightmare. `class` arrived in C++ (1983) and the coordination disappeared.
**Wave:** Origin (1967, Simula 67) → Early adopters (1972, Smalltalk at PARC) → Crest (1983, C++ 1.0) → Late majority (1995, Java) → Laggards (2000s+, game engines/HPC).
**Emotional center:** Seduction. Jobs saw the future at PARC. But the real driver was coordination pain.
**Code:** `struct Button { ... }; void draw_button(struct Button *b) { ... }; void click_button(struct Button *b) { ... }` → `class Button { void draw() { ... }; void click() { ... } }`
**Historical driver:** Personal computer revolution (1970s-1990s). Xerox PARC, Apple, Microsoft.
**Cultural driver:** Users became consumers. GUIs made computing experiential, not operational.
**Technological driver:** GUI programming — every widget has state AND behavior. Hardware powerful enough for vtable overhead.

### 4. Asynchrony — `await`
**The story:** Blocking I/O was honest. `read_file()` sat there waiting. Then the web. Network requests are 100,000x slower than CPU. Callbacks scaled but created nested hell. `async/await` arrived in C# (2012), then Python (2015), JS (2017), Rust (2019), Swift (2021). Five languages, independently. Inevitable.
**Wave:** Origin (2009, Node.js demo) → Early adopters (2012, C# 5.0) → Crest (2017, ES2017) → Late majority (2019, Rust) → Laggards (2020s+, scripts/CLI tools).
**Emotional center:** Relief. Async code finally reads like sync code.
**Code:** `fetch(url, function(err, data) { parse(data, function(err, result) { save(result, function(err) { done(); }); }); });` → `const data = await fetch(url); const result = await parse(data); await save(result);`
**Historical driver:** The dot-com boom (1995-2001). The web went mainstream.
**Cultural driver:** Always-on culture. Software as service, not product. Real-time expectations.
**Technological driver:** Network I/O 100,000x slower than CPU. Multi-core processors. Node.js proof.

### 5. Intelligence — `infer`
**The story:** HTTP calls, JSON parsing, system prompt strings — they work. They built ChatGPT, Claude. But now we're building agents. Thirty concerns for one operation. The coordination cost is exploding. `agent` and `infer` close the gap.
**Wave:** Origin (2017, Transformer paper) → Early adopters (2022, ChatGPT) → Crest (???) → Late majority (future) → Laggards (future).
**Emotional center:** Anticipation. The wave is coming.
**Code:** `client = openai.OpenAI(); response = client.chat.completions.create(model="gpt-4", messages=[...]); result = response.choices[0].message.content` → `result = infer "prompt"`
**Historical driver:** Transformer architecture (2017), GPT-3 (2020), ChatGPT (2022). The AI arms race.
**Cultural driver:** ChatGPT moment. AI democratized. Everyone wants to build with LLMs.
**Technological driver:** LLM API proliferation. Agent complexity — tools, memory, context, retries.

## Vocabulary

| Term | Definition | Portable? |
|---|---|---|
| **Lens** | A way of focusing attention on specific aspects of a subject. Analytical framework and narrative template are both lenses. | Yes — standard term |
| **Dimension** | An axis along which you measure or analyze something within a lens. | Yes — standard term |
| **Factor** | A specific condition that contributed to a paradigm shift. Multiple factors converge. | Yes — standard term |
| **Wave** | The adoption curve of a paradigm shift. Origin → Early adopters → Crest → Late majority → Laggards. | Yes — standard term |
| **Crest** | The moment the majority of working practitioners cross over from the old way to the new. | Yes — standard term |
| **Stratification** | Paradigm shifts don't replace the previous layer — they stratify it. The old way finds its niche. | No — our framing |

## The Five Dimensions (Analytical Lens)
1. **Intent** — What you wanted to say. The mental model. "I want to repeat this." "I want to call the model."
2. **Mechanics** — What you had to type instead. The friction. Labels, jumps, HTTP clients, JSON parsing.
3. **Scale** — When it broke. The turning point. Hundreds of lines → thousands. One-off scripts → production agents.
4. **Absorption** — What closed the gap. The new syntax. `for`, `class`, `async/await`, `agent`/`infer`.
5. **Legacy** — Where the old way still lives. Bootloaders, CLI tools, prototypes. The old way wasn't wrong — it found its niche.

## Files Created
- `/home/robomark/Projects/opencode-engineer/design-decisions.md` — PyL design decisions, updated to reflect preprocessor framing
- `/home/robomark/Projects/opencode-engineer/surface-area.md` — The surface area problem, documented failure modes, historical precedent
- `/home/robomark/Projects/opencode-engineer/syntax.md` — Syntax decisions, hello world, test case
- `/home/robomark/Projects/opencode-engineer/big-five.md` — The Big Five with five dimensions
- `/home/robomark/Projects/opencode-engineer/big-five-factors.md` — Catalog of factors for each shift
- `/home/robomark/Projects/opencode-engineer/keywords-added.md` — Comprehensive survey of keywords added to existing languages
- `/home/robomark/Projects/opencode-engineer/shift-oop.md` — OOP shift through five dimensions (template for others)
- `/home/robomark/Projects/lnl/README.md` — PyL project README
- `/home/robomark/Projects/lnl/LICENSE` — MIT license
- `/home/robomark/Projects/lnl/.gitignore` — Python basics
- `/home/robomark/Projects/lnl/src/transpiler.py` — The transpiler
- `/home/robomark/Projects/lnl/hello.pyl` — Hello world source
- `/home/robomark/Projects/lnl/hello.py` — Transpiled output

## What's Next
- Build the `tool` primitive in the transpiler
- Add `context` and `memory` primitives
- Write the full narrative essay with before/after code examples
- Decide on publication form (arxiv, moltbook, GitHub)
