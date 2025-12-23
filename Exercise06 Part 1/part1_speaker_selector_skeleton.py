"""
PCL1 & PfL Exercise 6 - Part 1b:
Speaker Selection.

- Parses one XML play file from the NLTK Shakespeare XML corpus.
- Extracts all spoken lines.
- Stores them in all_sentences.json.

Author 1 & Matriculation Number:
Author 2 & Matriculation Number:
"""

import json

MIN_SENTENCES = 50  # required minimum number of sentences per speaker


# Load sentences from a JSON file
def load_sentences():
    pass


# Calculate statistics about speakers, acts, and spoken lines in the play
def compute_statistics():
    pass


# Find speakers that spoke in all acts
# and have at least MIN_SENTENCES spoken lines
def find_valid_speakers():
    pass


# Print statistics about the play
def print_statistics():
    pass


# Interactively ask user for speaker selection until valid input is given
# Decide on two speakers that you would like to analyse
def ask_for_speakers():
    pass


# Filter sentences to include only those spoken by the selected speakers
def filter_sentences():
    pass


# Save data as JSON to the given path
def save_json():
    pass


# Run through the speaker selection process
def main(play_name):
    pass


if __name__ == "__main__":
    # Enter your selected play to parse
    play_name = "your_play_here"  # Placeholder for selected play

    print(f"Loading sentences from all_sentences_{play_name}.json ...")

    main(play_name)

    print("Speaker selection complete!")
    print(f"Selected speakers saved to selected_speakers_{play_name}.json.")
