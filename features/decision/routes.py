from flask import render_template, redirect, session
from models import User
from core.auth import login_required
from . import decision_bp

@decision_bp.route('/decision')
@login_required
def decision_dashboard():
    """Decision Management Dashboard"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('decision_dashboard.html', user=user)

@decision_bp.route('/decision/create')
@login_required
def create_decision():
    """Create Decision Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('create_decision.html', user=user)

@decision_bp.route('/decision/list')
@login_required
def decision_list():
    """Decision List Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('decision_list.html', user=user)

@decision_bp.route('/decision/hiring')
@login_required
def hiring_decisions():
    """Hiring Decisions Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('hiring_decisions.html', user=user)
