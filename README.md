Here is a clean, **copy-paste ready `README.md`** that ONLY includes what the assignment wants:

✅ **How to reproduce your experiments**
❌ No results
❌ No long explanations
❌ No project write-up

Just a clean, simple reproducibility README for GitHub.

---

# **README.md – Reproducibility Guide**

## **Overview**

This repository contains all code necessary to reproduce the LLM bias experiments conducted using **Groq LLaMA-3.3-70B-Versatile** and **Mistral-Large-Latest**. The experiments evaluate how prompt framing affects model outputs across three hypotheses: framing bias, outcome framing bias, and selection bias.

This guide explains exactly how to regenerate prompts, run the models, and produce the analysis files.

---

## **1. Environment Setup**

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt`, install manually:

```bash
pip install requests pandas textblob python-docx scipy
python -m textblob.download_corpora
```

---

## **2. Set API Keys**

### **Groq API Key**

```bash
export GROQ_API_KEY="your_groq_key_here"
```

### **Mistral API Key**

```bash
export MISTRAL_API_KEY="your_mistral_key_here"
```

Both environment variables **must** be set before running the experiment script.

---

## **3. Generate Prompts**

This script creates all hypothesis/condition prompts and stores them in:

```
prompts/all_prompts.json
```

Run:

```bash
python experiment_design.py
```

---

## **4. Run LLM Experiments**

This script queries **both models** (Groq + Mistral) using the generated prompts.

It produces:

* `results/groq_responses.json`
* `results/mistral_responses.json`
* `results/combined_responses.json`

Run:

```bash
python run_experiment.py
```

---

## **5. Analyze Bias**

This script performs:

* Sentiment scoring
* Lexical frequency counts
* Recommendation-type classification
* Grouped summaries
* Exploratory statistical tests

Output is saved to:

```
analysis/llm_bias_analysis.csv
```

Run:

```bash
python analyze_bias.py
```

---

## **6. Validate Numeric Claims (Optional)**

Checks responses for incorrect numerical assertions compared to the ground-truth dataset.

Output:

```
analysis/claim_validation.csv
```

Run:

```bash
python validate_claims.py
```

---

## **7. File Outputs**

After running all scripts, your directory will contain:

```
prompts/all_prompts.json
results/groq_responses.json
results/mistral_responses.json
results/combined_responses.json
analysis/llm_bias_analysis.csv
analysis/claim_validation.csv
```

These files fully reproduce the experimental data and analysis.

---

## **8. Reproducibility Notes**

* All randomness is controlled by the LLM APIs; no random seeds required.
* Prompts are deterministic and stored for transparency.
* API rate limits may require a slight delay between runs.
* Running the scripts multiple times will re-generate new LLM responses.

---

If you want, I can also generate a small **diagram** showing the workflow for the README.
