"""
PCL1 & PfL Exercise 6 - Part 1c:
Sentiment Analysis using Flair.

- Reads selected_speakers.json.
- Uses Flair's pre-trained sentiment model to analyze each sentence.
- Stores the results in selected_speakers.json by adding a "sentiment"
  field to each sentence.
- The sentiment field contains:
    - label (str): "POSITIVE" or "NEGATIVE"
    - score (float): confidence score between 0 and 1

Author 1 & Matriculation Number:
Author 2 & Matriculation Number:
"""

import json
from flair.models import TextClassifier
from flair.data import Sentence

MIN_SENTENCES = 50  # required minimum sentiment rich sentences per speaker


def load_sentences():
    pass


def save_json():
    pass


def analyze_sentiments(sentences: list[dict]) -> list[dict]:
    """
    Analyze sentiments of the given sentences using Flair.

    Args:
        sentences (list of dict): List of sentence dictionaries.

    Returns:
        list of dict: List of sentences with added sentiment data.
    """
    # Load Flair's pre-trained sentiment classifier
    print("Loading Flair sentiment model...")
    classifier = TextClassifier.load("sentiment")

    sentiment_sentences = []

    # Analyze each sentence
    for sentence_dict in sentences:
        text = sentence_dict["text"]

        # Create a Flair sentence object and predict sentiment
        flair_sentence = Sentence(text)
        classifier.predict(flair_sentence)

        # Get the sentiment label (POSITIVE or NEGATIVE) and confidence score
        sentiment_label = flair_sentence.labels[0]

        sentence_dict["sentiment"] = {
            "label": sentiment_label.value,
            "score": sentiment_label.score,
        }
        sentiment_sentences.append(sentence_dict)

    return sentiment_sentences


# Check if there are enough high-confidence sentences, you need 50 per speaker
def has_enough_sentences():
    pass


def main(play_name):
    pass


if __name__ == "__main__":
    play_name = "your_play_here" # Replace with the actual play name

    print(f"Starting sentiment analysis for {play_name}...")
    print(f"Minimum required sentences: {MIN_SENTENCES}\n")

    main(play_name)

    print("Sentiment analysis complete!")
    print(f"selected_speakers_{play_name}.json has"
          " been updated with sentiment data.")
