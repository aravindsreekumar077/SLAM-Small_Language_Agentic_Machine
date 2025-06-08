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