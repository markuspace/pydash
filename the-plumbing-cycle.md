# The Plumbing Cycle

Every era in programming follows the same lifecycle. Things start clean. Then the world changes. Then the plumbing grows — workarounds, conventions, frameworks, band-aids — as programmers try to manage the new reality with old tools. Then a new abstraction appears and absorbs all of it. Clean again.

This has happened five times. The fifth time is happening right now.

---

## Era 1: The Machine

**The clean start:**

In the beginning, programming was direct. One machine. One operator. One program at a time. You loaded a deck of punch cards, the machine processed them, you got a printout. The programmer specified exactly what the machine should do — load this register, add that value, store the result. Every instruction mapped to a physical operation. There was no abstraction. There was no plumbing. There was just the machine and the person telling it what to do.

For the programs of the era — calculating ballistics, breaking codes, simulating nuclear reactions — this was enough. The programs were short. The operations were specific. The machine was the abstraction.

**What changed:**

Science grew. The Cold War poured money into computing. Universities got machines. Physicists, engineers, and mathematicians needed to program — but they weren't assembly programmers. They were scientists who thought in formulas. `X = (A + B) * C` was how they thought. `LOAD A, R1; ADD B, R1; STORE R1, TEMP; LOAD C, R2; MUL TEMP, R2; STORE R2, X` was how the machine thought. The gap between those two was enormous, and it was growing with every new scientific application.

Programs were getting longer too. Hundreds of lines became thousands. Managing registers across a large program — which register holds which value, which one is free, which one did I just overwrite — became the dominant activity. The programmer spent more time managing the machine than solving the problem.

**The plumbing grew:**

Assembly macros — reusable instruction sequences that pretended to be higher-level operations. Coding conventions — naming schemes for registers, standard patterns for common operations. Libraries of subroutines — shared code that handled common tasks, but required manual linking and calling conventions.

Organizations hired armies of keypunch operators — people whose entire job was translating formulas into punch cards. The workaround was labor. More people doing the translation between intent and mechanics.

Some programmers tried to build higher-level tools. Early attempts at automatic programming — having the computer generate its own code — were dismissed as impossible. "No compiler could match hand-written assembly." The plumbing was accepted as the cost of computing.

**What eliminated it:**

FORTRAN (1957). John Backus at IBM built a compiler that translated formulas into assembly. You wrote `X = (A + B) * C`. The compiler figured out register allocation, memory layout, instruction scheduling, optimization. Dozens of mechanical concerns that the programmer managed by hand — absorbed.

Nobody believed it would work. Assembly programmers were certain they could beat any compiler. They were wrong. FORTRAN-generated code matched hand-written assembly, and in some cases beat it, because the compiler could optimize across the entire program in ways no human could.

The programmer moved up. You stopped thinking about registers and started thinking about formulas. The machine disappeared underneath. Assembly didn't die — it found its niche in bootloaders, device drivers, and performance-critical inner loops. But for most programming, it was over.

---

## Era 2: The System

**The clean start:**

Procedural programming was clean. A program was a sequence of steps. Read input. Process it. Write output. The program was a pipe. Data flowed through it. Functions transformed it. The programmer specified the order of operations, and the machine executed them.

For the programs of the era — business applications, scientific computing, system utilities — this was enough. The input was a file. The output was a file. The program ran and finished. No persistent state. No user interaction. Just data transformation.

**What changed:**

The graphical interface. Xerox PARC invented it in the 1970s — windows, icons, menus, a mouse. Apple put it on the Macintosh in 1984. Microsoft followed with Windows in 1985. Suddenly the program wasn't a pipe. It was a living thing that sat on the screen and waited for a human to interact with it.

Every window had state — its position, its size, its contents. Every button had state — is it pressed? Is it enabled? Is it focused? Every menu had state — which items are available? Which one is selected? And every one of these things had behavior — what happens when you click it? What happens when you drag it? What happens when you resize the window it's in?

State and behavior were everywhere, and they were tangled together. A button's data (position, size, pressed state) and its behavior (draw yourself, handle a click, respond to hover) were conceptually the same thing. But the language kept them separate. Structs here. Functions there. Connected by convention.

**The plumbing grew:**

Function pointer tables. C programmers in the late 1970s were building "objects" by hand — structs with function pointers, manually wired together. You'd create a `Button` struct, then manually assign function pointers to it: `button->draw = &draw_button; button->click = &handle_click`. Every new type meant new wiring. Every new function meant updating every type that needed it.

Naming conventions. `draw_button()`, `click_button()`, `move_button()`. The function name encoded the type it operated on. Adding a new widget type meant adding new functions for every operation. The function list grew with every feature. The naming convention was the only thing keeping it organized.

