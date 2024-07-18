import pandas as pd
import sqlite3

# Load the CSV file into a DataFrame
df = pd.read_csv('part-merged_1.csv')

df['StandardDateofBooking'] = pd.to_datetime(df['StandardDateofBooking'])
df['StandardDateofJourney'] = pd.to_datetime(df['StandardDateofJourney'])

# # Connect to SQLite database
# connection = sqlite3.connect("flight_fare.db")
# cursor = connection.cursor()

# # Create the table (adjust column names and types as per your CSV file)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS FLIGHT_FARE (
#     AIRLINE TEXT,
#     FLIGHT_NUMBER TEXT,
#     SOURCE TEXT,
#     DESTINATION TEXT,
#     DATE TEXT,
#     PRICE REAL
# );
# """)

# # Write the data into the SQLite database
# df.to_sql('FLIGHT_FARE', connection, if_exists='append', index=False)

# # Commit and close the connection
# connection.commit()
# connection.close()

# print("CSV data has been successfully written to the SQLite database.")

df.info()