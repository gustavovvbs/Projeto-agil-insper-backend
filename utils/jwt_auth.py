import jwt
from datetime import datetime, timedelta
from config import Config

def create_jwt_token(user_id: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),  # Expiry set to 24 hours from now
        "role": role
    }
    # Encoding JWT token with the payload and the secret key
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str) -> dict:
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    except Exception as e:
        # Catch other unexpected errors
        return {"error": f"An error occurred: {str(e)}"}
