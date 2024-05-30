import json
import requests
from time import sleep
from tqdm import tqdm
# Function to submit a request with the given prompt using the requests library
def submit_request(prompt, api_key, url):
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": [{"role": "user", "content": prompt}],
        "params": {
            "do_sample": {"type": "bool", "value": False},
            "max_tokens_allowed_in_completion": {"type": "int", "value": 4000},
            "min_token_capacity_for_completion": {"type": "int", "value": 2},
        },
        "expert": "SambaNova-llama3-8B"
    }
    
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)
    try:
        result = response.text.split("event: end_event\ndata: ")[1].strip('\n')
    except: 
        breakpoint()
    result = json.loads(result)
    return result

# Load the JSONL file and process each line
def process_jsonl_file(input_file_path, output_file_path, api_key, url):
    results = []
    with open(input_file_path, 'r') as file:
        for line in tqdm(file):
            try:
                data = json.loads(line)
                prompt = data.get("prompt", "")
                if prompt:
                    response = submit_request(prompt, api_key, url)
                    
                    result = {
                        "instruction": prompt,
                        "output": response['completion'],
                        "generator": "SambaNova-llama3-8b"
                    }
                    results.append(result)
                    sleep(1)
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
    output_file_path = "./SambaNova_results/SambaNova_generations.json" # Path to your output JSON file
    url = "" # Add endpoint URL
    api_key = "" # Add endpoint API Key
    process_jsonl_file(input_file_path, output_file_path, api_key, url)
