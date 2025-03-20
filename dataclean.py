import pandas as pd
import glob
import os

# Specify the folder containing CSV files (modify the path accordingly)
folder_path = r"L:\Guvi\Project 1\Web ScrapIMDB\*.csv"  # Use raw string

# Get all CSV file paths
csv_files = glob.glob(folder_path)

# Check if CSV files exist
if not csv_files:
    print("No CSV files found in the specified directory.")
    exit()

# Load and concatenate all CSV files
df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Drop duplicate rows
df.drop_duplicates(inplace=True)

# Handle missing values (remove rows with NaN values)
df.dropna(inplace=True)

# Ensure columns exist before converting data types
for col in ['duration', 'rating', 'vote_counts']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Sort by rating (optional)
if 'rating' in df.columns:
    df.sort_values(by='rating', ascending=False, inplace=True, ignore_index=True)

# Save cleaned data to a new CSV file
output_file = "merged_cleaned_movies.csv"
df.to_csv(output_file, index=False)

print(f"All CSV files merged and cleaned successfully! Saved as {output_file}")