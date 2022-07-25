import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GENDER = "male"
WEIGHT_KG = 65
HEIGHT_CM = 167
AGE = 32

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]
nutritionix_endpoint = "https://trackapi.nutritionix.com"

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

exercise_endpoint = f"{nutritionix_endpoint}/v2/natural/exercise"

headers_nutritionix = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

TOKEN = os.environ["TOKEN"]
bearer_headers = {
    "Authorization": f"Bearer {TOKEN}"
}

data = {
    "query": input("Tell me witch exercises you did? "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=data, headers=headers_nutritionix)
response.raise_for_status()
exercise_data = response.json()

for exercise in exercise_data["exercises"]:
    data_to_post = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheet_response = requests.post(url=SHEET_ENDPOINT, json=data_to_post, headers=bearer_headers)
    response.raise_for_status()
