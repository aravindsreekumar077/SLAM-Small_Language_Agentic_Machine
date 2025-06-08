from agent import LanguageAgent

# This file acts as the backend logic provider

agent = LanguageAgent()

def get_simulated_response(user_input: str) -> dict:
    return agent.process(user_input)
