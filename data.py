import pandas as pd
import re

# 📂 Load the dataset
df = pd.read_csv(r"L:\Guvi\Project 1\Web ScrapIMDB\merged_cleaned_movies.csv")

# 🔍 Print column names for debugging
print("Columns in CSV file:", df.columns)

# 🔄 Rename columns to consistent format
df.rename(columns={'Movie Name': 'movie_name', 'Vote Counts': 'votes'}, inplace=True)

# 🔍 Check for duplicate movie names
duplicate_count = df.duplicated(subset=['movie_name']).sum()
print(f"Total duplicate movies found: {duplicate_count}")

# 🔄 Remove duplicate movies (keeping the first occurrence)
df.drop_duplicates(subset=['movie_name'], keep='first', inplace=True)

# 🔧 Function to convert "2h 7m" → 127 minutes
def convert_duration(duration_str):
    if isinstance(duration_str, str):  # Ensure it's a string
        match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', duration_str)  
        if match:
            hours = int(match.group(1)) if match.group(1) else 0
            minutes = int(match.group(2)) if match.group(2) else 0
            return hours * 60 + minutes
    return None  # If format is incorrect

# ✅ Standardize and convert duration column
if 'Duration' in df.columns:
    df['Duration'] = df['Duration'].astype(str)  # Convert to string first
    df['Duration'] = df['Duration'].apply(convert_duration)  # Convert to minutes

# 🛠 Handle missing or invalid values
df.dropna(subset=['Duration'], inplace=True)
df['Duration'] = df['Duration'].astype(int)  # Ensure it's an integer

# 💾 Save cleaned data
df.to_csv("cleaned_movies.csv", index=False)

print("✅ Duplicates removed, duration converted, and cleaned data saved successfully!")
