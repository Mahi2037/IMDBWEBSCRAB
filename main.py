import re
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=family")

# Click 'Load More' until all movies are loaded
while True:
    try:
        load_more_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ipc-see-more')]"))
        )
        driver.execute_script("arguments[0].click();", load_more_button)  # Click using JavaScript
        time.sleep(5)  # Wait for new movies to load
        print("Clicked 'Load More' button")
    except:
        print("No more 'Load More' button found. All movies are loaded.")
        break

# Find all movie containers
movies = driver.find_elements(By.XPATH, ".//div[contains(@class, 'sc-f30335b4-0')]")

# Open CSV file to save data
with open("imdb_movies_2024_family.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Movie Name", "Genre", "Duration", "Rating", "Vote Counts" ])  # Added Genre column

    for movie in movies:
        text = movie.text  # Extract text from the movie container

        # Remove unwanted parts
        cleaned_text = re.sub(r"Rate.*|Metascore.*|\b2024\b|\bR\b", "", text, flags=re.DOTALL).strip()

        # Extract data using regex
        name_match = re.search(r"^\d+\.\s*(.+)", cleaned_text)  # Movie Name
        duration_match = re.search(r"(\d+h\s*\d*m|\d+h|\d+m)", cleaned_text)  # Duration
        rating_match = re.search(r"(\d+\.\d)", cleaned_text)  # Rating
        votes_match = re.search(r"\((\d+K?)\)", cleaned_text)  # Votes

        # Get values or set to empty if not found
        movie_name = name_match.group(1) if name_match else "N/A"
        genre = "Family"  # Default Genre
        duration = duration_match.group(1) if duration_match else "N/A"
        rating = rating_match.group(1) if rating_match else "N/A"
        votes = votes_match.group(1) if votes_match else "N/A"


        # Write to CSV
        writer.writerow([movie_name, genre, duration, rating, votes])

# Close the browser
driver.quit()

print("Scraping complete. Data saved in 'imdb_movies_2024_family.csv'.")
