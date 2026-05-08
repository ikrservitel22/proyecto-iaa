from transformers import AutoTokenizer, AutoModelForCausalLM

path = "./model"

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

tokenizer.save_pretrained(path)
model.save_pretrained(path)