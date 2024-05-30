import json
import requests
from time import sleep
from tqdm import tqdm
from groq import Groq


# Load the JSONL file and process each line
def process_jsonl_file(input_file_path, output_file_path, api_key):
    results = []
    groq_client = Groq(api_key=api_key)
    with open(input_file_path, 'r') as file:
        for line in tqdm(file):
            try:
                data = json.loads(line)
                prompt = data.get("prompt", "")
                if prompt:
                    completion = groq_client.chat.completions.create(
                            model="llama3-8b-8192",
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        )             
                    result = {
                        "instruction": prompt,
                        "output": completion.choices[0].message.content,
                        "generator": "groq_llama3"
                    }
                    results.append(result)
                else:
                    print("No prompt found in line.")
            except json.JSONDecodeError:
                print("Invalid JSON format in line.")
    
    # Write results to the output JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(results, outfile, indent=4)

# Example usage
if __name__ == "__main__":
    input_file_path = "./alpaca_eval_dataset.jsonl"  # Path to your JSONL file
    output_file_path = "./Groq_results/Groq_generations.json"  # Path to your output JSON file
    api_key = ""  # Your API key
    process_jsonl_file(input_file_path, output_file_path, api_key)
