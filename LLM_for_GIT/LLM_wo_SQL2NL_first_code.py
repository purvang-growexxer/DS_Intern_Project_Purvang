from dotenv import load_dotenv
load_dotenv()  # Load all environment variables 

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure API key
genai.configure(api_key = os.getenv("####"))

# Function to load Google Gemini model and provide query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)
    return rows

# Define your prompt

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name FLIGHT_FARE and has the following columns - 
    StandardDateofBooking, StandardDateofJourney, Month_of_Journey, Airline_Company, 
    Flight_Number, Flight_Class, Departure_Time, Departure_City, Arrival_Time, 
    Arrival_City, Duration_in_mins, Total_Stops, and Price.

    Description of columns:
    1) StandardDateofBooking: The date when the flight booking was made.
    Data type: Date (format: YYYY-MM-DD)

    2) StandardDateofJourney: The date of the flight journey.
    Data type: Date (format: YYYY-MM-DD)

    3) Month_of_Journey: The month of the flight journey.
    Data type: Integer

    4) Airline_Company: The name of the airline company operating the flight.
    Data type: String

    5) Flight_Number: Flight_Number Name given for a flight.
    Data type: String

    6) Flight_Class: The class of the flight, such as Economy, Business,First, Premiumeconomy. In my dataset price according to flight_class are in below format. First > Business > Premiumeconomy > economy
    Data type: String

    7) Departure_Time: The departure time of the flight.
    Data type: String (format: HH)

    8) Departure_City: The city from which the flight departs.
    Data type: String

    9) Arrival_Time: The arrival time of the flight.
    Data type: String (format: HH)

    10) Arrival_City: The city where the flight arrives.
    Data type: String

    11) Duration_in_mins: The duration of the flight in minutes.
    Data type: Integer

    12) Total_Stops: The total number of stops the flight makes, can include values such as "non-stop", "1-stop", "2+stop".
    Data type: String

    13) Price: The price of the flight ticket. This is the target column
    Data type: Integer

    For example, 
    Example-1 - How many entries of records are present?,
    the SQL command will be something like SELECT COUNT(*) FROM FLIGHT_FARE;

    Example-2 - Tell me all the flights from City A to City B?,
    the SQL command will be something like SELECT * FROM FLIGHT_FARE 
    WHERE Departure_City = 'City A' AND Arrival_City = 'City B';

    also the sql should not have ''' in the beginning or end and sql word in the output
    """
]

# Streamlit App
st.set_page_config(page_title="LLM without SQL2NL")
st.header("Give any question related to Flight Details")

question = st.text_input("Input:", key='input')
submit = st.button("Ask the Question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    response = read_sql_query(response, "flight_fare.db")
    st.subheader("The Response is: ")
    for row in response:
        print(row)
        st.header(row)
