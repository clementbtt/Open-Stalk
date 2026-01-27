from flask import session, redirect, url_for
from functools import wraps
class SessionManager:

    def protect_endpoint(self, endpoint_function:callable):
        @wraps(endpoint_function)
        def wrapper(*args, **kwargs):
            if session.get("authenticated"):
                return endpoint_function(*args, **kwargs)
            return redirect(url_for("user.show_login")) 
        return wrapper