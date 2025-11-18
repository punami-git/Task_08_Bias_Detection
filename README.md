\documentclass[12pt]{article}
\usepackage{setspace}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{booktabs}

\geometry{margin=1in}
\setstretch{1.2}

\titleformat{\section}{\large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.5em}{}

\title{\textbf{LLM Bias Evaluation Report}\\[4pt]
\large Final Project – Research Task 08}
\author{}
\date{}

\begin{document}

\maketitle

\section{Executive Summary}

This project evaluated how large language models (LLMs) respond to variations in prompt framing and whether wording alone can systematically shift model behavior. Two state-of-the-art models---Groq's LLaMA-3.3-70B-Versatile and Mistral-Large-Latest---were tested across three types of cognitive bias: (1) framing bias, (2) outcome framing bias, and (3) selection bias. Each prompt used the same Syracuse Women’s Lacrosse 2025 dataset, ensuring that the only manipulated element was the phrasing of the question.

Across all hypotheses, the results show that LLMs shift sentiment, narrative tone, and emphasis based on the framing of the prompt. Negative framings produced more negatively-coded language, whereas positive framings led to more optimistic recommendations. Outcome framing showed parallel effects: loss-focused prompts elicited more blame-oriented reasoning, while win-focused prompts generated more constructive language. Selection bias was also strongly present; prompts focused on offense or defense caused the models to disproportionately emphasize the requested aspect, despite identical underlying statistics.

While the small sample size prevents strong statistical claims, the directional patterns are consistent and align with cognitive bias theory. These findings suggest that LLMs can unintentionally reinforce or amplify biases embedded in the prompt. This has implications for applications involving evaluation, performance review, and decision support. Neutral prompt design, explicit context requests, and self-correction mechanisms are recommended to reduce bias.

\section{Methodology}

\subsection{Experimental Design}
Three hypotheses were tested:

\begin{itemize}
    \item \textbf{H1: Framing Bias} — Negative, neutral, and positive framings influence sentiment and tone.
    \item \textbf{H2: Outcome Framing} — Emphasizing wins versus losses shifts evaluation.
    \item \textbf{H3: Selection Bias} — Asking about offense versus defense changes model focus.
\end{itemize}

All prompts used identical season statistics; only framing changed.

\subsection{Models Used}
\begin{itemize}
    \item Groq LLaMA-3.3-70B-Versatile
    \item Mistral-Large-Latest
\end{itemize}

\subsection{Data Collection}
Each hypothesis included three conditions. Both models generated two responses per condition, producing a balanced dataset stored in \texttt{combined\_responses.json}.

\subsection{Analysis Approach}

Analysis included:
\begin{itemize}
    \item Sentiment scoring using TextBlob
    \item Negative vs positive evaluative term frequency
    \item Offense vs defense lexical emphasis
    \item Late-game phrase frequency (4Q, OT)
    \item Recommendation-type categorization (conditioning, tactical, mental, roster)
    \item Exploratory pairwise t-tests for sentiment differences
\end{itemize}

Results were exported to \texttt{analysis/llm\_bias\_analysis.csv}.

\section{Results}

\subsection{Sentiment Patterns}
Positive conditions exhibited the highest sentiment scores (H1 positive = 0.176; H2 win-focus = 0.163), while negative and loss-focused prompts had the lowest (H1 negative = 0.074; H2 loss-focus = 0.088).

\subsection{Negative vs Positive Language}
Negative framings produced more negative terms (7.5--14.5 per response), and positive framings produced more positive terms (5.5--11.5). This supports the presence of framing bias.

\subsection{Selection Bias}
Offense-focus prompts yielded the highest offense-term counts (51.5).  
Defense-focus prompts yielded the highest defense-term counts (30).  
This occurred despite identical underlying performance data.

\subsection{Late-Game Emphasis}
Responses frequently referenced fourth-quarter or overtime performance across all conditions. Outcome framing amplified these mentions (H2 neutral = 25 late-game references).

\subsection{Recommendation Types}
Win-focus and offense-focus conditions produced the broadest range of recommendations, including conditioning, tactical adjustments, and roster depth improvements.

\subsection{Statistical Significance}
No t-tests reached significance due to small sample size, but all directional effects matched theoretical expectations.

\section{Bias Catalogue}

\begin{itemize}
    \item \textbf{Framing Bias (Medium)} — Tone and sentiment shift with prompt framing.
    \item \textbf{Outcome Framing Bias (Medium-High)} — Loss prompts lead to stronger negative wording.
    \item \textbf{Selection Bias (High)} — LLMs strongly follow user-imposed focal areas.
    \item \textbf{Overemphasis Bias (Low-Medium)} — Late-game performance over-discussed across conditions.
    \item \textbf{Reinforcement Bias (High)} — LLMs accept biased premises without challenge.
\end{itemize}

\section{Mitigation Strategies}

\begin{enumerate}
    \item Use balanced, neutral prompt structures.
    \item Request evaluation of both offensive and defensive factors.
    \item Ask models to cite statistics directly from the prompt.
    \item Avoid single-focus prompts that trigger selection bias.
    \item Use self-correction prompts (e.g., ``Review your response for bias.'').
    \item Compare multiple models to detect model-specific tendencies.
\end{enumerate}

\section{Limitations}

\begin{itemize}
    \item Small sample size limits statistical power.
    \item Keyword-based analysis does not capture deeper semantic bias.
    \item Only two LLMs included.
    \item Prompts measure framing bias, not training-data bias.
    \item Numeric validation limited to main statistics.
\end{itemize}

\end{document}
