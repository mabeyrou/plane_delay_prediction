import streamlit as st
from datetime import datetime, time
import api_client

st.title("Prédiction de retard de vol")


def time_to_hhmm(t: time) -> int:
    return t.hour * 100 + t.minute


with st.form("flight_form"):
    flight_date = st.date_input("Date du vol", value=datetime.now())
    unique_carrier = st.selectbox(
        "Identifiant de la compagnie aérienne", options=["AA"]
    )
    origin = st.selectbox("Code IATA de l'aéroport de départ", options=["JFK"])
    dest = st.selectbox("Code IATA de l'aéroport d'arrivée", options=["JFK"])
    crs_dep_time = st.time_input("Heure prévue du départ", time(9, 5))
    dep_time = st.time_input("Heure effective du départ", time(9, 5))
    dep_delay = st.number_input(
        "Retard au départ (en minutes)", max_value=1800, value=0, step=5
    )
    taxi_out = st.number_input(
        "Temps de roulage avant le décollage",
        min_value=0,
        max_value=60,
        value=5,
        step=5,
    )
    wheels_off = st.time_input("Heure de décollage", time(9, 15))
    crs_arr_time = st.time_input(
        "Heure d'arrivée prévue (en minutes)",
    )
    crs_elapsed_time = st.number_input(
        "Durée prévue du vol (en minutes)", value=60, step=10
    )
    distance = st.number_input("Distance du trajet (en miles)", value=1000)
    submit = st.form_submit_button("Prédire")

    if submit:
        month = flight_date.month
        day_of_month = flight_date.day
        day_of_week = flight_date.isoweekday()

        input = {
            "MONTH": month,
            "DAY_OF_MONTH": day_of_month,
            "DAY_OF_WEEK": day_of_week,
            "UNIQUE_CARRIER": unique_carrier,
            "ORIGIN": origin,
            "DEST": dest,
            "CRS_DEP_TIME": time_to_hhmm(crs_dep_time),
            "DEP_TIME": time_to_hhmm(dep_time),
            "DEP_DELAY": dep_delay,
            "TAXI_OUT": taxi_out,
            "WHEELS_OFF": time_to_hhmm(wheels_off),
            "CRS_ARR_TIME": time_to_hhmm(crs_arr_time),
            "CRS_ELAPSED_TIME": crs_elapsed_time,
            "DISTANCE": distance,
        }

        response = api_client.predict(input)
        st.write("Résultat de la prédiction :")
        if "error" in response:
            st.error(f"Erreur lors de la prédiction : {response['error']}")
        else:
            prediction = response.get("prediction")
            prediction_formatted = "Retardé" if prediction == 1 else "À l'heure"
            probability = response.get("probability")
            st.write(f"Prédiction : {prediction_formatted}")
            st.write(f"Probabilité : {probability}")
