import streamlit as st
import requests
from loguru import logger

logger.remove()
logger.add(
    "logs/local_streamlit.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="TRACE",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

AI_API_URL = "http://ai-api:8000"  # adapt if needed

st.title("Socio-demographic Form")

with st.form("profile_form"):
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    workclass = st.selectbox(
        "Employment status",
        [
            "Federal-gov",
            "Local-gov",
            "Never-worked",
            "Private",
            "Self-emp-inc",
            "Self-emp-not-inc",
            "State-gov",
            "Without-pay",
        ],
    )
    education = st.selectbox(
        "Education Level",
        [
            "Preschool",
            "1st-4th",
            "5th-6th",
            "7th-8th",
            "9th",
            "10th",
            "11th",
            "12th",
            "HS-grad",
            "Some-college",
            "Assoc-acdm",
            "Assoc-voc",
            "Bachelors",
            "Masters",
            "Prof-school",
            "Doctorate",
        ],
    )
    education_num = st.number_input(
        "Education level (numeric)", min_value=1, max_value=20, value=10
    )
    marital_status = st.selectbox(
        "Marital status",
        [
            "Divorced",
            "Married-AF-spouse",
            "Married-civ-spouse",
            "Married-spouse-absent",
            "Never-married",
            "Separated",
            "Widowed",
        ],
    )
    occupation = st.selectbox(
        "Occupation",
        [
            "Adm-clerical",
            "Armed-Forces",
            "Craft-repair",
            "Exec-managerial",
            "Farming-fishing",
            "Handlers-cleaners",
            "Machine-op-inspct",
            "Other-service",
            "Priv-house-serv",
            "Prof-specialty",
            "Protective-serv",
            "Sales",
            "Tech-support",
            "Transport-moving",
            "?",
        ],
    )
    capital_gain = st.number_input("Capital gain", min_value=0, value=0)
    capital_loss = st.number_input("Capital loss", min_value=0, value=0)
    hours_per_week = st.number_input(
        "Hours per week", min_value=1, max_value=100, value=40
    )

    submitted = st.form_submit_button("Predict")

if submitted:
    data = {
        "age": age,
        "workclass_name": workclass,
        "education_name": education,
        "education_num": education_num,
        "marital_status_name": marital_status,
        "occupation_name": occupation,
        "capital_gain": capital_gain,
        "capital_loss": capital_loss,
        "hours_per_week": hours_per_week,
    }
    try:
        # Send data to the AI API
        response = requests.post(f"{AI_API_URL}/predict", json=data)
        if response.status_code == 200:
            st.success("Profile successfully registered!")
            st.json(response.json())
        else:
            st.error(f"Error during prediction: {response.text}")
    except Exception as e:
        st.error(f"Connection error to the AI API: {e}")
