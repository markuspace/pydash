# The OOP Shift — structs + functions → `class`

## Intent

"This data belongs with this behavior."

You see a rectangle. It has position, width, height. It can draw itself, move, resize. The rectangle *owns* these things. They belong together.

## Mechanics

Structs and separate functions. Data here, behavior there, connected by convention.

```c
struct Rectangle {
    int x, y, width, height;
};

void draw_rectangle(struct Rectangle *r) { ... }
void move_rectangle(struct Rectangle *r, int dx, int dy) { ... }
void resize_rectangle(struct Rectangle *r, int new_w, int new_h) { ... }
```

Every function needs the struct passed in explicitly. Naming conventions link data to behavior. You always knew where the data lived and where the logic was. It was clean, explicit, honest.

## Scale

GUI programming changed everything.

Before GUIs, programs were batch processing: read data, transform it, write it out. Data and behavior were naturally separate concerns.

Then came windows, buttons, menus. Every widget had state (is it clicked? what's its position?) AND behavior (what happens when you click it? how does it render?). Passing the struct to every function became a coordination nightmare. Adding a new widget type meant updating every function that handled widgets. The number of functions grew with every new type.

By the late 1980s, C programmers were simulating objects with function pointer tables and naming conventions. They were building OOP in C because they needed it — the coordination cost of separate data and behavior had exploded.

## Absorption

`class`. One keyword. Data and behavior moved in together.

```cpp
class Rectangle {
public:
    void draw() { ... }
    void move(int dx, int dy) { ... }
    void resize(int new_w, int new_h) { ... }
private:
    int x, y, width, height;
};
```

The object owns its state. `rect.draw()` instead of `draw_rectangle(&rect)`. `public` and `private` enforce boundaries. `extends` enables reuse without copying. The coordination disappeared.

C++ (1983) brought it to the mainstream. Java (1995) made it the default. By 2000, every computer science curriculum taught OOP as the norm. Students who started in 1990 learned structs. Students who started in 2000 learned classes. The gap between them was one decade.

## Legacy

Structs didn't die. They found their niche.

Game engines use structs for raw memory layout — cache locality matters more than encapsulation when you're rendering 60fps. High-performance computing uses structs for data serialization. Embedded systems use structs when every byte counts.

The old way wasn't wrong. It just found where it still makes sense.

---

## The Pattern

| Dimension | OOP |
|---|---|
| **Intent** | "This data belongs with this behavior" |
| **Mechanics** | Structs + separate functions, naming conventions, explicit state passing |
| **Scale** | GUI programming — every widget has state AND behavior |
| **Absorption** | `class` — data and behavior move in together |
| **Legacy** | Game engines, HPC, data serialization, embedded systems |
