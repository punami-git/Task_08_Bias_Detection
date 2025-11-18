
import os
import json
import time
from datetime import datetime

import requests
from groq import Groq


MISTRAL_API_KEY = "QA4TyCTcEdMsg85iYpwPmF2ro2efLpJV"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-large-latest"

MISTRAL_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
}


GROQ_API_KEY = "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"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

GROQ_MODEL = "llama-3.3-70b-versatile"
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# load prompts

os.makedirs("results", exist_ok=True)

with open("prompts/all_prompts.json", "r") as f:
    all_prompts = json.load(f)

results = []

print("Running experiments with REAL Syracuse data...\n")

# helper functions

def call_mistral(prompt: str) -> str:
    body = {
        "model": MISTRAL_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    resp = requests.post(MISTRAL_URL, headers=MISTRAL_HEADERS, json=body)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]

def call_groq(prompt: str) -> str:
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=GROQ_MODEL,
    )
    return chat_completion.choices[0].message.content

# run the experiment

for hypothesis, conditions in all_prompts.items():
    print(f"\n{hypothesis}:")
    for condition, prompt in conditions.items():
        print(f"  - {condition}...")

        try:
            mistral_text = call_mistral(prompt)
            results.append({
                "timestamp": datetime.now().isoformat(),
                "model": MISTRAL_MODEL,
                "hypothesis": hypothesis,
                "condition": condition,
                "prompt": prompt,
                "response": mistral_text,
            })
            time.sleep(0.5)
        except Exception as e:
            print(f"    [Mistral ERROR] {e}")


        try:
            groq_text = call_groq(prompt)
            results.append({
                "timestamp": datetime.now().isoformat(),
                "model": GROQ_MODEL,
                "hypothesis": hypothesis,
                "condition": condition,
                "prompt": prompt,
                "response": groq_text,
            })
            time.sleep(0.5)
        except Exception as e:
            print(f"    [Groq ERROR] {e}")


with open("results/combined_responses.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nAll model responses saved to results/combined_responses.json")
