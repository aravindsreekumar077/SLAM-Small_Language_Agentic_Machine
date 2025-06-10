from TOOLS.calculator import evaluate_expression
from TOOLS.json_formatter import format_json_from_text
from TOOLS.translator import translate_en_to_fr
from TOOLS.scratchpad import Scratchpad

class BackendInterface:
    def __init__(self):
        self.scratchpad = Scratchpad()
    def get_agent_response(self, prompt, file_text="", file_name=""):
        lowered = prompt.lower().strip()

        # Tool 1: JSON
        if "format this" in lowered:
            raw_json = prompt.split("format this", 1)[-1].strip()
            formatted_json = format_json_from_text(raw_json)
            self.scratchpad.add("Tool: JSON Formatter", formatted_json)
            final = self.scratchpad.build_prompt(prompt)
            return {"response": final}

        # Tool 2: Calculator
        result = evaluate_expression(prompt)
        if result:
            self.scratchpad.add("Tool: Calculator", result)
            final = self.scratchpad.build_prompt(prompt)
            return {"response": final}
        
        if lowered.startswith("translate to french "):
            text = prompt.split(" ", 3)[3]
            return {"response": f"🌐 FR: {translate_en_to_fr(text)}"}

        # Fallback: reverse text
        response_parts = []
        if file_text and file_name:
            response_parts.append(f"📁 File received: {file_name}")
        reversed_text = " ".join(prompt.strip().split()[::-1])
        response_parts.append(reversed_text)
        self.scratchpad.add("Tool: Reverse Text", "\n".join(response_parts))

        final = self.scratchpad.build_prompt(prompt)
        return {"response": final}
