import ollama

class Agent:
    def __init__(self, prompt: str = ""):
        self._prompt = prompt

    def __call__(self, prompt: str) -> str:
        resp = ollama.chat(
            model="qwen3:8b",
            messages=[
                {"role": "system", "content": self._prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return resp["message"]["content"]

translator = Agent(prompt="You translate to English.")


english=translator("bonjour, monde")
print(english)

