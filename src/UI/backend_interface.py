from simulated_backend import LanguageAgent

#This file provides an abstraction from the backend logic

class BackendInterface:
    def __init__(self):
        self.agent = LanguageAgent()

    def get_agent_response(self, prompt, file_text="", file_name=""):
        return self.agent.process(prompt, file_text, file_name)
