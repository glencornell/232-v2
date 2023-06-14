import requests
import zipfile
import csv
import psycopg2
import os
import shutil
import sys

class Section232Updater:
    def __init__(self):
        # constants
        self.url = 'https://232app.azurewebsites.net/data/BIS232Data.zip'
        self.tempDir = './temp/' # TODO: use mkstemp() instead
        self.zipFileName = self.tempDir + 'BIS232Data.zip'
        self.extractedDir = self.tempDir + "extracted/"
        self.conn = None
        self.cursor = None
        os.makedirs(self.tempDir, exist_ok=True)
        
    def __del__(self):
        if os.path.exists(self.tempDir):
            try:
                print(f"removing {self.tempDir}")
                # TODO: for now, while debugging, leave the temp files in place.
                #shutil.rmtree(self.tempDir)
            except:
                print(f'Error while deleting directory {self.tempDir}')
        

    def downloadZipFile(self):
        sys.stdout.write(f"Downloading the zip archive from {self.url}...")
        sys.stdout.flush()
        response = requests.get(self.url)
        with open(self.zipFileName, "wb") as zip_file:
            zip_file.write(response.content)
        print("done")

    def extractZipFile(self):
        sys.stdout.write(f"Extracting zip archive {self.zipFileName}...")
        sys.stdout.flush()
        with zipfile.ZipFile(self.zipFileName, "r") as zip_ref:
            zip_ref.extractall(self.extractedDir)
        print("done")

    def connectToDatabase(self):
        sys.stdout.write("Connecting to the database")
        sys.stdout.flush()
        conn = psycopg2.connect(database='TODO: database name',
                                user='TODO: database username',
                                password='TODO: database password',
                                host='TODO',
                                port='TODO')
        cursor = conn.cursor()
        print("done")

    def updateDatabase(self):
        csv_file = "ExclusionRequests.txt"
        sys.stdout.write(f"Processing CSV file {csv_file}")
        sys.stdout.flush()
        expected_header = [ 'column1', 'column2', 'column3' ] # TODO: replace with expected columns in cvs_file
        
        query = "INSERT INTO todo_table (column1, column2, column3) VALUES (%s, %s, %s)"

        # the number of records to read in at a time before we commit
        # to the database
        batch_size = 1000
        
        with open(self.extractedDir + csv_file, "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            # Validation check: make sure that the columns have not
            # changed from what we expect them to be.
            if header != expected_header:
                # TODO: raise an exception or return an error
                print(f"Error: {csv_file} header has changed.")
                return

            # Perform batch reads of the CSV file and update the
            # database in batches for efficiency:
            rows = []
            for row in csv_reader:
                # Read each row into memory:
                rows.append(row)

                # If the batch size has been reached, then make a
                # large commit to the database:
                if len(rows) == batch_size:
                    cursor.executemany(query, rows)
                    conn.commit()
                    rows = []
                    
            # Commit any remaining rows to the database
            if rows:
                cursor.executemany(query, rows)
                conn.commit()

        # Close the connection to the database
        cursor.close()
        conn.close()
        print("done")

if __name__ == "__main__":
    up = Section232Updater()
    up.downloadZipFile()
    up.extractZipFile()
    up.updateDatabase()
