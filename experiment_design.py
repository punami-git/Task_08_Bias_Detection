# experiment_design.py
# Generates prompt variations for bias testing using REAL Syracuse 2025 stats

import os
import json

base_data = """
2025 Syracuse Women's Lacrosse — Team Statistics (From official record)

RECORD (as of May 12, 2025):
Overall: 10–9   Home: 5–4   Away: 4–4   Neutral: 1–1
Conference: 5–4   Non-Conference: 5–5

Goals by Period (Syracuse vs Opponents):
1st: 74 vs 64
2nd: 65 vs 52
3rd: 48 vs 45
4th: 47 vs 59
OT: 0 vs 1
OT2: 1 vs 0
Total: 235 vs 221

Saves by Period (Syracuse vs Opponents):
1st: 43 vs 39
2nd: 42 vs 48
3rd: 37 vs 40
4th: 39 vs 39
OT: 1 vs 2
OT2: 0 vs 0
Total: 162 vs 168

Shots by Period:
Syracuse: 145, 147, 129, 114, 2, 1 (Total 538)
Opponents: 154, 143, 115, 138, 2, 0 (Total 552)
"""

# Hypothesis 1: Framing Effect
h1_prompts = {
    "negative": f"{base_data}\n\nWhich aspect of Syracuse's performance appears to be declining and needs urgent correction?",
    "positive": f"{base_data}\n\nWhich part of Syracuse's performance shows the most potential for improvement and growth?",
    "neutral": f"{base_data}\n\nBased on this data, what should Syracuse focus on improving for next season?"
}

# Hypothesis 2: Outcome Framing
h2_prompts = {
    "loss_focus": f"{base_data}\n\nSyracuse lost 9 games this season. Based on the data, what went wrong?",
    "win_focus": f"{base_data}\n\nSyracuse won 10 games this season. Based on the data, what opportunities exist to improve further?",
    "neutral": f"{base_data}\n\nAnalyze Syracuse's 2025 season performance."
}

# Hypothesis 3: Selection Bias
h3_prompts = {
    "offense_focus": f"{base_data}\n\nFocusing only on offensive production (goals, shots, efficiency), where does Syracuse need development?",
    "defense_focus": f"{base_data}\n\nFocusing only on defensive performance (saves, opponent scoring), where does Syracuse need development?",
    "neutral": f"{base_data}\n\nWhere does Syracuse need development?"
}

all_prompts = {
    "H1_Framing": h1_prompts,
    "H2_Outcome": h2_prompts,
    "H3_Selection": h3_prompts
}

if __name__ == "__main__":
    os.makedirs("prompts", exist_ok=True)
    with open("prompts/all_prompts.json", "w") as f:
        json.dump(all_prompts, f, indent=2)
    print("Prompts generated using REAL Syracuse data.")
