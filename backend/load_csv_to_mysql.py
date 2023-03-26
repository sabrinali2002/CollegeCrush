import csv
import mysql.connector

# Connect to the MySQL database
cnx = mysql.connector.connect(
    user="root", password="Youyou0305!", host="localhost", database="clush"
)
cursor = cnx.cursor()

# Open the CSV file and read the headers and data types
with open(
    "/Users/jayfeng/Documents/GitHub/CollegeCrush/useful_data/DE_data_col_names.csv",
    newline="",
) as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    datatypes = [
        "VARCHAR(2)" for header in headers
    ]  # default data type is VARCHAR(255)
    # Modify data types as needed based on the actual data in the file

# Generate the CREATE TABLE statement
create_statement = f'CREATE TABLE CollegeScoreBoard ({", ".join([f"{header} {datatype}" for header, datatype in zip(headers, datatypes)])});'

# Execute the CREATE TABLE statement
cursor.execute(create_statement)

# Generate the ALTER TABLE statement
alter_statement = "ALTER TABLE CollegeScoreBoard\n"
for i, header in enumerate(headers):
    alter_statement += f"CHANGE COLUMN col{i+1} {header} {datatypes[i]},\n"
alter_statement = alter_statement[:-2] + ";"

# Execute the ALTER TABLE statement
cursor.execute(alter_statement)

# Close the database connection
cnx.commit()
cursor.close()
cnx.close()
