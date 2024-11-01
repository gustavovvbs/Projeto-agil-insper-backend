from functools import wraps 
from flask import request, jsonify
from .jwt_auth import decode_jwt_token

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"error": "Token is missing"}), 
            user_data = decode_jwt_token(token.split(' ')[1])
            if isinstance(user_data, str):
                return jsonify({"error": user_data}), 403
            
            user_role = user_data.get('role')
            if user_role not in allowed_roles:
                return jsonify({"error": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
 

