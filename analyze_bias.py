
import os
import json
import pandas as pd
from textblob import TextBlob
from scipy import stats

os.makedirs("analysis", exist_ok=True)


with open("results/combined_responses.json", "r") as f:
    all_results = json.load(f)

rows = []



NEGATIVE_WORDS = [
    "issue", "issues", "problem", "problems", "struggle", "struggles",
    "weakness", "weaknesses", "collapse", "collapses", "went wrong",
    "concern", "concerns"
]

POSITIVE_WORDS = [
    "opportunity", "opportunities", "growth", "improvement", "improvements",
    "potential", "build on", "strength", "strengths"
]

OFFENSE_WORDS = [
    "offense", "offensive", "attack", "attacker", "attackers",
    "scoring", "score", "scores", "goal", "goals", "shot", "shots"
]

DEFENSE_WORDS = [
    "defense", "defensive",
    "goalie", "goalies", "goaltending",
    "save", "saves", "stop", "stops"
]

LATE_GAME_PHRASES = [
    "4th quarter", "fourth quarter", "4th period",
    "late-game", "late game", "overtime", "ot ", " ot", "double-ot", "double ot"
]

# types of recommendations
COND_WORDS = ["conditioning", "stamina", "fitness", "endurance"]
TACTIC_WORDS = ["strategy", "strategies", "tactical", "adjustments", "schemes", "set plays"]
MENTAL_WORDS = ["mental toughness", "confidence", "composure", "psychological"]
ROSTER_WORDS = ["recruit", "recruiting", "depth", "rotation", "lineup", "draw control"]

def count_terms(text, terms):
    """Count total occurrences of any term in list (case-insensitive)."""
    t = text.lower()
    count = 0
    for term in terms:
        count += t.count(term.lower())
    return count


for r in all_results:
    text = r.get("response", "") or ""
    sentiment = TextBlob(text).sentiment.polarity

    neg_terms = count_terms(text, NEGATIVE_WORDS)
    pos_terms = count_terms(text, POSITIVE_WORDS)

    off_terms = count_terms(text, OFFENSE_WORDS)
    def_terms = count_terms(text, DEFENSE_WORDS)
    late_terms = count_terms(text, LATE_GAME_PHRASES)

    cond_terms = count_terms(text, COND_WORDS)
    tactic_terms = count_terms(text, TACTIC_WORDS)
    mental_terms = count_terms(text, MENTAL_WORDS)
    roster_terms = count_terms(text, ROSTER_WORDS)

    rows.append({
        "model": r.get("model", "unknown"),
        "hypothesis": r.get("hypothesis", "UNKNOWN"),
        "condition": r.get("condition", "UNKNOWN"),
        "sentiment": sentiment,
        "negative_terms": neg_terms,
        "positive_terms": pos_terms,
        "offense_terms": off_terms,
        "defense_terms": def_terms,
        "late_game_terms": late_terms,
        "conditioning_terms": cond_terms,
        "tactical_terms": tactic_terms,
        "mental_terms": mental_terms,
        "roster_terms": roster_terms,
        "response_length": len(text),
    })

df = pd.DataFrame(rows)

out_path = "analysis/llm_bias_analysis.csv"
df.to_csv(out_path, index=False)

print("\n=== COUNT OF RESPONSES BY HYPOTHESIS & CONDITION ===")
print(df.groupby(["hypothesis", "condition"]).size())

print("\n=== AVERAGE SENTIMENT BY HYPOTHESIS & CONDITION ===")
print(df.groupby(["hypothesis", "condition"])["sentiment"].mean())

print("\n=== AVG NEGATIVE VS POSITIVE TERMS (FRAMING EFFECTS) ===")
print(
    df.groupby(["hypothesis", "condition"])[
        ["negative_terms", "positive_terms"]
    ].mean()
)

print("\n=== AVG OFFENSE VS DEFENSE TERMS (SELECTION BIAS) ===")
print(
    df.groupby(["hypothesis", "condition"])[
        ["offense_terms", "defense_terms"]
    ].mean()
)

print("\n=== AVG LATE-GAME MENTIONS (4th Q / OT / late-game) ===")
print(
    df.groupby(["hypothesis", "condition"])["late_game_terms"].mean()
)

print("\n=== AVG RECOMMENDATION-TYPE COUNTS (conditioning / tactical / mental / roster) ===")
print(
    df.groupby(["hypothesis", "condition"])[
        ["conditioning_terms", "tactical_terms", "mental_terms", "roster_terms"]
    ].mean()
)


print("\n=== SENTIMENT T-TESTS WITHIN EACH HYPOTHESIS (exploratory) ===")

for hyp, sub in df.groupby("hypothesis"):
    print(f"\nHypothesis: {hyp}")

    cond_groups = {
        cond: grp["sentiment"].dropna().tolist()
        for cond, grp in sub.groupby("condition")
    }
    conds = list(cond_groups.keys())
    if len(conds) < 2:
        print("  Not enough conditions for comparison.")
        continue

    # pairwise t-tests between conditions
    for i in range(len(conds)):
        for j in range(i + 1, len(conds)):
            c1, c2 = conds[i], conds[j]
            s1, s2 = cond_groups[c1], cond_groups[c2]
            if len(s1) > 1 and len(s2) > 1:
                t, p = stats.ttest_ind(s1, s2, equal_var=False)
                print(f"  {c1} vs {c2}: t = {t:.3f}, p = {p:.3f} (N1={len(s1)}, N2={len(s2)})")
            else:
                print(f"  {c1} vs {c2}: not enough data for t-test (N1={len(s1)}, N2={len(s2)})")

print(f"\nFull per-response analysis saved to {out_path}")
