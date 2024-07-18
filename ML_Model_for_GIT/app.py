# import streamlit as st
# import pandas as pd
# import numpy as np
# import datetime
# import pickle

# # Define constants for the app
# CITIES = ['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
# AIRLINES = ['AirAsia', 'AkasaAir', 'AllianceAir', 'GO FIRST', 'Indigo', 'SpiceJet', 'StarAir', 'Vistara', 'Air India']
# FLIGHT_CLASSES = ['ECONOMY', 'PREMIUMECONOMY', 'BUSINESS', 'FIRST']
# STOPS = ['0-stop', '1-stop', '2-stop']

# # Ordinal encoding order for airlines
# ordinal_order = {
#     'AkasaAir': 0,
#     'AllianceAir': 1,
#     'AirAsia': 2,
#     'GO FIRST': 3,
#     'SpiceJet': 4,
#     'Indigo': 5,
#     'StarAir': 6,
#     'Air India': 7,
#     'Vistara': 8
# }

# def main():
#     st.title("Flight-Price-Prediction")
#     st.write(" *--Built using StreamLit--* ")

#     # Sidebar for Departure Details
#     st.sidebar.subheader("Select Departure")
#     today = pd.to_datetime("today")
#     dep_date = st.sidebar.date_input("Departure Date", today)
#     dep_hour = st.sidebar.selectbox("Departure Hour", list(range(24)))
#     dep_minute = st.sidebar.selectbox("Departure Minute", list(range(60)))

#     # Sidebar for Arrival Details
#     st.sidebar.subheader("Select Arrival")
#     arr_hour = st.sidebar.selectbox("Arrival Hour", list(range(24)))
#     arr_minute = st.sidebar.selectbox("Arrival Minute", list(range(60)))

#     # Display Departure and Arrival Times
#     st.subheader("Selected Departure and Arrival Times")
#     st.write(f"Departure Time: {dep_hour:02d}:{dep_minute:02d}")
#     st.write(f"Arrival Time: {arr_hour:02d}:{arr_minute:02d}")

#     # Source and Destination
#     st.subheader("Select Flight Route")
#     source_city = st.selectbox("Departure City", CITIES)
#     dest_city = st.selectbox("Arrival City", [city for city in CITIES if city != source_city])

#     st.write(f"Source: {source_city}")
#     st.write(f"Destination: {dest_city}")

#     # Airline selection
#     st.subheader("Select Airline")
#     airline = st.selectbox("Airline Company", AIRLINES)
#     st.write(f"Airline: {airline}")

#     # Flight class selection
#     st.subheader("Select Flight Class")
#     flight_class = st.selectbox("Flight Class", FLIGHT_CLASSES)
#     st.write(f"Flight Class: {flight_class}")

#     # Total Stops selection
#     st.subheader("Select Total Stops")
#     total_stops = st.selectbox("Total Stops", STOPS)
#     st.write(f"Total Stops: {total_stops}")

#     # Calculate Journey_Day, Journey_Month, Journey_DOW
#     journey_day = dep_date.day
#     journey_month = dep_date.month
#     journey_dow = dep_date.weekday()

#     # Calculate Duration
#     dep_time = datetime.datetime.combine(dep_date, datetime.time(dep_hour, dep_minute))
#     arr_time = datetime.datetime.combine(dep_date, datetime.time(arr_hour, arr_minute))
#     duration = (arr_time - dep_time).seconds / 60
#     if duration < 0:
#         duration += 24 * 60  # adjust for overnight flights

#     st.subheader("Flight Duration")
#     st.write(f"Duration: {duration} minutes")

#     # Ordinal encoding for airline
#     airline_encoded = ordinal_order[airline]

#     # One-hot encoding for departure city and arrival city
#     departure_city_encoded = {f'Departure_City_{city}': 1 if city == source_city else 0 for city in CITIES}
#     arrival_city_encoded = {f'Arrival_City_{city}': 1 if city == dest_city else 0 for city in CITIES}

#     # Ordinal encoding for flight class
#     flight_class_mapping = {'ECONOMY': 1, 'PREMIUMECONOMY': 2, 'BUSINESS': 3, 'FIRST': 4}
#     flight_class_encoded = flight_class_mapping[flight_class]

#     # Label encoding for total stops
#     total_stops_mapping = {'0-stop': 0, '1-stop': 1, '2-stop': 2}
#     total_stops_encoded = total_stops_mapping[total_stops]

