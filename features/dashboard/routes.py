from flask import render_template, redirect, session
from models import User
from core.auth import login_required
from . import dashboard_bp

@dashboard_bp.route('/')
def root():
    """Root route should show login page directly"""
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/login')

@dashboard_bp.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@dashboard_bp.route('/signup')
def signup_page():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('signup.html')

@dashboard_bp.route('/home')
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
    
    company_name = user.organization.name if user.organization else "Your Company"
    return render_template('dashboard.html', user_name=user.name, company_name=company_name)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # If profile is not completed, redirect to complete profile
    if not user.profile_completed:
        return redirect('/complete-profile')
    
    company_name = user.organization.name if user.organization else "Your Company"
    return render_template('dashboard.html', user_name=user.name, company_name=company_name)
