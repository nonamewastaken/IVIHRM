from flask import render_template, redirect, session
from models import User
from core.auth import login_required
from . import salary_bp
from datetime import datetime


def get_sample_overview_data():
    """Return pseudo overview statistics for salary management."""
    current_year = datetime.now().year
    return {
        'summary_cards': [
            {'title': 'Total Payroll (YTD)', 'value': '$8,420,000', 'delta': '+6.2%', 'trend': 'up'},
            {'title': 'Average Salary', 'value': '$5,610', 'delta': '+3.4%', 'trend': 'up'},
            {'title': 'Payroll Pending Approval', 'value': '$216,450', 'delta': '-12.5%', 'trend': 'down'},
            {'title': 'Employees Paid', 'value': '148', 'delta': '+4', 'trend': 'up'},
        ],
        'monthly_trend': [
            {'month': 'Jan', 'amount': 640000},
            {'month': 'Feb', 'amount': 655000},
            {'month': 'Mar', 'amount': 672500},
            {'month': 'Apr', 'amount': 701200},
            {'month': 'May', 'amount': 724300},
            {'month': 'Jun', 'amount': 743800},
        ],
        'department_breakdown': [
            {'name': 'Engineering', 'amount': 289000, 'headcount': 52},
            {'name': 'Sales', 'amount': 176500, 'headcount': 28},
            {'name': 'Operations', 'amount': 142400, 'headcount': 24},
            {'name': 'Customer Success', 'amount': 121900, 'headcount': 20},
        ],
        'alerts': [
            {'title': 'Upcoming Payroll Deadline', 'description': 'Monthly payroll closes in 3 days', 'severity': 'warning'},
            {'title': 'Expiring Contracts', 'description': '4 contractor agreements end this month', 'severity': 'info'},
        ],
        'as_of_year': current_year,
    }


def get_sample_component_data():
    """Return pseudo salary component allocations."""
    return {
        'component_split': [
            {'label': 'Base Salary', 'percentage': 68, 'color': '#4c6ef5'},
            {'label': 'Bonuses', 'percentage': 15, 'color': '#845ef7'},
            {'label': 'Allowances', 'percentage': 9, 'color': '#f76707'},
            {'label': 'Overtime', 'percentage': 5, 'color': '#20c997'},
            {'label': 'Benefits', 'percentage': 3, 'color': '#0ca678'},
        ],
        'basic_salary_grades': [
            {'grade': 'Grade A - Senior', 'hourly_rate': '$28.50', 'monthly_base': '$4,950', 'band': 'Leadership'},
            {'grade': 'Grade B - Mid', 'hourly_rate': '$22.75', 'monthly_base': '$3,950', 'band': 'Professional'},
            {'grade': 'Grade C - Associate', 'hourly_rate': '$18.10', 'monthly_base': '$3,140', 'band': 'Skilled'},
            {'grade': 'Grade D - Entry', 'hourly_rate': '$14.25', 'monthly_base': '$2,470', 'band': 'Support'},
        ],
        'allowance_details': [
            {'name': 'Housing Allowance', 'per_employee': '$320', 'eligibility': 'All full-time employees'},
            {'name': 'Transport Allowance', 'per_employee': '$150', 'eligibility': 'On-site teams'},
            {'name': 'Meal Subsidy', 'per_employee': '$80', 'eligibility': 'All employees'},
            {'name': 'Health & Wellness', 'per_employee': '$60', 'eligibility': 'After 6 months tenure'},
        ],
        'deductions': [
            {'name': 'Social Insurance', 'basis': 'Gross Salary', 'percentage': '8%', 'notes': 'Employer matched'},
            {'name': 'Health Insurance', 'basis': 'Gross Salary', 'percentage': '1.5%', 'notes': 'Mandatory'},
            {'name': 'Unemployment Fund', 'basis': 'Gross Salary', 'percentage': '1%', 'notes': 'Mandatory'},
            {'name': 'Union Fees', 'basis': 'Net Salary', 'percentage': '0.5%', 'notes': 'Unionized staff'},
        ],
        'bonus_programs': [
            {'program': 'Quarterly Performance Bonus', 'average_payout': '$850', 'participants': 42, 'status': 'Scheduled'},
            {'program': 'Sales Incentive Plan', 'average_payout': '$1,450', 'participants': 18, 'status': 'Processing'},
            {'program': 'Retention Bonus', 'average_payout': '$1,200', 'participants': 6, 'status': 'Completed'},
        ],
    }

def get_sample_attendance_data():
    return [
        {
            'label': 'July 2025',
            'rows': [
                {'index': 1, 'employee': 'Lan Pham', 'position': 'HR Business Partner', 'days': 22},
                {'index': 2, 'employee': 'Hanh Do', 'position': 'Engineering Manager', 'days': 21},
                {'index': 3, 'employee': 'Linh Hoang', 'position': 'Client Success Lead', 'days': 20},
                {'index': 4, 'employee': 'Bao Le', 'position': 'Platform Lead', 'days': 19}
            ]
        },
        {
            'label': 'June 2025',
            'rows': [
                {'index': 1, 'employee': 'Lan Pham', 'position': 'HR Business Partner', 'days': 21},
                {'index': 2, 'employee': 'Hanh Do', 'position': 'Engineering Manager', 'days': 20},
                {'index': 3, 'employee': 'Bao Le', 'position': 'Platform Lead', 'days': 20},
                {'index': 4, 'employee': 'Mai Pham', 'position': 'Onboarding Specialist', 'days': 18}
            ]
        }
    ]

@salary_bp.route('/salary')
@login_required
def salary_dashboard():
    """Salary Management Dashboard - redirects to overview"""
    return redirect('/salary/overview')


@salary_bp.route('/salary/overview')
@login_required
def salary_overview():
    """Salary overview with pseudo analytics data."""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    overview_payload = get_sample_overview_data()
    component_preview = get_sample_component_data()['component_split']

    return render_template(
        'salary_overview.html',
        user=user,
        overview=overview_payload,
        component_preview=component_preview
    )


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
    
    return render_template('payroll_list.html', user=user, attendance_data=get_sample_attendance_data())

@salary_bp.route('/salary/slips')
@login_required
def salary_slips():
    """Salary Slips Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('salary_slips.html', user=user)


@salary_bp.route('/salary/basic')
@login_required
def salary_basic():
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    data = get_sample_component_data()
    return render_template(
        'salary/basic_salary.html',
        user=user,
        grades=data['basic_salary_grades'],
        component_split=data['component_split']
    )


@salary_bp.route('/salary/allowances')
@login_required
def salary_allowances():
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    data = get_sample_component_data()
    return render_template(
        'salary/allowances.html',
        user=user,
        allowances=data['allowance_details']
    )


@salary_bp.route('/salary/deductions')
@login_required
def salary_deductions():
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    data = get_sample_component_data()
    return render_template(
        'salary/deductions.html',
        user=user,
        deductions=data['deductions']
    )


@salary_bp.route('/salary/bonuses')
@login_required
def salary_bonuses():
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    data = get_sample_component_data()
    return render_template(
        'salary/bonuses.html',
        user=user,
        bonuses=data['bonus_programs']
    )
