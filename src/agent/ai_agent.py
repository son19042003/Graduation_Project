import requests
import os

API_KEY = "AIzaSyBKQ5J3HglHv-OhhkQei7Bo_bpZ8i1S5pM"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

def generate_testcase_from_prompt(prompt: str) -> str:
    payload = {
        "contents": [{"parts": [{'text': prompt}]}]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f'[ERROR] Failed for prompt: "{prompt}"')
        print(e)
        return ""

def main():
    script_dir = os.path.dirname(__file__)
    prompt_file = os.path.join(script_dir, 'prompt.txt')

    if not os.path.exists(prompt_file):
        print(f'[ERROR] {prompt_file} not found!')
        return
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]

    for idx, prompt in enumerate(prompts, start=1):
        print('f\n=== Test Case #{idx} for Prompt ===')
        print(f'>>> {prompt}\n')
        test_case = generate_testcase_from_prompt(prompt)
        print(test_case)

        filename = os.path.join(script_dir, f"generated_testcase_{idx}.py")
        with open(filename, "w", encoding="utf-8") as out_file:
            out_file.write("# Generated from prompt:\n")
            out_file.write(f"# {prompt}\n\n")
            out_file.write(test_case)
        print(f"[SAVED] → {filename}")

if __name__ == "__main__":
    main()