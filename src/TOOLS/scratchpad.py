
class Scratchpad:
    def __init__(self):
        self.contents = []

    def add(self, label, result):
        self.contents.append(f"[{label}]\n{result}")

    def reset(self):
        self.contents = []

    def build_prompt(self, user_prompt: str):
        scratch = "\n".join(self.contents)
        return f"{user_prompt}\n\n[Scratchpad]\n{scratch}" if scratch else user_prompt
