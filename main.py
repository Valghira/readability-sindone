import json
import csv
import os
from datetime import datetime
from src import utils
from src import indices

# ----------------------------
# Configuration settings
# ----------------------------
json_file = "./file_to_process/content.json"
MAX_SENTENCES = None  # Set to an integer to limit processing, or None to process all

# ----------------------------
# Index registry
# ----------------------------

# Maps index name → callable(text, lang) → score
INDEX_REGISTRY = {
    "gulpease":    lambda text, lang: indices.gulpease_index(text),
    "flesch":      lambda text, lang: indices.flesch_index(text, lang),
    "gunning_fog": lambda text, lang: indices.gunning_fog_index(text, lang),
}

# Maps index name → set of languages it supports
INDEX_LANGS = {
    "gulpease":    {"it"},
    "flesch":      {"it", "en"},
    "gunning_fog": {"it", "en"},
}

# ----------------------------
# Load JSON data from file
# ----------------------------
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ----------------------------
# Report generation
# ----------------------------

def generate_report(indices_to_use, lang, process_all_categories=False, category=None, sub_category=None):
    """
    Generate a CSV readability report.

    Parameters:
        indices_to_use : list[str] | "all"
            Indices to compute. Pass "all" to include every available index.
        lang : str | "all"
            Language of the texts ("it", "en", ...).
            Pass "all" to process every language in the JSON (a 'Lang' column is always included).
        process_all_categories : bool
            If True, process all categories; otherwise filter by category/sub_category.
        category : str | None
        sub_category : str | None
    """
    if indices_to_use == "all":
        indices_to_use = list(INDEX_REGISTRY.keys())

    langs_to_process = list(data.keys()) if lang == "all" else [lang]

    # Collect (sentence, actual_lang) pairs
    tagged_sentences = []
    for current_lang in langs_to_process:
        if current_lang not in data:
            raise ValueError(f"Language '{current_lang}' not found in the JSON data.")
        if process_all_categories:
            for age_group in data[current_lang]:
                for cat in data[current_lang][age_group]:
                    for s in utils.extract_sentences(data[current_lang][age_group][cat]):
                        tagged_sentences.append((s, current_lang))
        else:
            if category is None or sub_category is None:
                raise ValueError("Both 'category' and 'sub_category' must be specified if 'process_all_categories' is False.")
            for s in utils.extract_sentences(data[current_lang][category][sub_category]):
                tagged_sentences.append((s, current_lang))

    if MAX_SENTENCES:
        tagged_sentences = tagged_sentences[:MAX_SENTENCES]

    results = []
    for idx, (sentence, current_lang) in enumerate(tagged_sentences, start=1):
        row = {
            "Id": idx,
            "Lang": current_lang,
            "Sentence_Text": sentence,
            "Letters": utils.letter_count(sentence),
            "Words": utils.word_count(sentence),
            "Num_Sentences": utils.sentence_count(sentence),
        }
        for index_name in indices_to_use:
            if current_lang in INDEX_LANGS[index_name]:
                score = INDEX_REGISTRY[index_name](sentence, current_lang)
                row[index_name] = round(score, 2) if score is not None else None
            else:
                row[index_name] = "N/A"
        results.append(row)

    os.makedirs("./reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    indices_label = "_".join(indices_to_use)
    cat_label = "all" if process_all_categories else f"{category}_{sub_category}"
    csv_file_path = f"./reports/report_{indices_label}_{lang}_{cat_label}_{timestamp}.csv"

    fieldnames = ["Id", "Lang", "Sentence_Text", "Letters", "Words", "Num_Sentences"] + indices_to_use
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"CSV report generated: {csv_file_path}")

# ----------------------------
# Examples
# ----------------------------

# generate_report(indices_to_use=["gulpease"], lang="it", process_all_categories=False, category="adult", sub_category="typical")
# generate_report(indices_to_use=["flesch"], lang="en", process_all_categories=True)
generate_report(indices_to_use="all", lang="all", process_all_categories=True)