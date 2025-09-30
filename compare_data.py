import json
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))


# Load the production data
with open('production_career_data.json', 'r') as f:
    production_data = json.load(f)

# Load the local data
# Note: This is a simplified representation of your local data.
# In a real scenario, you would import and use the actual data.
from backend.comprehensive_careers import COMPREHENSIVE_CAREERS
local_data = {"careers": COMPREHENSIVE_CAREERS}

# Compare the number of careers
num_local_careers = len(local_data["careers"])
num_production_careers = production_data["total_careers"]

print(f"Number of local careers: {num_local_careers}")
print(f"Number of production careers: {num_production_careers}")

if num_local_careers != num_production_careers:
    print("\nWarning: The number of careers is different.")
else:
    print("\nThe number of careers is the same.")

# Compare the actual content (up to a certain limit to avoid excessive output)
local_titles = {c["title"] for c in local_data["careers"]}
production_titles = {c["title"] for c in production_data["careers"]}

if local_titles == production_titles:
    print("The career titles are identical.")
else:
    print("\nWarning: The career titles are different.")
    
    print("\nTitles in local but not in production:")
    print(sorted(list(local_titles - production_titles)))
    
    print("\nTitles in production but not in local:")
    print(sorted(list(production_titles - local_titles)))