from functools import wraps
from flask import request, jsonify
from src.config import Config

def restrict_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for custom header (sent by React app)
        app_key = request.headers.get('X-React-App-Key')
        if not app_key or app_key != Config.REACT_APP_KEY:
            return jsonify({"error": "Unauthorized: Invalid or missing app key"}), 403

        return f(*args, **kwargs)
    return decorated_function