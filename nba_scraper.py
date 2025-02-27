import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape (Example: NBA scores from Basketball-Reference)
url = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"

# Send a request to the website
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    print("Page loaded successfully!")
else:
    print("Failed to load page:", response.status_code)

# Find the main stats table
table = soup.find("table", {"id": "per_game_stats"})  # ID found from inspecting HTML

# Extract column headers
headers = [header.text.strip() for header in table.find("thead").find_all("th")]

# Extract player stats
rows = table.find("tbody").find_all("tr")  # Now, only extracting table body rows
data = []
for row in rows:
    cols = row.find_all("td")
    if cols:  # Skip empty rows
        data.append([col.text.strip() for col in cols])

# Check data length before creating DataFrame
print(f"Extracted {len(data[0])} columns, expected {len(headers)} columns")

# Ensure headers and data match in length
if len(data[0]) == len(headers) - 1:  # Some tables have an extra 'Rank' column
    headers = headers[1:]  # Remove the first column header (Rank)

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)

### 🔥 Fix 1: Remove extra repeated headers inside the data ###
# Drop rows where "Age" isn't a number (these rows are often duplicate headers)
df = df[df["Age"].apply(lambda x: str(x).isdigit())]

### 🔥 Fix 2: Remove duplicate player names (traded players) ###
# If a player appears multiple times (for different teams), keep only their "Total" row
df = df.drop_duplicates(subset=["Player"], keep="last")  # Keeps only the last occurrence

# Print cleaned data
print(df.head())  # Print first 5 rows

# Save the cleaned DataFrame
df.to_csv("nba_2025_per_game_stats.csv", index=False, encoding="utf-8-sig")
print("Data saved to nba_2025_per_game_stats.csv")