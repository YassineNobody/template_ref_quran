import os

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
URL_OAUTH2 = os.getenv("END_POINT_OAUTH")
TOKEN_FILE = "quran_token.json"

if not CLIENT_ID or not CLIENT_SECRET or not URL_OAUTH2:
    raise ValueError("Variable introuvable")
