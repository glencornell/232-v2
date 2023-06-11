import requests
import zipfile
import csv
import psycopg2


class section232Updater:
    def __init__(self):
        # constants
        self.url = 'https://232app.azurewebsites.net/data/BIS232Data.zip'
        self.tempDir = './temp/' # TODO: use mkstemp() instead
        self.zipFileName = self.tempDir + 'BIS232Data.zip'
        # TODO: setup connection to database
 
    def downloadZipFile(self):
        # Step 1: Download the zip archive
        response = requests.get(self.url)
        with open(self.zipFileName, "wb") as zip_file:
            zip_file.write(response.content)

    def extractZipFile(self):
        # Step 2: Extract the zip archive
        with zipfile.ZipFile(self.zipFileName, "r") as zip_ref:
            zip_ref.extractall(tempDir + "extracted")

    def updateDatabase(self):
        # Step 3: Process each CSV file
        # TODO: replace `file1.csv` with files in zip archive
        csv_file = "file1.csv" 
        with open(tempDir + f"extracted/{csv_file}", "r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header if present
            # Step 4: Update records in the database
            # Parse the row data and execute necessary queries using psycopg2
            # Example: connection.execute("UPDATE table_name SET ... WHERE ...")

    def cleanup(self):
        # Clean up - delete the downloaded zip and extracted files if needed
        # TODO: remove tempDir
    
if __name__ == "__main__":
    Section232Updater updater
    updater.downloadZipFile()
    updater.extractZipFile()
    updater.updateDatabase()
    updater.cleanup()
 
