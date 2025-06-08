#This file defines how to get responses from SLM

class LanguageAgent:        
    def process(self, user_input: str, file_text: str = "", file_name: str = "") -> dict:
        # Reverse only the words in user input. This is done for testing the UI. Will be removed.
        reversed_words = " ".join(user_input.strip().split()[::-1])       
        # Start building the response
        response_parts = []
        if file_text and file_name:
            response_parts.append(f"📁 File received: {file_name}") 
        response_parts.append(f"{reversed_words}") 
        return {"response": "\n".join(response_parts)}

#This file provides an abstraction from the backend logic
class BackendInterface:
    def __init__(self):
        self.agent = LanguageAgent()

    def get_agent_response(self, prompt, file_text="", file_name=""):
        return self.agent.process(prompt, file_text, file_name)


#echoing input


def get_simulated_response(user_input: str) -> dict:
    agent = LanguageAgent()
    return agent.process(user_input)