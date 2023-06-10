# 232-v2
Test of section 232 import into database
## Problem Description
I want to download a zip archive containing several very large (~2GiB) CSV files, and post the contents of these files to a postgresql database.  The zip archive is replaced once per day, so I will run this script daily.  Because the files are so large, I can’t ingest them in memory.  I only want to update the changes to each record in the database.
