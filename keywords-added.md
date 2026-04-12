# Keywords Added to Existing Languages

A survey of syntactic keywords that were added to languages after their initial release. Each example follows the same arc: problem exists → pattern/library proves value → keyword becomes syntax → workaround becomes legacy.

---

## JavaScript / ECMAScript

### `let` / `const`
- **Version:** ES6 (2015)
- **Before:** Only `var` — function-scoped, hoisted
- **Problem solved:** Block-scoped variable declarations

### `class`
- **Version:** ES6 (2015)
- **Before:** Prototype chains, constructor functions, manual `Object.create()`
- **Problem solved:** Familiar OOP syntax over JavaScript's prototype system

### `async` / `await`
- **Version:** ES2017
- **Before:** Callbacks ("callback hell"), Promise chains with `.then()`/`.catch()`
- **Problem solved:** Asynchronous code that reads like synchronous code

### `yield`
- **Version:** ES6 (2015)
- **Before:** Manual state machines, library-based solutions
- **Problem solved:** Generator functions that pause and resume execution

### `import` / `export`
- **Version:** ES6 (2015)
- **Before:** CommonJS `require()`, AMD `define()`, `<script>` tags
- **Problem solved:** Native module system with static analysis and tree-shaking

### `for...of`
- **Version:** ES6 (2015)
- **Before:** `for...in` (iterates property names, including inherited) or manual index loops
- **Problem solved:** Iterate over iterable values directly

### `extends` / `super`
- **Version:** ES6 (2015)
- **Before:** `Child.prototype = Object.create(Parent.prototype)`
- **Problem solved:** Declarative class inheritance with parent method access

---

## Python

### `with`
- **Version:** 2.5 (2006), PEP 343
- **Before:** `try`/`finally` blocks for resource cleanup
- **Problem solved:** RAII-like resource management via context managers

### `async` / `await`
- **Version:** 3.5 (2015), PEP 492
- **Before:** `@asyncio.coroutine` decorator with `yield from`
- **Problem solved:** Dedicated coroutine keywords, distinct from generators

### `match` / `case`
- **Version:** 3.10 (2021), PEP 634
- **Before:** `if isinstance(x, A) ... elif isinstance(x, B) ...` chains
- **Problem solved:** Structural pattern matching — destructure complex data in one construct

### `:=` (walrus operator)
- **Version:** 3.8 (2019), PEP 572
- **Before:** Separate assignment statement, or duplicate the expression
- **Problem solved:** Assign and use a value in a single expression

### `nonlocal`
- **Version:** 3.0 (2008), PEP 3104
- **Before:** No way to rebind variables in enclosing scopes; mutable container workarounds
- **Problem solved:** Explicitly rebind names in the nearest enclosing non-global scope

### `type` (type alias keyword)
- **Version:** 3.12 (2023), PEP 695
- **Before:** `TypeAlias` from `typing` module with assignment
- **Problem solved:** First-class syntax for type aliases with proper scoping

---

## Java

### `var`
- **Version:** 10 (2018), JEP 286
- **Before:** Explicit type declarations on every local variable
- **Problem solved:** Reduced verbosity for obvious types while preserving static typing

### `->` (lambda)
- **Version:** 8 (2014), JSR 335
- **Before:** Anonymous inner classes — 5+ lines for a single function
- **Problem solved:** Concise function literals enabling functional-style programming

### `record`
- **Version:** 16 (2021), JEP 395
- **Before:** Manual classes with fields, constructors, `equals()`, `hashCode()`, `toString()`
- **Problem solved:** Immutable data carriers in one declaration

### `sealed`
- **Version:** 17 (2021), JEP 409
- **Before:** No way to restrict which classes can extend a given class
- **Problem solved:** Explicitly limit permitted subclasses, enabling exhaustive pattern matching

### `yield` (in switch expressions)
- **Version:** 14 (2020), JEP 361
- **Before:** Switch statements with `break` and temporary variables
- **Problem solved:** Switch expressions that produce values

### `module` / `requires` / `exports`
- **Version:** 9 (2017), JEP 261
- **Before:** All public types on classpath accessible to all code
- **Problem solved:** Strong encapsulation at the module level

---

## C#

### `async` / `await`
- **Version:** 5.0 (2012)
- **Before:** `Task.ContinueWith()`, callback chains, Event-based Asynchronous Pattern
- **Problem solved:** Synchronous-looking async code with automatic state machine generation

### `var`
- **Version:** 3.0 (2007)
- **Before:** Explicit type declarations
- **Problem solved:** Reduced verbosity, especially for anonymous types and LINQ results

