import mysql.connector
import pandas as pd

# ✅ Step 1: Load CSV file
csv_file = r"L:\Guvi\Project 1\Web ScrapIMDB\imdb_movie_2024.csv"
df = pd.read_csv(csv_file)

# ✅ Ensure correct column names (remove unwanted spaces)
df.columns = df.columns.str.strip()

# ✅ Debugging: Print CSV column names
print("CSV Columns:", df.columns.tolist())

# ✅ Rename columns to match the database table format
column_mapping = {
    "Movie_name": "Movie Name",
    "Rating": "Ratings",
    "Vote_Counts": "Voting Counts"
}

df.rename(columns=column_mapping, inplace=True, errors="ignore")

# ✅ Ensure 'Voting Counts' column exists
if "Voting Counts" not in df.columns:
    print("❌ Error: 'Voting Counts' column not found! Check CSV file.")
    exit()

# ✅ Handle missing values
df["Voting Counts"] = df["Voting Counts"].fillna(0)

# ✅ Convert 'Voting Counts' (e.g., "44K" → 44000)
def convert_votes(value):
    if isinstance(value, str) and 'K' in value:
        return int(float(value.replace('K', '')) * 1000)
    return int(value)

df["Voting Counts"] = df["Voting Counts"].apply(convert_votes)
df["Ratings"] = df["Ratings"].fillna(0).astype(float)

# ✅ Database connection configuration
config = {
    'host': "gateway01.eu-central-1.prod.aws.tidbcloud.com",
    'port': 4000,
    'user': "3VYhXePBWtRATMR.root",
    'password': "x6mZSRxbndttBExE",
    'database': "IMDB",
    'ssl_ca': r"L:\Guvi\Project 1\certs\ca.pem",  # ✅ Update CA path
}

# ✅ Establish the connection
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    print("✅ Connection established successfully!")
except mysql.connector.Error as err:
    print(f"❌ Connection error: {err}")
    exit()

# ✅ Create table (if not exists)
create_table_query = """
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Movie Name` VARCHAR(255),
    `Genre` VARCHAR(100),
    `Ratings` FLOAT,
    `Voting Counts` INT,
    `Duration` VARCHAR(50)
);
"""
cursor.execute(create_table_query)
connection.commit()

# ✅ Insert data into TiDB Cloud
insert_query = """
INSERT INTO movies (`Movie Name`, `Genre`, `Ratings`, `Voting Counts`, `Duration`)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    `Ratings` = VALUES(`Ratings`), 
    `Voting Counts` = VALUES(`Voting Counts`);
"""

# ✅ Convert DataFrame to list of tuples
data = list(df[['Movie Name', 'Genre', 'Ratings', 'Voting Counts', 'Duration']].itertuples(index=False, name=None))

if data:
    cursor.executemany(insert_query, data)  # Efficient batch insert
    connection.commit()
    print(f"✅ Successfully inserted/updated {len(df)} records!")
else:
    print("⚠️ No valid data to insert.")

# ✅ Close connection
cursor.close()
connection.close()
print("✅ Database connection closed.")
