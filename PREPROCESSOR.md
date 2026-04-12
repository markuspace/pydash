# The Preprocessor — Reference

## What PyL Is

A **syntax preprocessor** for Python. It runs before Python, reads `.pyl` files, expands LLM-specific syntax into Python, and passes everything else through unchanged. Python never sees `.pyl` files — it only sees the expanded `.py` output.

## The Taxonomy

| Concept | What it does | Output | Boundary |
|---|---|---|---|
| **Preprocessor** | Runs *before* the host compiler. Handles specific keywords, passes everything else through. | Host language source | Hard — only handles its keywords |
| **Transpiler** | Owns the full source-to-source translation. Replaces the host compiler entirely. | Different language source | Owns everything |
| **Compiler** | Translates to a lower-level representation (bytecode, machine code). | Binary/bytecode | Owns everything |
| **DSL** | A standalone language with its own grammar, parser, and semantics. | Whatever its compiler produces | Replaces the host |
| **eDSL** | Embedded *within* the host language using the host's own syntax. No separate toolchain. | Same language | Uses host syntax |
| **Macro system** | A language feature that rewrites syntax at compile time. Built into the compiler. | Same language, expanded | General-purpose rewriting |

## Existing Examples

### C Preprocessor (cpp)
- **Adds:** `#define`, `#include`, `#ifdef`
- **Passes through:** Everything not starting with `#`
- **Boundary:** `#` at line start = preprocessor. Everything else = C compiler.
- **Scope discipline:** The `#` convention creates a hard syntactic boundary. Deliberately limited — not Turing-complete, no recursion, no control flow.

### JSX → JavaScript
- **Adds:** XML-like syntax (`<Component prop={value}>`)
- **Passes through:** All valid JavaScript unchanged
- **Boundary:** `<` at expression start triggers JSX parsing
- **Scope discipline:** Adds exactly one construct (XML elements). Doesn't add types, control flow, or new semantics.

### TypeScript → JavaScript
- **Adds:** Type annotations, interfaces, generics
- **Passes through:** All valid JavaScript (mostly)
- **Boundary:** Type syntax is stripped. Runtime JS semantics preserved 1:1.
- **Scope discipline:** Types are erased at compile time. No runtime semantics added. But — TypeScript has succumbed to scope avalanche: namespaces, enums, decorators, `satisfies`. It's arguably a full language now.

### SASS/SCSS → CSS
- **Adds:** Nesting, variables, mixins, functions, control flow
- **Passes through:** Valid CSS is valid SCSS
- **Boundary:** `@` rules and `$` variables are SASS. Everything else = CSS.
- **Scope discipline:** **Failed.** Started with nesting and variables, then added mixins, functions, loops, conditionals, imports, modules. It's a full programming language that outputs CSS.

### CoffeeScript → JavaScript
- **Adds:** Significant whitespace, implicit returns, comprehensions, destructuring
- **Passes through:** Nothing
- **Boundary:** None. CoffeeScript does not pass through JS.
- **Scope discipline:** **Failed completely.** Not a preprocessor — a full language that compiles to JS.

## Scope Avalanche — The Warning

The pattern is consistent: preprocessors that don't enforce a hard boundary become full languages.

| Tool | Started as | Became |
|---|---|---|
| SASS | CSS with nesting | Full programming language |
| CoffeeScript | Better JS syntax | Full language |
| TypeScript | Types for JS | Near-full language |
| C preprocessor | `#define`, `#include` | Still a preprocessor |
| JSX | XML in JS | Still a preprocessor |

## What Keeps a Preprocessor Bounded

Three mechanisms:

1. **Syntactic markers** — `#` for C, `<` for JSX. You know immediately whether a line is preprocessor or host language. This is the strongest constraint.

2. **Erasure semantics** — the preprocessor adds things that disappear at runtime. Types are erased. XML becomes function calls. If the preprocessor only adds things that vanish, there's a natural ceiling.

3. **Single-purpose design** — JSX adds exactly one thing: XML syntax. The moment you add a second unrelated feature, the pressure to add a third, fourth, and fifth begins.

## What PyL Does

- **Adds:** `agent { }` and `infer "..."`
- **Expands:** `agent` → system prompt string. `infer` → `ollama.chat()` call.
- **Passes through:** Everything else. Python handles it.
- **Boundary:** `agent` and `infer` are PyL's keywords. Everything else is Python.
- **Scope discipline:** Only handles LLM operations. No control flow, no types, no modules. If it's not LLM boilerplate, it's not PyL's job.

## The Boundary Rule

**If it's not LLM boilerplate, it's not PyL's job.**

- `if/else` → Python
- `for` loops → Python
- Functions → Python
- Types → Python
- Imports → Python
- Error handling → Python
- Package management → Python

`agent` and `infer` compress LLM boilerplate. That's the entire scope. Nothing more.
