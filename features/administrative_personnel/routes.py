from flask import render_template, redirect, session, request, jsonify
from models import User, Employee
from core.database import db
from core.auth import login_required
from . import administrative_personnel_bp
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

EMPLOYEE_TEXT_FIELDS = [
    'full_name',
    'gender',
    'date_of_birth',
    'place_of_birth',
    'hometown',
    'marital_status',
    'ethnicity',
    'religion',
    'personal_phone',
    'personal_email',
    'personal_tax_code',
    'social_insurance_code',
    'party_join_date',
    'party_join_place',
    'health_status',
    'emergency_contact',
    'permanent_address',
    'permanent_province',
    'permanent_ward',
    'permanent_street',
    'current_address',
    'current_province',
    'current_ward',
    'current_street',
    'id_card_number',
    'id_card_issue_date',
    'id_card_expiry_date',
    'id_card_issue_place',
    'passport_number',
    'passport_issue_date',
    'passport_expiry_date',
    'passport_issue_place'
]

EMPLOYEE_FILE_FIELDS = [
    'cv_file',
    'portrait_file',
    'health_file',
    'id_card_file',
    'passport_file'
]

ALL_EMPLOYEE_FIELDS = EMPLOYEE_TEXT_FIELDS + EMPLOYEE_FILE_FIELDS


def empty_to_none(value):
    """Normalize incoming payload values, converting blank strings to None."""
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else None
    return value


def sanitize_employee_payload(data, include_missing=True):
    """Return sanitized employee data ready for persistence."""
    sanitized = {}
    for field in ALL_EMPLOYEE_FIELDS:
        if include_missing or field in data:
            sanitized[field] = empty_to_none(data.get(field))
    return sanitized

