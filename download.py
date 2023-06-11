import requests
import zipfile
import csv
import psycopg2

# constants
url = 'https://232app.azurewebsites.net/data/BIS232Data.zip'
tempDir = './temp/'
zipFileName = tempDir + 'BIS232Data.zip'

# Step 1: Download the zip archive
response = requests.get(url)
with open(zipFileName, "wb") as zip_file:
    zip_file.write(response.content)

# Step 2: Extract the zip archive
with zipfile.ZipFile(tempDir + zipFileName, "r") as zip_ref:
    zip_ref.extractall(tempDir)

# Step 3: Process each CSV file
# TODO: replace `file1.csv` with files in zip archive
csv_files = ["file1.csv", "file2.csv", "file3.csv"]  # Update with the actual file names
for csv_file in csv_files:
    with open(f"extracted_folder/{csv_file}", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if present
        for row in csv_reader:
            # Step 4: Update records in the database
            # Parse the row data and execute necessary queries using psycopg2
            # Example: connection.execute("UPDATE table_name SET ... WHERE ...")

# Clean up - delete the downloaded zip and extracted files if needed
