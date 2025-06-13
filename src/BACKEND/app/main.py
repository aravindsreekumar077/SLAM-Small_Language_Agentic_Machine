##SLAM-Backend##

from pydantic import BaseModel
import os
import uuid
import cv2
import pytesseract
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

'''
from transformers import T5Tokenizer, T5ForConditionalGeneration
from peft import PeftModel, PeftConfig
import torch

peft_model_id = "/kaggle/input/t5/pytorch/default/1/flan-t5-math-lora-saved"

# 1. Load LoRA config
config = PeftConfig.from_pretrained(peft_model_id)

# 2. Load base model (T5, for example)
base_model = T5ForConditionalGeneration.from_pretrained(config.base_model_name_or_path)

# 3. Load adapter weights into base model
model = PeftModel.from_pretrained(base_model, peft_model_id)

# 4. Load tokenizer
tokenizer = T5Tokenizer.from_pretrained(peft_model_id)
model = model.to(device)
'''


UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class Query(BaseModel):
    input_text: str

@app.get("/ping")
def ping():
    return {"message": "Hi , SLAM backend is up and running"}


@app.post("/OCR")
async def upload_image(image: UploadFile = File(...)):
    try:
        # Save the uploaded image
        filename = f"{uuid.uuid4().hex}.jpg"
        input_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(input_path, "wb") as f:
            f.write(await image.read())

        # Load and process the image
        img = cv2.imread(input_path)
        if img is None:
            raise HTTPException(status_code=400, detail="Failed to read image")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh, config=custom_config)

        rows = text.strip().split('\n')
        output_filename = f"{uuid.uuid4().hex}.txt"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        with open(output_path, "w") as f:
            for item in rows:
                f.write(f"{item}\n")

        return FileResponse(path=output_path, filename=output_filename, media_type='text/plain')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Inference code for model
'''
@app.post("/infer")
async def generate_output(query: Query):


    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    question = "what is ninety eight times fifteen?"
    inputs = tokenizer(question, return_tensors="pt").to(device)
    outputs = model.generate(input_ids=inputs.input_ids, max_length=50)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": answer}
'''