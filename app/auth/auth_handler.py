# This file is responsible for signing , encoding , decoding and returning JWTS
import time
import jwt
import os
from dotenv import find_dotenv, load_dotenv

def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 1800
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=os.getenv("JWT_ALGORITHM"))

    return token_response(token)


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM")])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
