# classifier.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model and tokenizer
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

labels = [
    "Booking Issue",
    "Subscription Plan Issue",
    "Payment Issue",
    "Driver No Show Issue",
    "Ride Delay Issue",
    "Route Issue",
    "Account Profile Issue",
    "Customer Support Issue",
    "Junk Message"
]

def build_prompt(message):
    return f"""Classify the following user message into one of the categories: 
{', '.join(labels)}.

Message:
\"{message}\"

Only output the exact label name."""

def classify_message(message):
    prompt = build_prompt(message)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = model.generate(**inputs, max_length=32)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result.strip()