from flask import Blueprint, render_template, redirect, session
from models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def root():
    # Root route should show login page directly
    if 'user_id' in session:
        return redirect('/home')
    return render_template('login.html')

@main_bp.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

@main_bp.route('/signup')
def signup_page():
    if 'user_id' in session:
        return redirect('/')
    return render_template('signup.html')

@main_bp.route('/home')
def home_page():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    # If profile is not completed, redirect to complete profile
    if not user.profile_completed:
        return redirect('/complete-profile')
    
    return render_template('home.html', user=user)


