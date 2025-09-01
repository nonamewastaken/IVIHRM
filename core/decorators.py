from functools import wraps
from flask import session, redirect, jsonify

def redirect_if_logged_in(f):
    """Decorator to redirect logged-in users away from auth pages"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            return redirect('/dashboard')
        return f(*args, **kwargs)
    return decorated_function
