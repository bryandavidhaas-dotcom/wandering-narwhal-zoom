import json

def verify_career_count():
    """
    Counts the total and unique careers from the production data to verify the count.
    """
    try:
        with open('production_career_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            careers = data.get('careers', [])
    except FileNotFoundError:
        print("Error: production_career_data.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from production_career_data.json.")
        return

    total_entries = len(careers)
    unique_titles = set(career.get('title', '').lower() for career in careers)
    total_unique_careers = len(unique_titles)

    print("--- Career Count Verification ---")
    print(f"Total career entries in the list: {total_entries}")
    print(f"Total unique career titles: {total_unique_careers}")

    if total_entries == total_unique_careers:
        print("\nConclusion: The career count is consistent. There are no duplicate titles.")
    else:
        print(f"\nConclusion: Discrepancy found. There are {total_entries - total_unique_careers} duplicate titles.")

if __name__ == "__main__":
    verify_career_count()