Widget toolkits. Motif, Tk, the Mac Toolbox — frameworks that managed the state-behavior wiring for you. But they required their own boilerplate. Callback registration. Resource files. Event tables. The toolkit managed the wiring, but the programmer still had to configure it. And every toolkit had its own configuration language, its own conventions, its own way of doing things.

Manual inheritance. If you wanted a "RoundRectButton" that behaved like a "Button" but drew differently, you copied the struct, added fields, rewrote the drawing function, and rewired the function pointers. There was no `extends`. There was copy-paste and pray.

**What eliminated it:**

`class` (C++, 1983). Data and behavior moved in together. The object owned its state. `button.draw()` instead of `draw_button(button)`. Inheritance was built in — `class RoundRectButton extends Button` gave you all the parent's behavior for free. Virtual dispatch meant the right function was called automatically based on the object's actual type.

Under the hood, the compiler did everything the programmer used to do manually — memory layout, vtable construction, inheritance chain resolution, method dispatch. Dozens of mechanical concerns absorbed.

By the 1990s, every computer science curriculum taught OOP as the default. Java (1995) made it the mainstream. The programmer moved up. You stopped thinking about wiring structs to functions and started thinking about what things are and what they can do. The wiring disappeared underneath.

---

## Era 3: The Network

**The clean start:**

Object-oriented programming was clean. Programs modeled the world as interacting objects. You created a `User`, a `Document`, a `Printer`. They sent messages to each other. The program ran, the user interacted, the objects handled it. One user. One session. One program. Top to bottom.

**What changed:**

The internet. The web. Software stopped running on one machine and started running on all of them. A web server wasn't handling one user — it was handling thousands, simultaneously, from all over the world. Each request was an event that came from outside. The program didn't control the order. The world did.

And network requests were slow. Absurdly slow. A CPU operation takes nanoseconds. A network request takes milliseconds — sometimes seconds. Your blazing-fast server spent most of its time waiting. Waiting for the database. Waiting for the API. Waiting for the user's browser. The CPU was idle, waiting for the network, while thousands of other requests piled up.

The old model — do one thing, wait, do the next thing — couldn't handle this. You needed to do many things at once. Not because the program was complex, but because the world was concurrent.

**The plumbing grew:**

Threads. One thread per request. Simple, honest, and it worked — for dozens of connections. For thousands, the memory ran out. Each thread needed its own stack. A thousand threads meant a thousand stacks. The server crashed.

Callbacks. "Start this request, and when it comes back, run this function." The program didn't block. It registered a handler and moved on. But callbacks nested inside callbacks created unreadable code:

```javascript
getUser(userId, function(err, user) {
    getOrders(user.id, function(err, orders) {
        getOrderDetails(orders[0].id, function(err, details) {
            getShippingStatus(details.trackingId, function(err, status) {
                render(user, orders, details, status);
            });
        });
    });
});
```

Four levels deep for four operations. Error handling at every level. State passed manually. The code read inside-out.

Promises (2009). A better way to chain async operations. `getUser(userId).then(user => getOrders(user.id)).then(orders => ...)`. Less nesting. But `.then().then().then()` chains were still awkward. Error handling was `.catch()` at the end — unless you needed to handle errors at specific points, then it got complicated again.

Generators. `yield` pauses a function and resumes it later. Libraries like `co` used generators to simulate synchronous-looking async code. It worked. It was clever. Nobody understood how it worked.

Event emitters. `server.on('request', handler)`. The program was a set of handlers for events. Clean for simple cases. Unmanageable for complex ones — who emits what, when, in what order, with what data?

`async.js`. A library that managed parallel and sequential async operations. `async.waterfall()`, `async.parallel()`, `async.eachSeries()`. Each function managed one pattern. You picked the right one for your situation. The programmer juggled the library instead of juggling callbacks. The plumbing moved, it didn't disappear.

The programmer was drowning in coordination. Callbacks, promises, generators, event emitters, async libraries — all solving pieces of the same problem. None of them unified it. The code didn't look like what it did.

**What eliminated it:**

