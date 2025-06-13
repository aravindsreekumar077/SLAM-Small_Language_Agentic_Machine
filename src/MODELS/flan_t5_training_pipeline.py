import random
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

# Enhanced dataset class with better tokenization
class MathDataset(Dataset):
    def __init__(self, data, tokenizer, max_input_length=128, max_target_length=32):
        self.data = data
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        source, target = self.data[idx]

        # Better preprocessing
        source = f"Answer this math problem: {source}"

        # Tokenization with proper handling
        input_enc = self.tokenizer(
            source,
            padding="max_length",
            truncation=True,
            max_length=self.max_input_length,
            return_tensors="pt"
        )

        # Handle target with proper tokenization (updated method)
        target_enc = self.tokenizer(
            text_target=target,
            padding="max_length",
            truncation=True,
            max_length=self.max_target_length,
            return_tensors="pt"
        )

        # Replace padding token id with -100 for loss calculation
        labels = target_enc.input_ids.squeeze()
        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            "input_ids": input_enc.input_ids.squeeze(),
            "attention_mask": input_enc.attention_mask.squeeze(),
            "labels": labels,
        }

# Load and split data
df1 = pd.read_csv("/kaggle/input/mathdata/flan_t5_math_dataset_words_50k.csv")
df2 = pd.read_csv("/kaggle/input/input-actuall5/final_dataset.csv")
df2 = df2.rename(columns={"Input": "input", "Actual": "target"})
combined_df = pd.concat([df1, df2], ignore_index=True)

data = list(zip("Simplify this prompt: "+ combined_df["input"], combined_df["target"]))




# Train/validation split
train_data, val_data = train_test_split(data, test_size=0.1, random_state=42)

# Model and tokenizer
model_name = "google/flan-t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Ensure model is in training mode and enable gradient computation
model.train()
model.config.use_cache = False  # Disable cache for training

# Enhanced LoRA config
peft_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,
    inference_mode=False,
    r=16,  # Increased rank for better capacity
    lora_alpha=32,  # Increased alpha
    lora_dropout=0.1,
    target_modules=["q", "v"]  # More comprehensive targeting
)

model = get_peft_model(model, peft_config)

# Enable gradient computation for LoRA parameters
for name, param in model.named_parameters():
    if 'lora' in name:
        param.requires_grad = True

# Print trainable parameters
def print_trainable_parameters(model):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(f"Trainable params: {trainable_params:,} || All params: {all_param:,} || "
          f"Trainable%: {100 * trainable_params / all_param:.2f}%")

print_trainable_parameters(model)

# Datasets
train_dataset = MathDataset(train_data, tokenizer)
val_dataset = MathDataset(val_data, tokenizer)

# Enhanced training arguments
training_args = TrainingArguments(
    output_dir="./flan-t5-math-lora-enhanced",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    learning_rate=5e-5,
    warmup_steps=500,
    logging_dir="./logs",
    logging_steps=100,
    eval_steps=300,
    save_steps=900,
    eval_strategy="steps",  # Changed from evaluation_strategy
    save_strategy="steps",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    report_to="none",
    gradient_checkpointing=False,  # Disabled to avoid conflicts with LoRA
    dataloader_pin_memory=True,
    remove_unused_columns=False,
)

# Custom data collator for better batching
def data_collator(features):
    batch = {}
    batch["input_ids"] = torch.stack([f["input_ids"] for f in features])
    batch["attention_mask"] = torch.stack([f["attention_mask"] for f in features])
    batch["labels"] = torch.stack([f["labels"] for f in features])
    return batch

# Trainer with validation
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=data_collator,
)

# Training with progress tracking
print("Starting training...")
trainer.train()

# Save the LoRA adapter
model.save_pretrained("./flan-t5-math-lora-final")


# Gradient analysis function
def analyze_gradients(model, sample_batch):
    """Analyze gradient flow in LoRA layers"""
    model.train()

    # Forward pass
    outputs = model(**sample_batch)
    loss = outputs.loss

    # Backward pass
    loss.backward()

    # Analyze gradients
    lora_gradients = {}
    for name, param in model.named_parameters():
        if param.requires_grad and 'lora' in name:
            if param.grad is not None:
                lora_gradients[name] = {
                    'mean': param.grad.mean().item(),
                    'std': param.grad.std().item(),
                    'max': param.grad.max().item(),
                    'min': param.grad.min().item()
                }

    return lora_gradients

# Example gradient analysis
print("\n=== Gradient Analysis ===")
sample_batch = next(iter(DataLoader(train_dataset, batch_size=2)))
sample_batch = {k: v.to(model.device) if isinstance(v, torch.Tensor) else v
                for k, v in sample_batch.items()}

gradients = analyze_gradients(model, sample_batch)
for name, stats in gradients.items():
    print(f"{name}: mean={stats['mean']:.6f}, std={stats['std']:.6f}")