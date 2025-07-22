import os
import pandas as pd
import requests

from config import DATA_API_URL


def fetch_all_profiles_from_api(page_size: int = 100) -> pd.DataFrame:
    """
    Récupère tous les profils socio-démographiques depuis l'API de données
    en gérant la pagination.

    Args:
        page_size (int): Le nombre d'éléments à récupérer par requête.

    Returns:
        pd.DataFrame: Un DataFrame contenant tous les profils.
    """
    all_profiles = []
    current_page = 0

    print(f"Début de la récupération des données depuis {DATA_API_URL}...")

    while True:
        skip = current_page * page_size

        request_url = f"{DATA_API_URL}/profiles/?skip={skip}&limit={page_size}"

        try:
            response = requests.get(request_url)
            response.raise_for_status()

            data = response.json()

            if not data:
                print("Toutes les données ont été récupérées.")
                break

            all_profiles.extend(data)

            current_page += 1

        except requests.exceptions.RequestException as err:
            print(f"Erreur lors de la communication avec l'API de données : {err}")
            return pd.DataFrame()

    return pd.DataFrame(all_profiles)


if __name__ == "__main__":
    profiles_df = fetch_all_profiles_from_api()

    if not profiles_df.empty:
        print("\nAperçu des données récupérées :")
        print(profiles_df.head())
        print(f"\n{len(profiles_df)} profils au total ont été chargés.")

        # Ici, tu peux commencer le prétraitement et l'entraînement de ton modèle
        # ...
        # X = profiles_df.drop("income", axis=1)
        # y = profiles_df["income"]
        # ...