@administrative_personnel_bp.route('/personnel')
@login_required
def personnel_overview():
    """Administrative personnel landing page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    employees = Employee.query.order_by(Employee.created_at.desc()).all()
    headcount = len(employees)
    completed_profiles = sum(1 for e in employees if has_completed_profile(e))
    docs_pending = sum(1 for e in employees if has_document_gap(e))
    recent_hires = [e for e in employees if is_recent_hire(e)]

    summary_cards = [
        {'icon': 'fas fa-users', 'label': 'Total Employees', 'value': headcount},
        {'icon': 'fas fa-user-check', 'label': 'Profiles Completed', 'value': f"{percentage(completed_profiles, headcount)}%"},
        {'icon': 'fas fa-file-circle-exclamation', 'label': 'Docs Pending', 'value': docs_pending},
        {'icon': 'fas fa-user-plus', 'label': 'New Hires (30d)', 'value': len(recent_hires)},
    ]

    quick_actions = [
        {'icon': 'fas fa-user-plus', 'label': 'Add Employee', 'href': '/personnel/add'},
        {'icon': 'fas fa-users', 'label': 'View Employees', 'href': '/personnel/list'},
        {'icon': 'fas fa-building', 'label': 'Departments', 'href': '/personnel/departments'},
        {'icon': 'fas fa-file-contract', 'label': 'Create Decision', 'href': '/decision/create'},
    ]

    highlights = build_highlights(employees, completed_profiles, docs_pending)
    attention = build_attention_list(employees)
    activity = build_recent_activity(employees)
    onboarding = build_onboarding_list(recent_hires)
    composition = build_composition(employees, completed_profiles, docs_pending)

    return render_template(
        'administrative_personnel/overview.html',
        user=user,
        overview={
            'summary_cards': summary_cards,
            'quick_actions': quick_actions,
            'highlights': highlights,
            'attention': attention,
            'recent_activity': activity,
            'onboarding': onboarding,
            'composition': composition
        }
    )


def percentage(part, whole):
    if not whole:
        return 0
    return round((part / whole) * 100)


def has_completed_profile(employee):
    return bool(employee and employee.personal_phone and employee.personal_email and employee.id_card_number and employee.portrait_file)


def has_document_gap(employee):
    return bool(employee and (not employee.id_card_file or not employee.cv_file))


def is_recent_hire(employee):
    if not employee or not employee.created_at:
        return False
    return datetime.utcnow() - employee.created_at <= timedelta(days=30)


def build_highlights(employees, completed, docs_pending):
    highlights = []
    highlights.append(f"Current headcount: {len(employees)} team member{'s' if len(employees) != 1 else ''}.")
    highlights.append(f"{completed} personnel profiles have been completed ({percentage(completed, len(employees))}% onboarding).")
    if docs_pending:
        highlights.append(f"{docs_pending} record{'s' if docs_pending != 1 else ''} still require document uploads.")
    else:
        highlights.append("All active personnel files have required documents on file.")
    primary_location = most_common_location(employees)
    if primary_location:
        highlights.append(f"Primary location: {primary_location['label']} ({primary_location['count']} employees).")
    return highlights


def build_attention_list(employees):
    flagged = [e for e in employees if has_document_gap(e)]
    flagged.sort(key=lambda e: e.created_at or datetime.utcnow(), reverse=True)
    return [
        {
            'name': employee.full_name or 'Unnamed employee',
            'meta': missing_document_message(employee),
            'status': 'Action Needed'
        }
        for employee in flagged[:4]
    ]


def build_recent_activity(employees):
    entries = sorted(
        (e for e in employees if e.created_at),
        key=lambda e: e.created_at,
        reverse=True
    )[:5]
    return [
        {
            'title': employee.full_name or 'Employee update',
            'meta': employee.personal_email or employee.personal_phone or 'No contact info',
            'time': format_time_ago(employee.created_at)
        }
        for employee in entries
    ]


def build_onboarding_list(recent_hires):
    if not recent_hires:
        return []
    return [
        {
            'name': employee.full_name or 'New hire',
            'started': employee.created_at.strftime('%b %d, %Y') if employee.created_at else 'Recently added',
            'status': 'Complete' if has_completed_profile(employee) else 'In Progress'
        }
        for employee in sorted(recent_hires, key=lambda e: e.created_at or datetime.utcnow(), reverse=True)[:4]
    ]


def most_common_location(employees):
    counts = {}
    for employee in employees:
        location = employee.current_province or 'Unspecified location'
        counts[location] = counts.get(location, 0) + 1
    if not counts:
        return None
    label, value = max(counts.items(), key=lambda item: item[1])
    return {'label': label, 'count': value}


def missing_document_message(employee):
    missing = []
    if not employee.id_card_file:
        missing.append('ID')
    if not employee.cv_file:
        missing.append('CV')
    label = ' & '.join(missing) if missing else 'documents'
    created = employee.created_at.strftime('%b %d') if employee.created_at else 'recently'
    return f"Missing {label} · Added {created}"


def build_composition(employees, completed_profiles, docs_pending):
    gender_counts = {'female': 0, 'male': 0, 'other': 0, 'unspecified': 0}
    for employee in employees:
        gender = (employee.gender or 'unspecified').lower()
        if gender not in gender_counts:
            gender_counts['other'] += 1
        else:
            gender_counts[gender] += 1

    return {
        'profiles_complete': completed_profiles,
        'profiles_incomplete': len(employees) - completed_profiles,
        'documents_pending': docs_pending,
        'documents_complete': len(employees) - docs_pending,
        'gender': gender_counts
    }


def format_time_ago(dt):
    if not dt:
        return 'Unknown'
    delta = datetime.utcnow() - dt
    minutes = int(delta.total_seconds() // 60)
    if minutes < 1:
        return 'Just now'
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = hours // 24
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"
    weeks = days // 7
    return f"{weeks} week{'s' if weeks != 1 else ''} ago"


def get_structure_data():
    """Return the base personnel structure with divisions, departments, sub-departments, and company branches."""
    return {
        'companies': [
            {
                'name': 'Ho Chi Minh City Branch',
                'address': 'District 1, HCMC',
                'members': 78,
                'founded': '2018',
                'leader': 'Anh Tran',
                'focus': 'Headquarters operations, product, and engineering'
            },
            {
                'name': 'Hanoi Branch',
                'address': 'Ba Dinh District, Hanoi',
                'members': 64,
                'founded': '2019',
                'leader': 'Thu Nguyen',
                'focus': 'Client services, renewals, and support'
            }
        ],
        'divisions': [
            {
                'name': 'Commercial Division',
                'company': 'Ho Chi Minh City Branch',
                'leader': 'Lan Pham',
                'focus': 'Sales, marketing, and customer acquisition',
                'departments': [
                    {
                        'name': 'Sales Department',
                        'leader': 'Lan Pham',
                        'company': 'Ho Chi Minh City Branch',
                        'division': 'Commercial Division',
                        'focus': 'Strategic sales execution and partner growth',
                        'members': 18,
                        'team': [
                            'Lan Pham · Department Head',
                            'Quang Nguyen · Regional Sales Lead',
                            'Hong Le · Marketing Liaison',
                            'Bao Tran · Partner Success Lead'
                        ],
                        'sub_departments': [
                            {
                                'name': 'Enterprise Sales Team',
                                'division': 'Commercial Division',
                                'department': 'Sales Department',
                                'leader': 'Tam Nguyen',
                                'members': 9,
                                'focus': 'Enterprise account strategy and deal support',
                                'team': []
                            }
                        ]
                    },
                    {
                        'name': 'Customer Success',
                        'leader': 'Linh Hoang',
                        'company': 'Hanoi Branch',
                        'division': 'Commercial Division',
                        'focus': 'Renewals, onboarding, and customer satisfaction',
                        'members': 15,
                        'team': [
                            'Linh Hoang · CS Lead',
                            'Phuong Mai · Renewals Manager',
                            'Thanh Bui · Implementation Lead',
                            'Nhi Do · Support Excellence Lead'
                        ],
                        'sub_departments': [
                            {
                                'name': 'Customer Onboarding Team',
                                'division': 'Client Services Division',
                                'department': 'Customer Success',
                                'leader': 'Mai Pham',
                                'members': 7,
                                'focus': 'New customer onboarding and early adoption',
                                'team': []
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'Technology Division',
                'company': 'Ho Chi Minh City Branch',
                'leader': 'Hanh Do',
                'focus': 'Product engineering and platform reliability',
                'departments': [
                    {
                        'name': 'Engineering Hub',
                        'leader': 'Hanh Do',
                        'company': 'Ho Chi Minh City Branch',
                        'division': 'Technology Division',
                        'focus': 'Product development and technical innovation',
                        'members': 32,
                        'team': [
                            'Hanh Do · Engineering Manager',
                            'Khai Nguyen · Senior Platform Engineer',
                            'Thu Le · QA Practice Lead',
                            'An Tran · DevOps Manager'
                        ],
                        'sub_departments': [
                            {
                                'name': 'Platform Core Squad',
                                'division': 'Technology Division',
                                'department': 'Engineering Hub',
                                'leader': 'Bao Le',
                                'members': 12,
                                'focus': 'Core services, performance, and reliability',
                                'team': []
                            }
                        ]
                    },
                    {
                        'name': 'Platform Enablement',
                        'leader': 'Khai Nguyen',
                        'company': 'Ho Chi Minh City Branch',
                        'division': 'Technology Division',
                        'focus': 'Developer tooling and productivity',
                        'members': 14,
                        'team': [
                            'Khai Nguyen · Platform Architect',
                            'Thu Le · QA Practice Lead',
                            'An Tran · DevOps Manager',
                            'Bao Tran · Automation Engineer'
                        ],
                        'sub_departments': []
                    }
                ]
            },
            {
                'name': 'Client Services Division',
                'company': 'Hanoi Branch',
                'leader': 'Linh Hoang',
                'focus': 'Account management and customer retention',
                'departments': [
                    {
                        'name': 'Professional Services',
                        'leader': 'Phuong Mai',
                        'company': 'Hanoi Branch',
                        'division': 'Client Services Division',
                        'focus': 'Implementation, renewals, and client success enablement',
                        'members': 11,
                        'team': [
                            'Phuong Mai · Renewals Manager',
                            'Thanh Bui · Implementation Lead',
                            'Nhi Do · Support Excellence Lead',
                            'An Vo · Training Coordinator'
                        ],
                        'sub_departments': []
                    }
                ]
            }
        ]
    }


def get_employee_names():
    """Return sorted employee full names with pseudo fallback."""
    employees = Employee.query.order_by(Employee.full_name.asc()).all()
    names = [emp.full_name for emp in employees if emp.full_name]
    if not names:
        names = [
            'Lan Pham',
            'Quang Nguyen',
            'Hong Le',
            'Bao Tran',
            'Dung Vo',
            'Khai Nguyen',
            'Anh Tran',
            'Thu Nguyen'
        ]
    return names


@administrative_personnel_bp.route('/personnel/dashboard')
@login_required
def personnel_dashboard():
    """Legacy Personnel Dashboard"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('personnel_dashboard.html', user=user)