### `yield`
- **Version:** 2.0 (2005)
- **Before:** Manual `IEnumerable`/`IEnumerator` with explicit state machines
- **Problem solved:** Compiler-generated iterators — write a loop, compiler builds the state machine

### `dynamic`
- **Version:** 4.0 (2010)
- **Before:** Reflection (`Type.InvokeMember`) or `object` with explicit casting
- **Problem solved:** Late-bound operations at runtime

### `nameof`
- **Version:** 6.0 (2015)
- **Before:** String literals for member names — break silently on rename
- **Problem solved:** Compile-time-safe retrieval of symbol names

### `with` (record copy-and-update)
- **Version:** 9.0 (2020)
- **Before:** Manual copy constructors
- **Problem solved:** Immutable copy-and-update syntax: `var copy = original with { Name = "New" }`

---

## C++

### `auto`
- **Version:** C++11 (2011)
- **Before:** Explicit type declarations, including verbose template types
- **Problem solved:** Compiler deduces the type

### `nullptr`
- **Version:** C++11 (2011)
- **Before:** `0` or `NULL` (an integer), causing overload ambiguity
- **Problem solved:** Distinct null pointer literal

### `constexpr`
- **Version:** C++11 (2011)
- **Before:** `const` with integral types only, or preprocessor macros
- **Problem solved:** Guaranteed compile-time evaluation

### `noexcept`
- **Version:** C++11 (2011)
- **Before:** `throw()` exception specification — runtime overhead, poorly understood
- **Problem solved:** Compile-time guarantee that a function does not throw

### `concept` / `requires`
- **Version:** C++20 (2020)
- **Before:** SFINAE with `std::enable_if` — cryptic, hard to debug
- **Problem solved:** Named constraints on template parameters with clear error messages

### `module` / `import`
- **Version:** C++20 (2020)
- **Before:** `#include` — textually pastes headers, slow compilation
- **Problem solved:** True module system with faster compilation

### `co_await` / `co_yield` / `co_return`
- **Version:** C++20 (2020)
- **Before:** Manual state machines, callback-based APIs
- **Problem solved:** Native coroutine support

---

## Rust

### `async` / `await`
- **Version:** 1.39 (2019)
- **Before:** Futures 0.1 combinator chains (`.and_then()`, `.map()`) — deeply nested
- **Problem solved:** Synchronous-looking async code with compiler-generated state machines

### `dyn`
- **Version:** 2021 edition
- **Before:** Bare trait names as types (`Box<Trait>`)
- **Problem solved:** Explicit syntax distinguishing trait objects from generic type parameters

### `impl Trait`
- **Version:** 1.26 (return), 1.34 (argument)
- **Before:** Explicit generic type parameters with trait bounds
- **Problem solved:** Hide concrete types in function signatures

---

## Swift

### `guard`
- **Version:** 2.0 (2015)
- **Before:** Nested `if-let` "pyramid of doom"
- **Problem solved:** Early exit pattern that flattens control flow

### `async` / `await`
- **Version:** 5.5 (2021)
- **Before:** Closure-based completion handlers
- **Problem solved:** Structured concurrency with synchronous-looking async code

### `actor`
- **Version:** 5.5 (2021)
- **Before:** Manual thread synchronization with locks, dispatch queues
- **Problem solved:** Compiler-enforced isolation of mutable state

### `throw` / `throws` / `do` / `catch`
- **Version:** 2.0 (2015)
- **Before:** NSError pointer pattern (`func foo(error: NSErrorPointer) -> Bool`)
- **Problem solved:** Native error handling with typed errors

---

## Go

### `any`
- **Version:** 1.18 (2022)
- **Before:** `interface{}` — semantically opaque
- **Problem solved:** Readable alias for the empty interface

### Generics (`[T any]`)
- **Version:** 1.18 (2022)
- **Before:** `interface{}` with runtime type assertions, code generation, or duplicated code
- **Problem solved:** Parametric polymorphism with compile-time type safety

---

## PHP

### `fn` (arrow functions)
- **Version:** 7.4 (2019)
- **Before:** `function() use ($x) { return $x + 1; }` — verbose with explicit `use` clause
- **Problem solved:** Concise single-expression functions with automatic variable capture

### `match`
- **Version:** 8.0 (2020)
- **Before:** `switch` with `break`, fallthrough bugs, loose `==` comparison
- **Problem solved:** Expression-based matching with strict `===` and no fallthrough

### `enum`
- **Version:** 8.1 (2021)
- **Before:** Class constants or integer constants
- **Problem solved:** First-class enumerated types with methods and interfaces

### `readonly`
- **Version:** 8.1 (2021)
- **Before:** Private properties with only a getter, or docblock annotations
- **Problem solved:** Language-enforced immutability

