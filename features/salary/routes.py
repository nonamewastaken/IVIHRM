from flask import render_template, redirect, session
from models import User
from core.auth import login_required
from . import salary_bp

@salary_bp.route('/salary')
@login_required
def salary_dashboard():
    """Salary Management Dashboard"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('salary_dashboard.html', user=user)

@salary_bp.route('/salary/calculate')
@login_required
def calculate_salary():
    """Calculate Salary Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('calculate_salary.html', user=user)

@salary_bp.route('/salary/payroll')
@login_required
def payroll_list():
    """Payroll List Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('payroll_list.html', user=user)

@salary_bp.route('/salary/slips')
@login_required
def salary_slips():
    """Salary Slips Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('salary_slips.html', user=user)
