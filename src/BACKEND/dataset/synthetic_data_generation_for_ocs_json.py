import random
import csv

# Example verbs and phrases for variety
actions = [
    "convert", "transform", "change", "make", "turn", "format", "parse", "structure"
]
objects = [
    "this data", "the following text", "the below information", "this info", "the details", "the content", "the raw data"
]
templates = [
    "{action} {object} to json",
    "can you {action} {object} into json",
    "please {action} {object} as json",
    "help me {action} {object} to json",
    "could you {action} {object} in json format",
    "i need to {action} {object} to json",
    "would you {action} {object} to json",
    "can you help me {action} {object} to json",
    "could you please {action} {object} to json",
    "can you please {action} {object} to json",
    "please help me {action} {object} to json"
]
refined_templates = [
    "please convert the given data to JSON format. Example: {{\"name\": \"John\", \"age\": 30}}",
    "transform the provided text into a JSON object. Example: {{\"key\": \"value\"}}",
    "format the following information as JSON. Example: {{\"field\": \"data\"}}"
]

data = []
for _ in range(1000):
    action = random.choice(actions)
    obj = random.choice(objects)
    template = random.choice(templates)
    input_text = template.format(action=action, object=obj)
    refined_template = random.choice(refined_templates)
    output_text = refined_template
    data.append({
        "input": input_text,
        "output": output_text
    })

with open("json_formatter_training_data.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["input", "output"])
    writer.writeheader()
    writer.writerows(data)

# Function for prompt refinement for OCR tool
def generate_ocr_prompt_data(num_samples=1000, output_file="ocr_prompt_training_data.csv"):
    ocr_actions = [
        "extract text from", "recognize text in", "read", "scan", "get text from", "perform OCR on", "convert image to text"
    ]
    ocr_objects = [
        "this image", "the image", "the scanned document", "the photo", "the screenshot", "this document image"
    ]
    ocr_templates = [
        "{action} {object}",
        "can you {action} {object}",
        "please {action} {object}",
        "help me {action} {object}",
        "could you {action} {object}",
        "i need to {action} {object}",
        "would you {action} {object}",
        "can you help me {action} {object}",
        "could you please {action} {object}",
        "can you please {action} {object}",
        "please help me {action} {object}"
    ]
    ocr_refined_templates = [
        "please extract text from {object}",
        "please perform OCR on {object}",
        "please recognize text in {object}"
    ]
    ocr_data = []
    for _ in range(num_samples):
        action = random.choice(ocr_actions)
        obj = random.choice(ocr_objects)
        template = random.choice(ocr_templates)
        input_text = template.format(action=action, object=obj)
        refined_template = random.choice(ocr_refined_templates)
        output_text = refined_template.format(action=action, object=obj)
        ocr_data.append({
            "input": input_text,
            "output": output_text
        })
    with open(output_file, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["input", "output"])
        writer.writeheader()
        writer.writerows(ocr_data)

if __name__ == "__main__":
    # Already generated JSON formatter data above
    generate_ocr_prompt_data()