# import _sqlite3

# # connect to sqlite
# connection = sqlite3.connect("student.db")

# cursor = connection.cursor()

# # creation of table
# table_info = """
# CREATE TABLE STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
# SECTION VARCHAR(25), MARKS INT);

# """

# cursor.execute(table_info)

# # Insert some more records

# # Queries to INSERT records. 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Krish', 'Data Science', 'A', 90)''') 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Sudhanshu', 'Data Science', 'B', 100)''') 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Darius', 'Devops', 'A', 86)''') 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Vikash', 'DEVOPS', 'A', 50)''') 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Dipesh', 'DEVOPS', 'A', 35)''') 

# # Display all the recordsprint
# print("Inserted Records are: ")
# data = cursor.execute('''SELECT * FROM STUDENT''')

# for row in data:
#     print(row)

# ### Close the connection
# connection.commit()
# connection.close()


#<--------------------------------------------------------------->

import pandas as pd
import sqlite3

# Load the CSV file into a DataFrame
df = pd.read_csv('part-merged_1_null_removed.csv')

# Rename the column 'Total Stops' to 'Total_Stops'
df.rename(columns={'Total Stops': 'Total_Stops'}, inplace=True)

# Convert date columns to datetime format
df['StandardDateofBooking'] = pd.to_datetime(df['StandardDateofBooking'])
df['StandardDateofJourney'] = pd.to_datetime(df['StandardDateofJourney'])

# Connect to SQLite database
connection = sqlite3.connect("flight_fare.db")
cursor = connection.cursor()

# Create the table (adjust column names and types as per your CSV file)
cursor.execute("""
CREATE TABLE IF NOT EXISTS FLIGHT_FARE (
    StandardDateofBooking TEXT,
    StandardDateofJourney TEXT,
    Month_of_Journey INTEGER,
    Airline_Company TEXT,
    Flight_Number TEXT,
    Flight_Class TEXT,
    Departure_Time TEXT,
    Departure_City TEXT,
    Arrival_Time TEXT,
    Arrival_City TEXT,
    Duration_in_mins REAL,
    Total_Stops TEXT,
    Price REAL
);
""")

# Write the data into the SQLite database
df.to_sql('FLIGHT_FARE', connection, if_exists='append', index=False)

# Commit and close the connection
connection.commit()
connection.close()

print("CSV data has been successfully written to the SQLite database.")


