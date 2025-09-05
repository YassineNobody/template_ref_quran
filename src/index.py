from src.constantes import URL_OAUTH2, CLIENT_ID, CLIENT_SECRET, TOKEN_FILE
import time
import requests
import os
import json


def fetch_new_token() -> dict:
    """Demande un nouveau token à l'API Quran.com"""
    url = URL_OAUTH2 + "/oauth2/token" # type: ignore
    payload = {"grant_type": "client_credentials", "scope": "content"}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

    response = requests.post(url, data=payload, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET)) # type: ignore
    response.raise_for_status()
    data = response.json()

    # On ajoute la date d'expiration en timestamp absolu
    data["expires_at"] = int(time.time()) + data["expires_in"]

    # Sauvegarde dans un fichier JSON
    with open(TOKEN_FILE, "w") as f: #type: ignore
        json.dump(data, f)

    return data


def load_token() -> dict:
    """Charge un token depuis le fichier si valide, sinon en récupère un nouveau"""
    if os.path.exists(TOKEN_FILE): #type:ignore
        with open(TOKEN_FILE, "r") as f: #type:ignore
            token_data = json.load(f)

        # Vérifie si encore valide (ajout d'une marge de 30 sec pour éviter les erreurs)
        if token_data.get("expires_at", 0) > int(time.time()) + 30:
            return token_data

    # Sinon, on refait une requête
    return fetch_new_token()


def get_access_token() -> str:
    """Retourne le token actif"""
    token_data = load_token()
    return token_data["access_token"]

