import openai
import json

# Set up your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

# Define the path to the JSONL file containing the prompt completion pairs
jsonl_file_path = 'prompt_completion_pairs.jsonl'

# Load the prompt completion pairs from the JSONL file
def load_prompt_completion_pairs(jsonl_file_path):
    prompt_completion_pairs = []
    with open(jsonl_file_path, 'r') as f:
        for line in f:
            prompt_completion_pairs.append(json.loads(line))
    return prompt_completion_pairs

# Fine-tune ChatGPT using the loaded prompt completion pairs
def fine_tune_chatgpt(prompt_completion_pairs):
    model_engine = "text-davinci-002"
    prompts = []
    completions = []

    # Extract prompts and completions from the prompt_completion_pairs
    for pair in prompt_completion_pairs:
        prompts.append(pair["prompt"])
        completions.append(pair["completion"])

    prompt = "\n".join(prompts)
    completion = "\n".join(completions)
    prompt_completion = f"{prompt}\n{completion}"

    # Fine-tune the model
    fine_tuned_model = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_completion,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return fine_tuned_model

# Call the function to load prompt completion pairs from the JSONL file
prompt_completion_pairs = load_prompt_completion_pairs(jsonl_file_path)

# Call the function to fine-tune ChatGPT
fine_tuned_model = fine_tune_chatgpt(prompt_completion_pairs)

# Extract the fine-tuned model's ID for future use
fine_tuned_model_id = fine_tuned_model['id']

# Use the fine-tuned model to generate responses
def generate_response(user_message):
    model_engine = "text-davinci-002"
    completions = []

    # Append user message as prompt
    completions.append(f"User: {user_message}")

    # Append the fine-tuned model ID as continuation
    completions.append(f"ChatGPT: ")

    prompt_completion = "\n".join(completions)

    # Generate response using fine-tuned model
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_completion,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response['choices'][0]['text'].strip()

# Example usage: Generate a response to a user message
user_message = "What's your name?"
response = generate_response(user_message)
print(response)