"""
PCL1 & PfL Exercise 6 - Part 2a:
Calling an API for Emotion Analysis

- Writing a prompt for Emotion Analysis.
- Calling the OpenAI API to analyze the whole jason file and randomly select 50 sentences per speaker.
- Using a Command Line Interface (CLI) to specify input/output files.
- Store the final results in an Excel file.

Author 1 & Matriculation Number: Liu Xiaoduan 23-749-609
Author 2 & Matriculation Number: Qi Xinyan 23-757-511
"""

import json
import sys
import random
from openpyxl import Workbook
from openai import OpenAI
from tqdm import tqdm  # for progress bar


SYSTEM_MESSAGE = """
Analyze the given sentence and output a JSON object in the following format:

{
  "main_emotion": "anger | anticipation | disgust | fear | joy | sadness | surprise | trust",
  "sentiment": "positive | negative | neutral"
}

Rules:
- Your output MUST be valid JSON.
- main_emotion must be exactly one of the 8 categories.
- sentiment must be exactly one of: positive, negative, neutral.
- Base your analysis ONLY on the sentence text.
"""

# Loaded JSON is based on the solution data from Part 1, not our original Part1 output.
# but we revised our codes and rerun after realizing we did not originally control the >0.9 "confidence" score
def load_json(path):
    """"
    Load JSON data from a file.

    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Group sentences by speaker
def group_sentences_by_speaker(data):
    """
    Group sentences by speaker.
    
    Returns a dictionary with speaker names as keys
    and lists of their sentences as values.

    """
    grouped = {}
    for item in data:
        speaker = item["speaker"]
        grouped.setdefault(speaker, []).append(item)
    return grouped

# In addition to the full set of King and Hamlet lines, 
# we randomly sampled 100 sentences from the combined pool of the two speakers.
def sample_random_sentences(grouped_data, total_samples=100):
    """
    Randomly sample a fixed number of sentences
    from the combined King + Hamlet pool.
    Returns a list of sampled sentences.

    """
    combined = []

    for speaker in ["KING CLAUDIUS", "HAMLET"]:
        combined.extend(grouped_data.get(speaker, []))

    if len(combined) <= total_samples:
        return combined

    return random.sample(combined, total_samples)

# GPT Emotion + Sentiment
def analyze_with_gpt(text, client):
    """
    Analyze text with GPT to get main emotion and sentiment.
    
    Returns a dictionary with keys 'main_emotion' and 'sentiment'.

    """
    import json as _json
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": text},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        return _json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"GPT error: {e}")
        return {"main_emotion": None, "sentiment": None}

# Save to Excel
def save_to_excel(rows, output_path):
    """
    Save the results to an Excel file.

    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Sentiment Analysis"

    ws.append([
        "act", "scene", "speaker", "sentence number", "text",
        "flair_label", "flair_score",
        "gpt_main_emotion", "gpt_sentiment"
    ])

    for row in rows:
        ws.append([
            row["act"],
            row["scene"],
            row["speaker"],
            row["sentence number"],
            row["text"],
            row["flair_label"],
            row["flair_score"],
            row["gpt_main_emotion"],
            row["gpt_sentiment"],
        ])

    wb.save(output_path)
    print(f"Excel saved to: {output_path}")

# CLI Setup
def system_setup():
    """
    Setup command line arguments:
    python part2_call_API.py <input_json_file> <output_excel_file> <max_sentences_per_speaker>
    Returns input_path, output_path, max_per_speaker.

    """
    import sys

    if len(sys.argv) != 4:
        print("Error: Missing required arguments\n")
        print(
            "Usage: python part2_call_API.py <input_json_file> "
            "<output_excel_file> <max_sentences_per_speaker>\n"
        )
        print("Example:")
        print(
            "  python part2_call_API.py "
            "selected_speakers_hamlet.json "
            "sentiment_analysis_hamlet.xlsx "
            "50"
        )
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    max_per_speaker = int(sys.argv[3])

    return input_path, output_path, max_per_speaker

# Main Processing Function
def process_file(input_path, output_path, max_per_speaker):
    """
    Process the input file and perform emotion analysis.
    
    input_path: Path to the input JSON file.
    output_path: Path to the output Excel file.
    max_per_speaker: Maximum sentences per speaker to analyze.

    """
    print("Loading JSON...")

    # Load JSON
    data = load_json(input_path)

    # Group by speaker
    grouped = group_sentences_by_speaker(data)

    # Debug: print counts
    print("KING total:", len(grouped.get("KING CLAUDIUS", [])))
    print("HAMLET total:", len(grouped.get("HAMLET", [])))

    # Full sentences for KING and HAMLET
    king_sentences = grouped.get("KING CLAUDIUS", [])
    hamlet_sentences = grouped.get("HAMLET", [])

    # Random sample 100 sentences from combined KING + HAMLET pool
    sampled_sentences = sample_random_sentences(grouped, total_samples=100)

    # Combine all sentences
    final_data = king_sentences + hamlet_sentences + sampled_sentences

    # Shuffle the final data to mix the sampled sentences
    start = len(king_sentences) + len(hamlet_sentences)
    random.shuffle(final_data[start:])

    # Call GPT API for each sentence
    client = OpenAI()
    results = []

    print("\nAnalyzing sentences with ChatGPT...\n")

    # Progress bar for showing progress generated by Copilot
    for item in tqdm(final_data, desc="Processing", unit="sentence"):
        text = item["text"]
        flair_label = item["sentiment"]["label"]
        flair_score = item["sentiment"]["score"]

        gpt_result = analyze_with_gpt(text, client)

        results.append({
            "act": item["act"],
            "scene": item["scene"],
            "speaker": item["speaker"],
            "sentence number": item["sentence number"],
            "text": text,
            "flair_label": flair_label,
            "flair_score": flair_score,
            "gpt_main_emotion": gpt_result.get("main_emotion"),
            "gpt_sentiment": gpt_result.get("sentiment"),
        })

    save_to_excel(results, output_path)


if __name__ == "__main__":
    print("Starting Emotion Analysis...\n")

    # Aquire parameters of command line
    input_path, output_path, max_per_speaker = system_setup()

    # Run Process_file function
    process_file(input_path, output_path, max_per_speaker)

    print("\nEmotion Analysis Completed.")