#     # Prepare input data
#     input_data = {
#         'Duration_in_mins': duration,
#         'Total Stops': total_stops_encoded,
#         'Journey_Day': journey_day,
#         'Journey_Month': journey_month,
#         'Dep_Hour': dep_hour,
#         'Dep_Minute': dep_minute,
#         'Arrival_Hour': arr_hour,
#         'Arrival_Minute': arr_minute,
#         'Departure_City_Bangalore': departure_city_encoded['Departure_City_Bangalore'],
#         'Departure_City_Chennai': departure_city_encoded['Departure_City_Chennai'],
#         'Departure_City_Delhi': departure_city_encoded['Departure_City_Delhi'],
#         'Departure_City_Hyderabad': departure_city_encoded['Departure_City_Hyderabad'],
#         'Departure_City_Kolkata': departure_city_encoded['Departure_City_Kolkata'],
#         'Departure_City_Mumbai': departure_city_encoded['Departure_City_Mumbai'],
#         'Arrival_City_Bangalore': arrival_city_encoded['Arrival_City_Bangalore'],
#         'Arrival_City_Chennai': arrival_city_encoded['Arrival_City_Chennai'],
#         'Arrival_City_Delhi': arrival_city_encoded['Arrival_City_Delhi'],
#         'Arrival_City_Hyderabad': arrival_city_encoded['Arrival_City_Hyderabad'],
#         'Arrival_City_Kolkata': arrival_city_encoded['Arrival_City_Kolkata'],
#         'Arrival_City_Mumbai': arrival_city_encoded['Arrival_City_Mumbai'],
#         'Ordinal_Airline': airline_encoded,
#         'Flight_Class_Encoded': flight_class_encoded
#     }

#     # Ensure the input data matches the model's expected features
#     input_df = pd.DataFrame([input_data])
#     model_features = [
#         'Duration_in_mins', 'Total Stops', 'Journey_Day', 'Journey_Month',
#         'Dep_Hour', 'Dep_Minute', 'Arrival_Hour', 'Arrival_Minute',
#         'Departure_City_Bangalore', 'Departure_City_Chennai',
#         'Departure_City_Delhi', 'Departure_City_Hyderabad',
#         'Departure_City_Kolkata', 'Departure_City_Mumbai',
#         'Arrival_City_Bangalore', 'Arrival_City_Chennai',
#         'Arrival_City_Delhi', 'Arrival_City_Hyderabad',
#         'Arrival_City_Kolkata', 'Arrival_City_Mumbai',
#         'Ordinal_Airline', 'Flight_Class_Encoded'
#     ]
#     input_df = input_df[model_features]

#     # Load the model
#     model = pickle.load(open("linear_reg_model.pkl", "rb"))

#     # Prediction button
#     if st.button("Predict Price"):
#         prediction = model.predict(input_df)
#         st.subheader("Predicted Price")
#         # st.write(input_df)
#         st.write(f"₹{prediction[0]:.2f}")

# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pickle

