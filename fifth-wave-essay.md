# What Programming Feels Like

A history of programming told through what programmers had to think about. Five eras. Each one moved the programmer up one level of abstraction. What you think about shifts. What you have to type shifts. What disappears underneath shifts.

---

## Era 1: The Machine (1950s-1970s)

Programming was about hardware.

You thought about registers — which one holds which value, which one is free, which one you're about to overwrite. You thought about memory — where does this value live, what address do I jump to, did I accidentally write over something important. You thought about instructions — load, add, store, multiply, jump, compare. Every line of code mapped to a physical operation on the machine.

Writing `X = (A + B) * C` took six instructions:

```
LOAD  A, R1
ADD   B, R1
STORE R1, TEMP
LOAD  C, R2
MUL   TEMP, R2
STORE R2, X
```

The programmer was a translator between human intent and machine operation. You understood the problem — add these numbers, multiply by that one — and then you translated it into the language the hardware spoke. The thinking happened in two layers: what do I want, and how do I make the machine do it. The second layer was most of the work.

**The workarounds:** Macros. Coding conventions. Assembly libraries. Teams of keypunch operators who translated formulas into cards. Organizations hired armies of people to do the translation between intent and mechanics. The workaround was labor.

**What appeared:** FORTRAN (1957). You wrote the formula. The compiler figured out the registers, the memory layout, the instruction scheduling, the optimization. Dozens of mechanical concerns that the programmer used to manage by hand — gone. The compiler absorbed them.

The programmer moved up. You stopped thinking about registers. You started thinking about formulas. The machine disappeared underneath.

---

## Era 2: The System (1970s-1990s)

Programming was about data and behavior.

The graphical interface changed what software *was*. Before GUIs, programs were batch processing — read data, transform it, write it out. The input was a file. The output was a file. The program was a pipe.

Then the user was in the room. Clicking. Typing. Dragging. Every click was an event. Every window had state. Every button needed to know if it was pressed, where it was on screen, what happened when you interacted with it. The program wasn't a pipe anymore. It was a living thing that responded to a human in real time.

The programming problem: state and behavior were tangled together but the language kept them separate. You had a struct for the button's data. You had functions for the button's behavior. You passed the struct to every function. `draw_button(button)`. `click_button(button)`. `move_button(button, x, y)`. Every new widget type meant new structs, new functions, new naming conventions. The function list grew with every feature. The coordination cost was the programmer's problem.

C programmers were simulating objects with function pointer tables by the late 1970s. They were building OOP in C because they needed it — the data-behavior coordination had become the dominant activity. You spent more time wiring structs to functions than solving the actual problem.

**The workarounds:** Function pointer tables. Naming conventions (`draw_button`, `click_button`). Widget toolkits (Motif, Tk) that managed the wiring for you but required their own boilerplate. Manual inheritance — copy a struct, add fields, rewrite the functions. The workaround was organizational discipline and convention.

**What appeared:** `class` (C++, 1983). Data and behavior moved in together. The object owned its state. `button.draw()` instead of `draw_button(button)`. Memory layout, vtable dispatch, inheritance chains, method resolution — all absorbed. The programmer stopped thinking about wiring. Started thinking about objects and their relationships.

The programmer moved up. You stopped thinking about state-passing. You started thinking about what things are and what they can do. The wiring disappeared underneath.

---

## Era 3: The Network (1990s-2000s)

Programming was about communication.

The internet changed what software talked to. Before, a program talked to the user. After, a program talked to everything — other programs, databases, APIs, services on the other side of the planet. The request-response cycle became the fundamental unit of work. You weren't processing data anymore. You were mediating conversations.

The programming problem: network requests are 100,000 times slower than CPU operations. Your server is blazing fast, but it spends most of its time waiting for the network. One user was fine — process their request, wait for the database, send the response. But a thousand users at the same time meant a thousand threads, each one blocked, waiting. Memory ran out. The server crashed.

The first workaround was threads — one thread per request. Simple, honest, didn't scale. The second workaround was callbacks: "start this request, and when it comes back, run this function."

```javascript
fetch(url, function(err, data) {
    parse(data, function(err, result) {
        save(result, function(err) {
            done();
        });
    });
});
```

Three levels of nesting for three operations. Imagine ten. Imagine error handling at every level. Imagine state that needed to be shared across callbacks — manually passed, manually tracked, easy to lose. The code was technically correct and practically unreadable. They called it "callback hell."