`async/await` (C# 2012, Python 2015, JavaScript 2017, Rust 2019, Swift 2021). Five languages. Independently. Over ten years.

```javascript
const user = await getUser(userId);
const orders = await getOrders(user.id);
const details = await getOrderDetails(orders[0].id);
const status = await getShippingStatus(details.trackingId);
render(user, orders, details, status);
```

Top to bottom. Error handling with `try/catch` — the same way synchronous code worked. Under the hood, the compiler generated a state machine. The event loop, task scheduling, promise chaining — all absorbed. The programmer wrote sequential-looking code that handled concurrent operations.

The programmer moved up. You stopped thinking about callbacks and event loops. You started thinking about what needs to happen and in what order. The concurrency disappeared underneath.

---

## Era 4: The Pocket

**The clean start:**

`async/await` was clean. Code read top-to-bottom. The network was handled. Servers scaled. The web was mature.

**What changed:**

The iPhone (2007). Android (2008). The computer went from the desk to the pocket. Touch interfaces replaced mice. GPS, camera, accelerometer, gyroscope, fingerprint reader — sensors that gave software inputs it never had before. The program wasn't running on a machine anymore. It was running in a *situation*.

And two platforms. iOS and Android. Different languages (Swift/Objective-C, Java/Kotlin). Different UI frameworks (UIKit, Android Views). Different design patterns (delegates, fragments). Different app stores with different review processes. Every feature built twice. Every bug fixed twice.

**The plumbing grew:**

Cross-platform frameworks. React Native (2015), Flutter (2017), Xamarin, Ionic — write once, run everywhere. But the abstraction leaked. Platform-specific behavior required platform-specific code. Push notifications worked differently on each platform. Camera integration was different. Background processing was different. Biometric auth was different. The frameworks managed the common case but broke on the edge cases — and the edge cases were where the interesting stuff lived.

Responsive design. Layouts that adapted to screen size. But responsive design was a UI concern, not a programming paradigm. The deeper problem — managing sensors, platform differences, offline behavior, background sync — remained the programmer's problem.

Plugin ecosystems. Cordova plugins, React Native modules, Flutter packages — each one wrapping a platform-specific feature in a cross-platform API. Dozens of plugins per app. Each one with its own API, its own bugs, its own maintenance burden. The plumbing was distributed across hundreds of community packages.

Feature flags and A/B testing infrastructure. Mobile apps needed to ship different versions to different users. The codebase became a maze of conditional paths. `if (platform === 'ios') { ... } else { ... }`. The coordination cost wasn't just code — it was entire release pipelines.

**What eliminated it:**

Nothing clean. No single paradigm shift. Instead, the ecosystem converged.

Swift (2014) and Kotlin (2016) became the standard languages for their platforms. The language fragmentation reduced. Cross-platform frameworks matured — not by solving the problem perfectly, but by making the common case good enough. The cloud handled the backend — AWS, Firebase, serverless functions. The app store model standardized distribution.

The combination of all these convergences reduced the pain. But no single abstraction absorbed it the way `=` or `class` or `await` did. Mobile was a convergence era, not a paradigm shift era.

Mobile did one important thing: it accelerated the internet era's paradigm. `async/await` spread to every language because everything was a network call now. The mobile era was the internet era's abstraction reaching its full expression.

---

## Era 5: The Intelligence

**The clean start:**

APIs were clean. You called an endpoint, got a response. REST. JSON. HTTP. The programmer knew exactly what was happening. Request in. Response out. Deterministic. Predictable.

LLM APIs followed the same pattern at first. OpenAI's API (2020) was a simple HTTP call. Send a prompt, get a completion. One request, one response. The programmer set up an HTTP client, constructed a message, parsed the result. A few lines of boilerplate. Manageable.

**What changed:**

Agents. Not one-off calls. Systems that used the LLM as a component in a larger loop. Agents that remembered conversations. Agents that called tools — functions, APIs, shell commands. Agents that managed context — keeping track of what was said, truncating when it got too long, summarizing when it overflowed. Agents that retried on failure. Agents that chained multiple steps together. Agents that worked with other agents.

ChatGPT (November 2022) hit 100 million users in two months. Everyone wanted to build with LLMs. Not just chatbots — agents. Autonomous systems. Code generators. Customer service bots. Research assistants. Writing partners. Each one required tool use, memory, context management, error handling, and orchestration.

The single API call turned into a pipeline. The pipeline turned into a system. The system turned into a platform. And the plumbing grew with every layer.

**The plumbing is growing now:**

HTTP client setup and lifecycle management. OpenAI, Anthropic, Ollama, local models, cloud models — each with its own API, its own authentication, its own rate limits, its own response format. The programmer manages the connection before they can even start thinking about the problem.

Message list construction. System prompt, user message, assistant response, tool calls, tool results — all formatted as a list of role-tagged messages. The programmer manually constructs and manages this list. Truncation when it gets too long. Summarization when it overflows. The context window is a resource the programmer manages by hand.

System prompt string concatenation. "You are a helpful assistant. Always respond in JSON. Never break character. Here are your tools: ..." These are strings. They degrade as context fills. They get ignored when the conversation gets long. They're the `goto` statements of AI programming — technically functional, practically fragile. Prompt engineering has become a discipline. That's a sign the plumbing is too thick.

Tool schema registration. Every function the agent can call needs a JSON schema describing its parameters. The programmer writes the function AND the schema. They're separate documents that can drift apart. The schema is the contract between the model and the code, and the programmer maintains both sides by hand.

JSON parsing of responses. The model returns JSON. The programmer parses it. Extracts the tool calls. Dispatches to the right function. Collects the results. Formats them back into the message list. Sends the updated list back to the model. Repeat until the model stops calling tools.

Retry loops. The API returns an error — rate limited, timeout, server error. The programmer retries with backoff. The model returns malformed JSON. The programmer re-prompts. The model calls a tool with wrong arguments. The programmer handles the error and feeds it back.

Context management. The conversation grows. The context window fills. The programmer truncates — but which messages do you drop? The oldest? The least relevant? How do you decide? Summarize — but the summary loses detail. The programmer manages a resource (context window) that's invisible and unforgiving.

Memory persistence. The agent needs to remember things across sessions. The programmer sets up a database. Stores conversations. Retrieves relevant memories. Decides what's important enough to keep. The memory system is a separate subsystem the programmer builds and maintains.

Multi-agent orchestration. Agents talking to agents. Who speaks next? Who is each message directed at? How do you represent group dynamics in a model trained on one-on-one conversations? The programmer builds an orchestrator that routes messages between agents who each think they're in a two-person conversation.

The frameworks are the workarounds. LangChain (2022) — 500,000 lines of Python that wire together prompts, chains, agents, memory, and tools. It works. Debugging requires reading the framework source. The abstraction is so thick it becomes its own problem.

AutoGen (2023, Microsoft) — multi-agent conversation framework. An orchestrator routes messages between agents. The group chat is an illusion maintained by the orchestrator. It works for tasks. It doesn't feel like conversation.

CrewAI (2023) — agent orchestration with roles and goals. Agents are defined as configuration objects. The behavior is emergent from the framework, not specified by the programmer.

Each framework solves one piece. LangChain solves chains. AutoGen solves multi-agent. CrewAI solves orchestration. None of them solve the fundamental problem: the gap between "I want the model to do X" and the code that makes it happen is enormous.

The programmer is drowning in coordination. HTTP clients, message lists, system prompts, tool schemas, JSON parsing, retry loops, context management, memory persistence, multi-agent routing — thirty concerns for one intent. The frameworks are getting bigger, not smaller. The abstraction is getting thicker, not thinner. The plumbing is growing.

**What will eliminate it:**

Not yet. But the pattern is proven.

The audience has changed. It's not just humans using software. It's software using software. Agents calling agents. The programmer isn't writing code that a human triggers anymore. They're writing code that an AI triggers. The intent-to-mechanics ratio needs to flip.

The coordination cost is exploding. Thirty concerns per operation. Every independent thing the LLM must get right is a multiplicative failure probability. The surface area is too wide. Something needs to absorb it.

The same pattern is converging independently. OpenAI's function calling. Anthropic's tool use. Google's Gemini API. LangChain's expression language. LLM-native syntax experiments like PyL. Everyone is converging on the same insight: the current API model is the assembly language of AI.

Four times in history, the plumbing grew until a new abstraction absorbed it. Registers disappeared under `=`. Wiring disappeared under `class`. Callbacks disappeared under `await`. Platform fragmentation partially disappeared under convergence.

The LLM plumbing will disappear under something. The HTTP, the messages, the schemas, the retries, the context management — all of it will be absorbed. The programmer will stay at the level of intent. The tool will handle everything underneath.

The abstraction is coming.

---

## The Cycle

Clean start → world changes → plumbing grows → abstraction absorbs → clean again.

| Era | Clean start | What changed | Plumbing | What absorbed it |
|---|---|---|---|---|
| Machine | Direct hardware access | Programs grew, scientists needed formulas | Macros, conventions, armies of operators | FORTRAN (compiler) |
| System | Procedural data transformation | GUIs, interactive state + behavior | Function pointer tables, naming conventions, widget toolkits | `class` (encapsulation) |
| Network | Sequential OOP | Internet, concurrent users, network latency | Callbacks, promises, event emitters, async libraries | `await` (structured concurrency) |
| Pocket | Clean async code | Mobile, two platforms, sensors | Cross-platform frameworks, responsive design, plugin ecosystems | Convergence (no single abstraction) |
| Intelligence | Simple API calls | Agents, tools, memory, multi-step | LangChain, AutoGen, CrewAI, prompt engineering | Emerging |

The programmer's experience is always the same:

1. Things start clean. You think about the problem.
2. The world changes. New requirements, new constraints, new complexity.
3. The plumbing grows. Workarounds, conventions, frameworks. You think about the mechanics instead of the problem.
4. The abstraction appears. The mechanics disappear. You think about the problem again.

We're in step 3 for AI. The plumbing is growing. The frameworks are multiplying. The programmer thinks about HTTP, JSON, schemas, retries, context, memory — instead of the problem.

Step 4 is coming. It always does.
