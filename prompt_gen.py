import openai
import json

# Set up your OpenAI API key
openai.api_key = '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'

# Define the path to the large body of text
large_text_file_path = 'C:/Prathamesh/Semester 6/tarp_project/healthcaremagic_dialogue_2.txt'

# Define the path to the output JSONL file for storing prompt completion pairs
output_jsonl_file_path = 'C:/Prathamesh/Semester 6/tarp_project/prompt_completion_pairs.jsonl'

# Load the large body of text
def load_large_text(large_text_file_path):
    with open(large_text_file_path, encoding="utf8") as f:
        large_text = f.read()
    return large_text

# Generate prompt completion pairs from the large text
def generate_prompt_completion_pairs(large_text):
    prompt_completion_pairs = []

    # Split the large text into sentences to use as prompts
    sentences = large_text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # Use the sentence as the prompt
            prompt = sentence
            # Use OpenAI's completions API to generate the completion for the prompt
            completions = openai.Completion.create(
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
                model="text-davinci-002"
            )
            # Extract the generated completion from the API response
            completion = completions.choices[0].text.strip()
            # Create a prompt completion pair
            prompt_completion = {"prompt": prompt, "completion": completion}
            prompt_completion_pairs.append(prompt_completion)

    return prompt_completion_pairs

# Store the prompt completion pairs in a JSONL file
def store_prompt_completion_pairs(prompt_completion_pairs, output_jsonl_file_path):
    with open(output_jsonl_file_path, 'w') as f:
        for prompt_completion in prompt_completion_pairs:
            json.dump(prompt_completion, f)
            f.write('\n')

# Call the function to load the large body of text
large_text = load_large_text(large_text_file_path)

# Call the function to generate prompt completion pairs from the large text
prompt_completion_pairs = generate_prompt_completion_pairs(large_text)

# Call the function to store the prompt completion pairs in a JSONL file
store_prompt_completion_pairs(prompt_completion_pairs, output_jsonl_file_path)