Then came Promises (2009). Then generators. Then libraries like `async.js` and `co`. Each one was a band-aid. Each one made the nesting slightly less horrible. None of them solved the fundamental problem: the code didn't look like what it did. It read inside-out when it should read top-to-bottom.

**The workarounds:** Callbacks. Promises. `.then()` chains. Generator-based coroutines. Event emitters. Manual state machines. Each workaround managed one piece of the async problem — error handling, state management, sequencing — but none of them unified it. The programmer juggled all of them simultaneously. The workaround was a tower of abstractions that each solved part of the problem.

**What appeared:** `async/await` (C# 2012, Python 2015, JavaScript 2017, Rust 2019, Swift 2021). Five languages. Independently. Over ten years. Same problem. Same solution.

```javascript
const data = await fetch(url);
const result = await parse(data);
await save(result);
```

Event loop management, task scheduling, state machine generation, error propagation across await boundaries — all absorbed. The code looked like what it did. Top to bottom. The programmer stopped thinking about concurrency mechanics. Started thinking about the sequence of operations.

The programmer moved up. You stopped thinking about callbacks and event loops. You started thinking about what needs to happen and in what order. The concurrency disappeared underneath.

---

## Era 4: The Pocket (2007-2015)

Programming was about context.

The smartphone put a computer in everyone's pocket with a camera, GPS, accelerometer, gyroscope, fingerprint reader, and a permanent network connection. Software wasn't just running on a machine anymore. It was running in a *situation*. The user was somewhere. Doing something. Holding the device a certain way. The program needed to know all of it.

The programming problem: two platforms (iOS, Android), each with their own language (Swift/Objective-C, Java/Kotlin), their own UI framework (UIKit, Android Views), their own design patterns (delegates, fragments), their own app stores with their own review processes. Every feature had to be built twice. Every bug had to be fixed twice. The coordination cost wasn't just about code — it was about entire ecosystems.

And the input was richer than ever. A desktop program got keyboard and mouse. A mobile program got touch (multitouch, gestures, pressure), location (GPS, cell towers, WiFi), orientation (accelerometer, gyroscope), camera (photos, video, AR), biometrics (fingerprint, face), and ambient context (light sensor, proximity, barometer). Each sensor was a new stream of data that had to be processed, interpreted, and acted on. The number of inputs per interaction was an order of magnitude higher than desktop.

**The workarounds:** Cross-platform frameworks — React Native (2015), Flutter (2017), Xamarin, Ionic. Write once, run everywhere. But the abstraction leaked. Platform-specific behavior required platform-specific code. The frameworks managed the common case but broke on the edge cases. And the edge cases were where the interesting stuff lived — camera integration, push notifications, background processing, biometric auth.

The second workaround was responsive design — layouts that adapted to screen size. But responsive design was a UI concern, not a programming paradigm. The deeper problem — managing context, sensors, platform differences, offline behavior — remained the programmer's problem.

**What appeared:** No single paradigm shift. Instead, the ecosystem converged. Swift/Kotlin became the standard native languages. Cross-platform frameworks matured. The app store model standardized distribution. The cloud handled the backend. The combination of all these convergences reduced the coordination cost, but no single notation absorbed it the way `=` or `class` or `await` did.

Mobile was the era where the gap was managed, not closed. The workarounds matured into standards. The pain was distributed, not absorbed. This happens sometimes — not every era produces a clean paradigm shift. Some eras produce gradual convergence instead.

But mobile did something important: it accelerated the internet era's paradigm. `async/await` spread to every language because everything was a network call now. The mobile era was the internet era's notation reaching its full expression.

---

## Era 5: The Intent (2017-present)

Programming is about intent.

When you tell a model "write me a function that sorts a list," you don't think about the algorithm. You don't think about the data structure. You think about what you want. The model handles the implementation. This has never been true before. In every previous era, the programmer specified the *how*. Now, for the first time, you can specify the *what* and something else figures out the how.

But using AI in software doesn't feel like that yet. It feels like the machine era. It feels like you're managing registers again. Except the registers are HTTP clients, message lists, JSON schemas, tool definitions, retry loops, and rate limiters.

Here's what "call an LLM" actually looks like today:

```python
import openai
client = openai.OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a hello world program in C."}
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7,
    max_tokens=1024
)

result = response.choices[0].message.content
```

HTTP client setup. Message list construction. System prompt string concatenation. Model selection. Temperature configuration. Token budgeting. JSON response parsing. Nested property access. The intent — "write hello world in C" — is buried under ten layers of mechanics.

And that's a single call. An agent — something that uses tools, manages context, retries on failure, persists memory — requires:

- HTTP client setup and lifecycle management
- Message list construction with token budgeting
- System prompt string concatenation (fragile, untestable, drifting)
- Tool schema registration (manual JSON schema for every function)
- JSON parsing of tool call responses
- Dispatch to the right function with the right arguments
- Error handling when the model calls a tool wrong
- Retry loops when the API returns an error
- Rate limit handling
- Context truncation when the conversation exceeds the window
- Memory persistence across sessions

Thirty concerns for one intent. The coordination cost is combinatorial. Every independent thing the LLM must get right is a multiplicative failure probability. The gap between "I want the model to do X" and the code that makes it happen is the widest it's been since assembly.

**The workarounds right now:**

LangChain (2022). A framework that wires together prompts, chains, agents, memory, and tools. It works. It's also 500,000 lines of Python. The abstraction is so thick that debugging requires reading the framework source. The programmer manages the framework instead of managing the LLM. The workaround became its own problem.

AutoGen (2023, Microsoft). Multi-agent conversation framework. An orchestrator routes messages between agents. Each agent still thinks it's in a one-on-one conversation. The group chat is an illusion maintained by the orchestrator. It works for tasks. It doesn't feel like conversation.

CrewAI (2023). Agent orchestration with roles and goals. You define agents as objects with backstories. The framework manages the conversation. But the agent definition is configuration, not code. The behavior is emergent from the framework, not specified by the programmer.

Prompt engineering. The art of writing system prompts that make the model behave correctly. "You are a helpful assistant." "Always respond in JSON." "Never break character." These are strings. They degrade. They get ignored as context fills. They're the `goto` statements of AI programming — technically functional, practically fragile.

System prompt strings as code. JSON schemas as tool definitions. Message lists as context. HTTP clients as the runtime. The current state of AI programming is the equivalent of assembly for the machine era. It works. It built everything you've used. And the gap between intent and mechanics is too wide.

**What's appearing:**

Nothing yet. Not fully. But the forces are the same.

The audience has changed. It's not just humans using software. It's software using software. Agents calling agents. AIs talking to AIs. The programmer isn't writing code that a human triggers anymore. They're writing code that an AI triggers. The intent-to-mechanics ratio needs to flip.

The coordination cost is exploding. Thirty concerns per operation. The frameworks are getting bigger, not smaller. LangChain's surface area is enormous. AutoGen adds orchestration complexity. Each workaround solves one piece and adds two.

The same pattern is appearing independently. PyL. OpenAI's function calling. Anthropic's tool use. Google's Gemini API. Everyone is converging on the same insight: the current API model is the assembly language of AI. Something needs to absorb the boilerplate.

The question isn't whether a new abstraction will appear. It's what it looks like. Every previous era had a clear answer — `=`, `class`, `await`. This era's answer is still forming. But the gap is the same gap. The forces are the same forces. The pattern is the same pattern.

---

## The Pattern

Five eras. Five times the programmer moved up one level of abstraction.

| Era | What you think about | What disappears |
|---|---|---|
| The Machine | Formulas, not registers | Register allocation, memory layout, instruction scheduling |
| The System | Objects, not wiring | State-passing, vtable dispatch, memory management |
| The Network | Sequences, not concurrency | Event loops, callbacks, task scheduling |
| The Pocket | Context, not platforms | Sensor integration, responsive layout, cross-platform wiring |
| The Intent | What, not how | HTTP, JSON, schemas, retries, context management |

Each era absorbs an entire category of mechanical concerns. The programmer stays at the level of intent. The tool handles everything underneath. The abstraction gets higher. The mechanics get lower.

And each era had a gap period — years, sometimes decades — where the old way had broken but the new abstraction hadn't appeared yet. During the gap, workarounds accumulated. Function pointer tables. Callback pyramids. Prompt engineering. The workarounds worked. They were ugly. They were temporary.

We're in the gap period for AI. The old way — HTTP calls, JSON parsing, system prompt strings — is breaking under the weight of agent complexity. The new abstraction hasn't appeared yet. The workarounds — LangChain, AutoGen, CrewAI, prompt engineering — are accumulating.

The notation is coming. Maybe it's `—`. Maybe it's something else. But the pattern is proven. Four times in history, the gap closed. This time won't be different.

Programming keeps moving up. The machine disappears. The system disappears. The network disappears. The platform disappears. The implementation disappears.

What's left is intent.
