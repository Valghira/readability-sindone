from src.core import load_data, generate_csv_report, generate_excel_report, DEFAULT_JSON_PATH

# ----------------------------
# CLI entry point
# ----------------------------
# Run with: python main.py
# To change what gets generated, edit the calls below.
# ----------------------------

if __name__ == "__main__":
    data = load_data(DEFAULT_JSON_PATH)

    # Examples — uncomment/modify as needed:
    # generate_csv_report(data, indices_to_use=["gulpease"], lang="it", process_all_categories=False, category="adult", sub_category="typical")
    # generate_csv_report(data, indices_to_use="all", lang="all", process_all_categories=True)
    # generate_excel_report(data, indices_to_use="all", lang="all", process_all_categories=True)

    generate_csv_report(data, indices_to_use="all", lang="it", process_all_categories=False, category="adult", sub_category="typical")
    generate_excel_report(data, indices_to_use="all", lang="it", process_all_categories=False, category="adult", sub_category="typical")
