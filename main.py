import json
import csv
import os
from datetime import datetime
from src import utils
from src import indices

# ----------------------------
# Configuration settings
# ----------------------------
json_file = "./file_to_process/content.json"  # Path to the JSON file containing text phrases

# Optional: limit the number of sentences to analyze (useful for future GUI implementations)
MAX_SENTENCES = None  # Set to an integer to limit processing, or None to process all sentences

# ----------------------------
# Load JSON data from file
# ----------------------------
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ----------------------------
# Function to generate a CSV report with Gulpease readability scores
# ----------------------------

def generate_gulpease_report(process_all_categories=False, category=None, sub_category=None):
    report_folder = "./reports"
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    # Extract sentences based on parameters
    if process_all_categories:
        sentences = []
        for lang in data:
            for age_group in data[lang]:
                for cat in data[lang][age_group]:
                    sentences.extend(utils.extract_sentences(data[lang][age_group][cat]))
    else:
        if category is None or sub_category is None:
            raise ValueError("Both 'category' and 'sub_category' must be specified if 'process_all_categories' is False.")
        sentences = utils.extract_sentences(data["it"][category][sub_category])

    # Apply optional limit to number of sentences
    if MAX_SENTENCES:
        sentences = sentences[:MAX_SENTENCES]

    results = []

    # Compute readability scores for each sentence
    for idx, sentence in enumerate(sentences, start=1):
        raw_score = indices.gulpease_index(sentence)
        if raw_score is None:
            normalized_score = None
            raw_score_rounded = None
        else:
            # Normalize score to be within 0 to 100 and round to 2 decimals
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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if process_all_categories:
        report_filename = f"gulpease_report_all_categories_{timestamp}.csv"
    else:
        report_filename = f"gulpease_report_{category}_{sub_category}_{timestamp}.csv"

    csv_file_path = os.path.join(report_folder, report_filename)

    # Write results to CSV file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Id", "Sentence_Text", "Letters", "Words", "Num_Sentences", "Raw_Gulpease_index", "Normalized_Gulpease_index"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        
        # Write the CSV header
        writer.writeheader()
        
        # Write each row of the report
        for row in results:
            writer.writerow(row)

    print(f"CSV report generated: {csv_file_path}")

# ----------------------------
# Generate the readability report CSV
# ----------------------------

#generate_gulpease_report(process_all_categories=False, category="adult", sub_category="typical")
# generate_gulpease_report(process_all_categories=False, category="category_name", sub_category="sub_category_name")
generate_gulpease_report(process_all_categories=True)
