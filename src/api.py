import requests
from src.constantes import CLIENT_ID
from src.index import get_access_token

def call_quran_api(endpoint: str):
    """Appelle un endpoint de l'API Quran.com avec token valide"""
    url = f"https://apis.quran.foundation/content/api/v4{endpoint}"
    headers = {
        "Accept": "application/json",
        "x-auth-token": get_access_token(),
        "x-client-id": CLIENT_ID,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
