"""
PCL1 & PfL Exercise 6 - Part 2.1.3
Numerical Evaluation of Automatic Sentiment/Emotion Results
Based on the flair- and OpenAI annotations, compute the following statistics:

- count the number of positive, negative, and neutral sentences per character
- compute sentiment distribution across acts or scenes
- check the number of highly emotional sentences, that should be the total number of text lines in the json file equals to 1489+547 = 2036
- any additional counts that support interpretation of sentiment dynamics, in this case, count average emotional intensity per character

Author 1 & Matriculation Number: Liu Xiaoduan 23-749-609
Author 2 & Matriculation Number: Qi Xinyan 23-757-511
"""

import pandas as pd
from collections import defaultdict, Counter

# The random 100 extra sampled lines for manual annotation was not included in this statistics analysis

# Excel file path
INPUT_PATH = "/Users/liuxduan/Downloads/exercise_06_b/sentiment_analysis_hamlet.xlsx"

def load_excel(path):
    """
    Load the Excel file into a pandas DataFrame.
    Args:
        path (str): Path to the Excel file.
    Returns:
        pd.DataFrame: Loaded DataFrame.

    """
    return pd.read_excel(path)

# Count positive/negative/neutral per character
def count_sentiment_per_character(df):
    """
    Count the number of positive, negative, and neutral sentences per character.
    Args:   
        df (pd.DataFrame): DataFrame containing sentiment data.
    Returns:
        defaultdict: Counts of sentiments per character.
    
    """
    counts = defaultdict(lambda: Counter({"positive": 0, "negative": 0, "neutral": 0}))
    for _, row in df.iterrows():
        speaker = row["speaker"]
        sentiment = row["gpt_sentiment"]
        counts[speaker][sentiment] += 1
    return counts

# Sentiment distribution across ACTs
def sentiment_distribution_by_act(df):
    """
    Compute sentiment distribution across acts.
    Returns:
        defaultdict: Counts of sentiments per act.
    
    """
    counts = defaultdict(lambda: Counter({"positive": 0, "negative": 0, "neutral": 0}))
    for _, row in df.iterrows():
        act = row["act"]
        sentiment = row["gpt_sentiment"]
        counts[act][sentiment] += 1
    return counts

# Sentiment distribution across SCENEs
def sentiment_distribution_by_scene(df):
    """
    Compute sentiment distribution across scenes.
    Returns:
        defaultdict: Counts of sentiments per scene.
    
    """
    counts = defaultdict(lambda: Counter({"positive": 0, "negative": 0, "neutral": 0}))
    for _, row in df.iterrows():
        scene = row["scene"]
        sentiment = row["gpt_sentiment"]
        counts[scene][sentiment] += 1
    return counts

# Check total lines = 2036
def check_total_lines(df):
    """
    Check if the total number of lines equals 2036.
    Args:
        df (pd.DataFrame): DataFrame containing sentiment data.
    Returns:
        tuple: (bool, int) - True if total lines equal expected, else False

    """
    total = len(df)
    expected = 2036
    return total == expected, total

# Count highly emotional sentences (|flair_score| ≥ 0.90)
def count_high_emotion(df):
    """
    Count the number of highly emotional sentences (|flair_score| ≥ 0.90).
    Args:    
        df (pd.DataFrame): DataFrame containing sentiment data.
    Returns:
        int: Count of highly emotional sentences.

    """
    return (df["flair_score"].abs() >= 0.90).sum()

# Additional: average emotional intensity per character
def average_intensity_per_character(df):
    """
    Compute average emotional intensity per character.
    Returns:
        dict: Average emotional intensity per character.
    Args:
        df (pd.DataFrame): DataFrame containing sentiment data.

    """
    scores = defaultdict(list)
    for _, row in df.iterrows():
        speaker = row["speaker"]
        scores[speaker].append(abs(row["flair_score"]))

    avg_scores = {}
    for speaker, vals in scores.items():
        avg_scores[speaker] = sum(vals) / len(vals) if vals else 0
    return avg_scores

def print_section(title):
    """
    Print a formatted section header with a title.

    Args:
    title (str): The section title to display.

    Returns: a visual separator consisting of two lines of
    equal signs surrounding the given title.

    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

# Main function to run the analysis
def main():
    df = load_excel(INPUT_PATH)

    # Sentiment per character
    print_section("1) Sentiment Count per Character")
    char_counts = count_sentiment_per_character(df)
    for speaker, cnt in char_counts.items():
        print(f"{speaker}: {dict(cnt)}")

    # Sentiment distribution by ACT
    print_section("2) Sentiment Distribution Across Acts")
    act_counts = sentiment_distribution_by_act(df)
    for act, cnt in act_counts.items():
        print(f"{act}: {dict(cnt)}")

    # Sentiment distribution by SCENE
    print_section("2b) Sentiment Distribution Across Scenes")
    scene_counts = sentiment_distribution_by_scene(df)
    for scene, cnt in scene_counts.items():
        print(f"{scene}: {dict(cnt)}")

    # Total line count check
    print_section("3) Total Line Count Check")
    ok, total = check_total_lines(df)
    print(f"Total lines = {total}")
    print(f"Check result: {ok}")

    # Additional: average emotional intensity
    print_section("4) Average Emotional Intensity per Character")
    avg_intensity = average_intensity_per_character(df)
    for speaker, avg in avg_intensity.items():
        print(f"{speaker}: {avg:.4f}")

    print("\n Analysis complete.")

if __name__ == "__main__":
    main()