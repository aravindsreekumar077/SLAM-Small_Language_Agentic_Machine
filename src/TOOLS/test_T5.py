from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

class flanT5:
    def __init__(self):
        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5")
        
    def get_T5_resp(self, prompt):
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        return model.generate(input_ids)