@administrative_personnel_bp.route('/personnel/add')
@login_required
def add_employee():
    """Add Employee Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template(
        'add_employee.html',
        user=user,
        mode='add',
        employee_id=None,
        employee_data={}
    )


@administrative_personnel_bp.route('/personnel/<int:employee_id>/edit')
@login_required
def edit_employee(employee_id):
    """Edit Employee Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    employee = Employee.query.get_or_404(employee_id)

    return render_template(
        'add_employee.html',
        user=user,
        mode='edit',
        employee_id=employee.id,
        employee_data=employee.to_dict()
    )

@administrative_personnel_bp.route('/personnel/list')
@login_required
def employee_list():
    """Employee List Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('employee_list.html', user=user)

@administrative_personnel_bp.route('/personnel/departments')
@login_required
def departments():
    """Departments Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    employee_names = get_employee_names()
    structure = get_structure_data()

    departments_data = []
    for division in structure['divisions']:
        for dept in division['departments']:
            dept_copy = {
                'name': dept['name'],
                'leader': dept['leader'],
                'company': dept['company'],
                'division': dept['division'],
                'focus': dept['focus'],
                'team': list(dept.get('team', [])),
                'members': dept.get('members', len(dept.get('team', []))),
                'sub_departments': dept.get('sub_departments', [])
            }
            departments_data.append(dept_copy)

    division_options = sorted({dept['division'] for dept in departments_data})

    return render_template(
        'departments.html',
        user=user,
        departments=departments_data,
        employees=employee_names,
        divisions=division_options,
        structure=structure
    )


