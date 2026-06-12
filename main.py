import json
import csv
import os
from src import utils 

# ----------------------------
# Configuration
# ----------------------------
json_file = "./file_to_process/content.json"  # file with phrases

# Optional: limit the number of sentences to analyze (for future GUI)
MAX_SENTENCES = None  # set to an integer to limit, or None to process all

# ----------------------------
# Load JSON data
# ----------------------------
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ----------------------------
# Extract sentences from JSON
# ----------------------------
# Example: italian adult typical texts
sentences = utils.extract_sentences(data["it"]["adult"]["typical"])

# Apply optional limit
if MAX_SENTENCES:
    sentences = sentences[:MAX_SENTENCES]

# ----------------------------
# Function to generate report CSV
# ----------------------------

def generate_gulpease_report(sentences, report_filename="gulpease_report.csv"):
    report_folder = "./reports"
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    results = []

    for idx, sentence in enumerate(sentences, start=1):
        raw_score = utils.gulpease_index(sentence)
        if raw_score is None:
            normalized_score = None
            raw_score_rounded = None
        else:
            normalized_score = max(0, min(100, raw_score))
            raw_score_rounded = round(raw_score, 2)
            normalized_score = round(normalized_score, 2)
        results.append({
            "Id" : idx,
            "Sentence_Text" : sentence,
            "Letters" : utils.letter_count(sentence),
            "Words" : utils.word_count(sentence),
            "Num_Sentences" : utils.sentence_count(sentence),
            "Raw_Gulpease_index" : raw_score_rounded,
            "Normalized_Gulpease_index" : normalized_score
        })

    csv_file_path = os.path.join(report_folder, report_filename)

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Id", "Sentence_Text", "Letters", "Words", "Num_Sentences", "Raw_Gulpease_index", "Normalized_Gulpease_index"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Scrivo l’intestazione
        writer.writeheader()
        
        # Scrivo ogni riga del report
        for row in results:
            writer.writerow(row)

    print(f"Report CSV generato: {csv_file_path}")

# ----------------------------
# Generate report
# ----------------------------

generate_gulpease_report(sentences)
