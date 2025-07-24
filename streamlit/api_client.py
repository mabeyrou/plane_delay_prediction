from dotenv import load_dotenv
from loguru import logger
from os import getenv
import requests

load_dotenv()

API_URL = getenv("API_URL")


def predict(form_data):
    try:
        response = requests.post(url=f"{API_URL}/predict", json=form_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        logger.error(f"Erreur HTTP lors de la prédiction : {error}")
        return {
            "success": False,
            "message": f"Erreur HTTP lors de la prédiction: {error}",
        }
    except Exception as error:
        logger.error(f"Erreur lors de la prédiction : {error}")
        return {"success": False, "message": f"Erreur lors de la prédiction: {error}"}
