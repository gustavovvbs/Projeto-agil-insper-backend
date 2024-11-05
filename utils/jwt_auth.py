import jwt 
from datetime import datetime, timedelta

from config import Config 

def create_jwt_token(user_id: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "role": role
    }


    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload 
    except:
        return {"error": "Invalid token"}

