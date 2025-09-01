from functools import wraps
from flask import session, redirect, jsonify
from models import User

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        
        user = User.query.get(session['user_id'])
        if not user:
            session.pop('user_id', None)
            return redirect('/login')
        
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    """Decorator to require login for API routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            session.pop('user_id', None)
            return jsonify({'error': 'User not found'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get the current logged-in user"""
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])