---

## Ruby

### `->` (stabby lambda)
- **Version:** 1.9 (2007)
- **Before:** `lambda { }` or `Lambda.new { }`
- **Problem solved:** Concise lambda syntax with mandatory parentheses

### Pattern matching (`in`)
- **Version:** 2.7 (2019, experimental), 3.0 (2020)
- **Before:** Manual `case/when` with type checking and destructuring
- **Problem solved:** Declarative pattern matching on arrays, hashes, objects

### Endless method (`def foo = expr`)
- **Version:** 3.0 (2020)
- **Before:** Full `def foo; expr; end` even for one-liners
- **Problem solved:** Concise single-expression method definitions

---

## C

### `_Generic`
- **Version:** C11 (2011)
- **Before:** Preprocessor macros with type-specific variants
- **Problem solved:** Type-generic expressions at compile time

### `_Static_assert`
- **Version:** C11 (2011)
- **Before:** Array size tricks or no compile-time assertions
- **Problem solved:** Clean compile-time assertions with custom error messages

### `_Thread_local`
- **Version:** C11 (2011)
- **Before:** Platform-specific thread-local storage (`__thread`, `__declspec(thread)`)
- **Problem solved:** Standardized thread-local storage

---

## Perl

### `say`
- **Version:** 5.10 (2007)
- **Before:** `print "hello\n"`
- **Problem solved:** Print with automatic trailing newline

### `state`
- **Version:** 5.10 (2007)
- **Before:** `my` variables in outer scope or `our` package variables
- **Problem solved:** Persistent lexical variables across subroutine calls

### `//` (defined-or)
- **Version:** 5.10 (2007)
- **Before:** `defined($x) ? $x : $default`
- **Problem solved:** Default only when left side is `undef`, not any false value

---

## Haskell

### `do` notation
- **Version:** Haskell 98 (1998)
- **Before:** Explicit `>>=` (bind) chains — deeply nested expressions
- **Problem solved:** Monadic code that reads like imperative code

---

## Scala

### `given` / `using`
- **Version:** Scala 3 (2021)
- **Before:** `implicit` keyword — overloaded and confusing
- **Problem solved:** Separate syntax for implicit parameters and definitions

### `extension` methods
- **Version:** Scala 3 (2021)
- **Before:** Implicit classes with boilerplate
- **Problem solved:** Add methods to existing types without implicit class wrappers

---

## Lua

### `goto`
- **Version:** 5.2 (2011)
- **Before:** No goto; structured control flow only
- **Problem solved:** Breaking out of deeply nested loops, implementing state machines

---

## R

### `|>` (pipe operator)
- **Version:** 4.1 (2021)
- **Before:** Nested function calls `f(g(h(x)))` or magrittr's `%>%`
- **Problem solved:** Left-to-right data pipeline as a language feature

---

## TypeScript

### `satisfies`
- **Version:** 4.9 (2022)
- **Before:** Type assertions (`as Type`) that could narrow types undesirably
- **Problem solved:** Validate expression matches a type without changing inferred type

### `as const`
- **Version:** 3.4 (2019)
- **Before:** Mutable type inference for object literals
- **Problem solved:** Narrowest possible literal types for type-safe configuration

### `infer`
- **Version:** 2.8 (2018)
- **Before:** Manual type extraction with complex mapped types
- **Problem solved:** Extract type components within conditional types

### `keyof`
- **Version:** 2.1 (2016)
- **Before:** Manual union of string literal types for object keys
- **Problem solved:** Get union of all property keys of a type

---

## The Universal Pattern

Every keyword addition follows the same arc:

1. **The problem exists** — developers write the same pattern over and over
2. **Libraries/frameworks prove the value** — external tools demonstrate it works
3. **The keyword arrives** — the pattern becomes syntax
4. **The workaround becomes legacy** — nobody uses the old pattern anymore

### The Standout: `async/await`

Added to five languages independently over a decade:

| Language | Version | Year | Before |
|---|---|---|---|
| C# | 5.0 | 2012 | `Task.ContinueWith()` |
| Python | 3.5 | 2015 | `@coroutine` + `yield from` |
| JavaScript | ES2017 | 2017 | `.then().then().catch()` |
| Rust | 1.39 | 2019 | `.and_then().map()` |
| Swift | 5.5 | 2021 | Completion handlers |

Same problem. Same solution. Five languages. Ten years. **Inevitable.**

### Where PyL Fits

PyL is in phase 2: proving that LLM-native syntax has value. `agent` and `infer` are the `async/await` of AI programming — currently bolted on as patterns (system prompt strings, HTTP calls, JSON parsing), waiting to become syntax.
