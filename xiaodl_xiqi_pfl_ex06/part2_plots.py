"""
PCL1 & PfL Exercise 6 - Part 2b:
Creating 5 plots for Emotion Analysis

- Extract data from Excel.
- Filter data for information needed for plots.
- Create at least 5 different plots to visualize emotion analysis results.

Note: With this file you are free to create your own functions
as you see fit to achieve the desired plots.
You can even use the same extraction to create multiple plots,
if the analysis requires the same data but the visualization and following interpretation differ to a reasonable extent.

Author 1 & Matriculation Number: Liu Xiaoduan 23-749-609
Author 2 & Matriculation Number: Qi Xinyan 23-757-511
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

# All the following graphs are based on GPT and Flair sentiment analysis results.
# We consider to also include manual sentiment analysis results but decide not to do so
# as the manual sentiment analysis only covers a small portion of the entire text,
# first of all, too less for the whole dataset, and second, will make each graph too complicated.
# and also the portion of manual sentiment analysis results is not evenly distributed across different acts/scenes/characters,
# which may lead to unbalanced classification or biased interpretations.

# For the sentiment‑development plots (Hamlet and King Claudius) numerical labels were not added 
# because the goal of these visualizations is to highlight overall sentiment trends rather than individual data points. 
# Adding labels to every point would clutter the figure and obscure the temporal pattern.

# All sentiment labels were fully annotated in the dataset; 
# therefore, no missing-value filtering was required.
# Flair sentiment labels were filtered to retain only positive and negative classifications, 
# in line with the binary sentiment framework of the model.

# To visualize sentiment development over narrative progression, 
# categorical GPT sentiment labels (positive, neutral, negative)
# were encoded as numerical values (+1, 0, −1), representing sentiment direction rather than intensity. 
# GPT sentiment labels were used to focus on directional emotional shifts at the narrative level, while Flair scores provide continuous sentiment strength.

# AI Usage for this code file: 
# Copilot for generating original version
# Manual check logic and variable consistency with the project's instructions, for example, clarify sentiment distribution across scenes to Sentiment distribution across SCENES (Flair + GPT)
# ChatGPT for final checking error such as scene standardization and removing non-existent field assumptions

# Color definitions for sentiment
POS_COLOR = "#4CAF50"   # green
NEG_COLOR = "#F44336"   # red
NEU_COLOR = "#2196F3"   # blue

# Read and preprocess data
def read_data(filepath):
    """
    Reads the Excel file and preprocesses the data.

    """
    df = pd.read_excel(filepath)

    # Standardize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Convert numeric columns
    if "flair_score" in df.columns:
        df["flair_score"] = pd.to_numeric(df["flair_score"], errors="coerce")

    # Normalize ACT labels
    df["act"] = df["act"].astype(str).str.upper().str.strip()

    # Normalize SCENE labels: extract "SCENE I", "SCENE II", etc.
    df["scene"] = (
        df["scene"]
        .astype(str)
        .str.upper()
        .str.extract(r"(SCENE\s+[IVX]+)")
    )

    # Remove nonexistent Scene VI
    df = df[df["scene"] != "SCENE VI"]

    return df


# Save plot function
def save_plot(fig, filename):
    """
    Saves a matplotlib figure to a file.

    """
    fig.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


# 1. Positive vs Negative per ACT (Flair + GPT)
def plot_sentiment_per_act(df):
    """
    Plots sentiment distribution per ACT using Flair and GPT sentiment analysis.

    Args:
        df (pd.DataFrame): DataFrame containing the sentiment data. 
    Returns:
        fig (matplotlib.figure.Figure): The generated plot figure.
    
    """
    acts = ["ACT I", "ACT II", "ACT III", "ACT IV", "ACT V"]

    flair_counts = defaultdict(lambda: Counter({"POSITIVE": 0, "NEGATIVE": 0}))
    gpt_counts = defaultdict(lambda: Counter({"positive": 0, "negative": 0, "neutral": 0}))

    for _, row in df.iterrows():
        act = row["act"]
        if act not in acts:
            continue

        # Flair
        flair_label = str(row["flair_label"]).upper()
        if flair_label in ["POSITIVE", "NEGATIVE"]:
            flair_counts[act][flair_label] += 1

        # GPT
        sent = row["gpt_sentiment"]
        if sent in ["positive", "negative", "neutral"]:
            gpt_counts[act][row["gpt_sentiment"]] += 1

    fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    x = range(len(acts))
    width = 0.25

    # --- Flair subplot ---
    bars1 = axes[0].bar(
    [i - width / 2 for i in x],
    [flair_counts[a]["POSITIVE"] for a in acts],
    width=width,
    label="Flair Positive",
    color=POS_COLOR
)

    bars2 = axes[0].bar(
    [i + width / 2 for i in x],
    [flair_counts[a]["NEGATIVE"] for a in acts],
    width=width,
    label="Flair Negative",
    color=NEG_COLOR
)


    axes[0].set_title("Flair Sentiment Counts per Act")
    axes[0].legend()

    for bar in bars1 + bars2:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2, h + 2, str(h),
                     ha="center", va="bottom", fontsize=10)

    # --- GPT subplot ---
    bars3 = axes[1].bar(
    [i - width for i in x],
    [gpt_counts[a]["positive"] for a in acts],
    width=width,
    label="GPT Positive",
    color=POS_COLOR
)

    bars4 = axes[1].bar(
    x,
    [gpt_counts[a]["negative"] for a in acts],
    width=width,
    label="GPT Negative",
    color=NEG_COLOR
)

    bars5 = axes[1].bar(
    [i + width for i in x],
    [gpt_counts[a]["neutral"] for a in acts],
    width=width,
    label="GPT Neutral",
    color=NEU_COLOR
)

    axes[1].set_title("GPT Sentiment Counts per Act")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(acts)
    axes[1].legend()

    for bar in bars3 + bars4 + bars5:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width() / 2, h + 2, str(h),
                     ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    return fig


# 2. Sentiment distribution across SCENES (Flair + GPT)
def plot_sentiment_per_scene(df):
    """
    Plots sentiment distribution per SCENE using Flair and GPT sentiment analysis.
    Args:
        df (pd.DataFrame): DataFrame containing the sentiment data.
    Returns:
        fig (matplotlib.figure.Figure): The generated plot figure.
    
    """
    scenes = ["SCENE I", "SCENE II", "SCENE III", "SCENE IV", "SCENE V", "SCENE VII"]

    flair_counts = defaultdict(lambda: Counter({"POSITIVE": 0, "NEGATIVE": 0}))
    gpt_counts = defaultdict(lambda: Counter({"positive": 0, "negative": 0, "neutral": 0}))

    for _, row in df.iterrows():
        scene = row["scene"]
        if scene not in scenes:
            continue

        flair_label = str(row["flair_label"]).upper()
        if flair_label in ["POSITIVE", "NEGATIVE"]:
            flair_counts[scene][flair_label] += 1

        sent = row["gpt_sentiment"]
        if sent in ["positive", "negative", "neutral"]:
            gpt_counts[scene][row["gpt_sentiment"]] += 1


    fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    x = range(len(scenes))
    width = 0.25

    # --- Flair subplot ---
    bars1 = axes[0].bar(
    [i - width / 2 for i in x],
    [flair_counts[a]["POSITIVE"] for a in scenes],
    width=width,
    label="Flair Positive",
    color=POS_COLOR
)

    bars2 = axes[0].bar(
    [i + width / 2 for i in x],
    [flair_counts[a]["NEGATIVE"] for a in scenes],
    width=width,
    label="Flair Negative",
    color=NEG_COLOR
)

    axes[0].set_title("Flair Sentiment Counts per Scene")
    axes[0].legend()

    for bar in bars1 + bars2:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2, h + 2, str(h),
                     ha="center", va="bottom", fontsize=10)

    # --- GPT subplot ---
    bars3 = axes[1].bar(
    [i - width for i in x],
    [gpt_counts[a]["positive"] for a in scenes],
    width=width,
    label="GPT Positive",
    color=POS_COLOR
)

    bars4 = axes[1].bar(
    x,
    [gpt_counts[a]["negative"] for a in scenes],
    width=width,
    label="GPT Negative",
    color=NEG_COLOR
)

    bars5 = axes[1].bar(
    [i + width for i in x],
    [gpt_counts[a]["neutral"] for a in scenes],
    width=width,
    label="GPT Neutral",
    color=NEU_COLOR
)


    axes[1].set_title("GPT Sentiment Counts per Scene")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(scenes)
    axes[1].legend()

    for bar in bars3 + bars4 + bars5:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width() / 2, h + 2, str(h),
                     ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    return fig


# 3. Sentiment trend comparison: Hamlet vs Claudius
def plot_character_comparison(df):
    """
    Plots sentiment trend comparison between Hamlet and King Claudius using GPT sentiment analysis.
    Args:
        df (pd.DataFrame): DataFrame containing the sentiment data.
    Returns:
        fig (matplotlib.figure.Figure): The generated plot figure.
    
    """
    df = df.copy()
    df["sentiment_value"] = df["gpt_sentiment"].map(
        {"positive": 1, "neutral": 0, "negative": -1}
    )

    hamlet = df[df["speaker"] == "HAMLET"]
    claudius = df[df["speaker"] == "KING CLAUDIUS"]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hamlet["sentence number"], hamlet["sentiment_value"], label="Hamlet")
    ax.plot(claudius["sentence number"], claudius["sentiment_value"], label="King Claudius")

    ax.set_title("Sentiment Trend Comparison: Hamlet vs King Claudius")
    ax.set_xlabel("Sentence Number")
    ax.set_ylabel("Sentiment Value (+1 / 0 / -1)")
    ax.legend()
    return fig


# 4. Sentiment development for Hamlet
def plot_hamlet_trend(df):
    df = df.copy()
    df["sentiment_value"] = df["gpt_sentiment"].map(
        {"positive": 1, "neutral": 0, "negative": -1}
    )

    hamlet = df[df["speaker"] == "HAMLET"]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hamlet["sentence number"], hamlet["sentiment_value"])
    ax.set_title("Sentiment Development: Hamlet")
    ax.set_xlabel("Sentence Number")
    ax.set_ylabel("Sentiment Value")
    return fig


# 5. Sentiment development for King Claudius
def plot_claudius_trend(df):
    """
    Plots sentiment development for King Claudius using GPT sentiment analysis.
    Args:
        df (pd.DataFrame): DataFrame containing the sentiment data.
    Returns:
        fig (matplotlib.figure.Figure): The generated plot figure.
    
    """
    df = df.copy()
    df["sentiment_value"] = df["gpt_sentiment"].map(
        {"positive": 1, "neutral": 0, "negative": -1}
    )

    claudius = df[df["speaker"] == "KING CLAUDIUS"]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(claudius["sentence number"], claudius["sentiment_value"])
    ax.set_title("Sentiment Development: King Claudius")
    ax.set_xlabel("Sentence Number")
    ax.set_ylabel("Sentiment Value")
    return fig


if __name__ == "__main__":
    print("Starting Plot Creation...\n")

    filepath = "sentiment_analysis_hamlet.xlsx"
    df = read_data(filepath)

    print("Creating Plot 1...")
    save_plot(plot_sentiment_per_act(df), "plot_1.png")

    print("Creating Plot 2...")
    save_plot(plot_sentiment_per_scene(df), "plot_2.png")

    print("Creating Plot 3...")
    save_plot(plot_character_comparison(df), "plot_3.png")

    print("Creating Plot 4...")
    save_plot(plot_hamlet_trend(df), "play_hamlet_sentiment_development.png")

    print("Creating Plot 5...")
    save_plot(plot_claudius_trend(df), "play_claudius_sentiment_development.png")

    print("Plot Creation Completed.")