@administrative_personnel_bp.route('/personnel/companies')
@login_required
def companies():
    """Branch companies overview"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    structure = get_structure_data()
    companies_data = structure['companies']

    return render_template('companies.html', user=user, companies=companies_data)


@administrative_personnel_bp.route('/personnel/divisions')
@login_required
def divisions():
    """Divisions overview"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    structure = get_structure_data()
    divisions_data = []

    for division in structure['divisions']:
        division_copy = {
            'name': division['name'],
            'company': division['company'],
            'leader': division['leader'],
            'focus': division['focus'],
            'departments': [
                {
                    'name': dept['name'],
                    'head': dept['leader'],
                    'members': dept.get('members', len(dept.get('team', [])))
                }
                for dept in division['departments']
            ]
        }
        divisions_data.append(division_copy)

    company_options = sorted({division['company'] for division in divisions_data})

    return render_template(
        'divisions.html',
        user=user,
        divisions=divisions_data,
        companies=company_options,
        structure=structure
    )


@administrative_personnel_bp.route('/personnel/sub-departments')
@login_required
def sub_departments():
    """Sub-departments overview"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    employee_names = get_employee_names()
    structure = get_structure_data()

    sub_departments_data = []
    department_names = set()
    division_names = set()

    for division in structure['divisions']:
        division_names.add(division['name'])
        for dept in division['departments']:
            department_names.add(dept['name'])
            for sub in dept.get('sub_departments', []):
                sub_copy = {
                    'name': sub['name'],
                    'division': sub['division'],
                    'department': sub['department'],
                    'leader': sub['leader'],
                    'focus': sub['focus'],
                    'team': list(sub.get('team', [])),
                    'members': sub.get('members', len(sub.get('team', [])))
                }
                sub_departments_data.append(sub_copy)

    department_options = sorted(department_names)
    division_options = sorted(division_names)

    return render_template(
        'sub_departments.html',
        user=user,
        sub_departments=sub_departments_data,
        employees=employee_names,
        departments=department_options,
        divisions=division_options,
        structure=structure
    )


@administrative_personnel_bp.route('/personnel/org-chart')
@login_required
def organizational_chart():
    """Organizational chart page showing company hierarchy"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    structure = get_structure_data()

    org_name = 'Company Headquarters'
    root_meta_parts = []
    if user.organization:
        org_name = user.organization.name or org_name
        if user.organization.industry:
            root_meta_parts.append(user.organization.industry)
        if user.organization.location:
            root_meta_parts.append(user.organization.location)
        if user.organization.size:
            root_meta_parts.append(f"Size: {user.organization.size}")

    root_meta = ' • '.join(root_meta_parts) if root_meta_parts else None

    return render_template(
        'organizational_chart.html',
        user=user,
        structure=structure,
        root_info={'name': org_name, 'meta': root_meta}
    )

