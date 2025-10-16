import json

def find_missing_careers():
    """
    Reads two JSON files, compares their career titles, and prints the titles
    that are in the comprehensive data but not in the existing careers list.
    """
    try:
        with open('backend/career_data.json', 'r', encoding='utf-8') as f:
            all_careers_data = json.load(f)
        
        with open('backend/existing_careers.json', 'r', encoding='utf-8') as f:
            existing_careers_list = json.load(f)

        all_career_titles = {career['title'] for career in all_careers_data}
        existing_career_titles = set(existing_careers_list)

        missing_careers = all_career_titles - existing_career_titles

        if missing_careers:
            print("Missing Careers:")
            for career in sorted(list(missing_careers)):
                print(f"- {career}")
        else:
            print("No missing careers found.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure both JSON files exist.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    find_missing_careers()