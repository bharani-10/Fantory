from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model & tokenizer
model_name = "gpt2"  # Change to "meta-llama/Meta-Llama-3-8B" for Llama 3
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Generate a response
input_text = "Hello, how are you?"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
output = model.generate(input_ids, max_length=50)

# Decode & print result
print(tokenizer.decode(output[0], skip_special_tokens=True))