@administrative_personnel_bp.route('/personnel/api/employee', methods=['POST'])
@login_required
def save_employee():
    """Save employee data to database"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        sanitized_payload = sanitize_employee_payload(data)
        
        # Create new employee record
        employee = Employee(**sanitized_payload)
        
        # Add to database
        db.session.add(employee)
        db.session.commit()
        
        print(f"DEBUG: Employee saved successfully - ID: {employee.id}, Name: {employee.full_name}")
        
        return jsonify({
            'success': True,
            'message': f'Employee {employee.full_name} has been saved successfully!',
            'employee_id': employee.id
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: Failed to save employee: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to save employee data: {str(e)}'
        }), 500


@administrative_personnel_bp.route('/personnel/api/employee/<int:employee_id>', methods=['PUT'])
@login_required
def update_employee(employee_id):
    """Update an existing employee record"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        employee = Employee.query.get_or_404(employee_id)

        sanitized_payload = sanitize_employee_payload(data, include_missing=False)

        for field, value in sanitized_payload.items():
            setattr(employee, field, value)

        db.session.commit()

        print(f"DEBUG: Employee updated successfully - ID: {employee.id}, Name: {employee.full_name}")

        return jsonify({
            'success': True,
            'message': f'Employee {employee.full_name} has been updated successfully!',
            'employee_id': employee.id
        })
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"ERROR: Database error while updating employee {employee_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update employee due to a database error.'
        }), 500
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: Failed to update employee {employee_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to update employee data: {str(e)}'
        }), 500

@administrative_personnel_bp.route('/personnel/api/employees', methods=['GET'])
@login_required
def get_employees():
    """Get all employees from database"""
    try:
        employees = Employee.query.order_by(Employee.created_at.desc()).all()
        
        employees_data = []
        for employee in employees:
            employees_data.append(employee.to_dict())
        
        print(f"DEBUG: Retrieved {len(employees_data)} employees from database")
        
        return jsonify({
            'success': True,
            'employees': employees_data,
            'count': len(employees_data)
        })
        
    except Exception as e:
        print(f"ERROR: Failed to retrieve employees: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve employees: {str(e)}'
        }), 500