# Define constants for the app
CITIES = ['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
AIRLINES = ['AirAsia', 'AkasaAir', 'AllianceAir', 'GO FIRST', 'Indigo', 'SpiceJet', 'StarAir', 'Vistara', 'Air India']
FLIGHT_CLASSES = ['ECONOMY', 'PREMIUMECONOMY', 'BUSINESS', 'FIRST']
STOPS = ['0-stop', '1-stop', '2-stop']

# Ordinal encoding order for airlines
ordinal_order = {
    'AkasaAir': 0,
    'AllianceAir': 1,
    'AirAsia': 2,
    'GO FIRST': 3,
    'SpiceJet': 4,
    'Indigo': 5,
    'StarAir': 6,
    'Air India': 7,
    'Vistara': 8
}

def main():
    st.title("Flight-Price-Prediction")
    st.write(" *--Built using StreamLit--* ")

    # Sidebar for Departure Details
    st.sidebar.subheader("Select Departure")
    today = pd.to_datetime("today")
    dep_date = st.sidebar.date_input("Departure Date", today)
    dep_hour = st.sidebar.selectbox("Departure Hour", list(range(24)))
    dep_minute = st.sidebar.selectbox("Departure Minute", list(range(60)))

    # Sidebar for Arrival Details
    st.sidebar.subheader("Select Arrival")
    arr_hour = st.sidebar.selectbox("Arrival Hour", list(range(24)))
    arr_minute = st.sidebar.selectbox("Arrival Minute", list(range(60)))

    # Display Departure and Arrival Times
    st.subheader("Selected Departure and Arrival Times")
    st.write(f"Departure Time: {dep_hour:02d}:{dep_minute:02d}")
    st.write(f"Arrival Time: {arr_hour:02d}:{arr_minute:02d}")

    # Source and Destination
    st.subheader("Select Flight Route")
    source_city = st.selectbox("Departure City", CITIES)
    dest_city = st.selectbox("Arrival City", [city for city in CITIES if city != source_city])

    st.write(f"Source: {source_city}")
    st.write(f"Destination: {dest_city}")

    # Airline selection
    st.subheader("Select Airline")
    airline = st.selectbox("Airline Company", AIRLINES)
    st.write(f"Airline: {airline}")

    # Flight class selection
    st.subheader("Select Flight Class")
    flight_class = st.selectbox("Flight Class", FLIGHT_CLASSES)
    st.write(f"Flight Class: {flight_class}")

    # Total Stops selection
    st.subheader("Select Total Stops")
    total_stops = st.selectbox("Total Stops", STOPS)
    st.write(f"Total Stops: {total_stops}")

    # Calculate Journey_Day, Journey_Month, Journey_DOW
    journey_day = dep_date.day
    journey_month = dep_date.month
    journey_dow = dep_date.weekday()

    # Calculate Duration
    dep_time = datetime.datetime.combine(dep_date, datetime.time(dep_hour, dep_minute))
    arr_time = datetime.datetime.combine(dep_date, datetime.time(arr_hour, arr_minute))
    duration = (arr_time - dep_time).seconds / 60
    if duration < 0:
        duration += 24 * 60  # adjust for overnight flights

    st.subheader("Flight Duration")
    st.write(f"Duration: {duration} minutes")

    # Check if duration is less than 100 minutes
    if duration < 100:
        st.error("The duration of the flight must be at least 100 minutes.")
        return

    # Ordinal encoding for airline
    airline_encoded = ordinal_order[airline]

    # One-hot encoding for departure city and arrival city
    departure_city_encoded = {f'Departure_City_{city}': 1 if city == source_city else 0 for city in CITIES}
    arrival_city_encoded = {f'Arrival_City_{city}': 1 if city == dest_city else 0 for city in CITIES}

    # Ordinal encoding for flight class
    flight_class_mapping = {'ECONOMY': 1, 'PREMIUMECONOMY': 2, 'BUSINESS': 3, 'FIRST': 4}
    flight_class_encoded = flight_class_mapping[flight_class]

    # Label encoding for total stops
    total_stops_mapping = {'0-stop': 0, '1-stop': 1, '2-stop': 2}
    total_stops_encoded = total_stops_mapping[total_stops]

    # Prepare input data
    input_data = {
        'Duration_in_mins': duration,
        'Total Stops': total_stops_encoded,
        'Journey_Day': journey_day,
        'Journey_Month': journey_month,
        'Dep_Hour': dep_hour,
        'Dep_Minute': dep_minute,
        'Arrival_Hour': arr_hour,
        'Arrival_Minute': arr_minute,
        'Departure_City_Bangalore': departure_city_encoded['Departure_City_Bangalore'],
        'Departure_City_Chennai': departure_city_encoded['Departure_City_Chennai'],
        'Departure_City_Delhi': departure_city_encoded['Departure_City_Delhi'],
        'Departure_City_Hyderabad': departure_city_encoded['Departure_City_Hyderabad'],
        'Departure_City_Kolkata': departure_city_encoded['Departure_City_Kolkata'],
        'Departure_City_Mumbai': departure_city_encoded['Departure_City_Mumbai'],
        'Arrival_City_Bangalore': arrival_city_encoded['Arrival_City_Bangalore'],
        'Arrival_City_Chennai': arrival_city_encoded['Arrival_City_Chennai'],
        'Arrival_City_Delhi': arrival_city_encoded['Arrival_City_Delhi'],
        'Arrival_City_Hyderabad': arrival_city_encoded['Arrival_City_Hyderabad'],
        'Arrival_City_Kolkata': arrival_city_encoded['Arrival_City_Kolkata'],
        'Arrival_City_Mumbai': arrival_city_encoded['Arrival_City_Mumbai'],
        'Ordinal_Airline': airline_encoded,
        'Flight_Class_Encoded': flight_class_encoded
    }

    # Ensure the input data matches the model's expected features
    input_df = pd.DataFrame([input_data])
    model_features = [
        'Duration_in_mins', 'Total Stops', 'Journey_Day', 'Journey_Month',
        'Dep_Hour', 'Dep_Minute', 'Arrival_Hour', 'Arrival_Minute',
        'Departure_City_Bangalore', 'Departure_City_Chennai',
        'Departure_City_Delhi', 'Departure_City_Hyderabad',
        'Departure_City_Kolkata', 'Departure_City_Mumbai',
        'Arrival_City_Bangalore', 'Arrival_City_Chennai',
        'Arrival_City_Delhi', 'Arrival_City_Hyderabad',
        'Arrival_City_Kolkata', 'Arrival_City_Mumbai',
        'Ordinal_Airline', 'Flight_Class_Encoded'
    ]
    input_df = input_df[model_features]

    # Load the model
    model = pickle.load(open("linear_reg_model.pkl", "rb"))

    # Prediction button
    if st.button("Predict Price"):
        prediction = model.predict(input_df)
        st.subheader("Predicted Price")
        st.write(f"₹{prediction[0]:.2f}")

if __name__ == "__main__":
    main()
