import csv

# Open the CSV file and read the headers. Change the path.
with open(
    "/Users/jayfeng/Documents/GitHub/CollegeCrush/useful_data/DE_data.csv", newline=""
) as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)

# Write the headers to a file
with open(
    "CollegeCrush/useful_data/DE_data_col_names.txt",
    "w",
) as outfile:
    outfile.write(",".join(headers))
