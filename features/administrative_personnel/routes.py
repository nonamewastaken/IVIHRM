from flask import render_template, redirect, session, request, jsonify, send_file
from models import User, Employee
from core.database import db
from core.auth import login_required
from . import administrative_personnel_bp
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import os
import base64
import json
import io
import zipfile
from config.settings import Config
from google import genai
from google.genai import types
from werkzeug.utils import secure_filename

gemini_client = genai.Client(api_key=Config.GEMINI_API_KEY)

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


@administrative_personnel_bp.route('/personnel/cv-customization')
@login_required
def cv_customization():
    """Placeholder CV customization workspace."""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    return render_template('cv_customization.html', user=user)


@administrative_personnel_bp.route('/personnel/add')
@login_required
def add_employee():
    """Entry point for Add Employee flow: choose single vs multiple."""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('select_add_mode.html', user=user)


@administrative_personnel_bp.route('/personnel/add/start')
@login_required
def start_add_employee():
    """Start the Add Employee wizard after choosing mode."""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    add_mode = request.args.get('add_mode', 'single')
    return render_template(
        'add_employee.html',
        user=user,
        mode='add',
        add_mode=add_mode,
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


@administrative_personnel_bp.route('/personnel/<int:employee_id>/profile')
@login_required
def view_employee_profile(employee_id):
    """Read-only Employee Profile page."""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    employee = Employee.query.get_or_404(employee_id)

    # Simple document status summary for UI
    missing_docs = []
    if not employee.id_card_file:
        missing_docs.append('ID card')
    if not employee.cv_file:
        missing_docs.append('CV')
    docs_status = 'All required documents on file' if not missing_docs else 'Missing: ' + ', '.join(missing_docs)

    # Build downloadable file list
    files = []

    # Predefined document fields (zipped on download)
    for key, (field_name, base_label) in FILE_FIELD_MAPPING.items():
        if getattr(employee, field_name, None):
            safe_name = (employee.full_name or f"employee_{employee.id}").replace(' ', '_').lower()
            filename = f"{safe_name}_{base_label}.zip"
            files.append({
                'name': filename,
                'url': f"/personnel/{employee.id}/files/{key}"
            })

    # Extra uploaded zip files on disk
    uploads_dir = os.path.join(
        os.path.dirname(__file__),
        'static',
        'uploads',
        f'employee_{employee.id}'
    )
    try:
        if os.path.isdir(uploads_dir):
            for entry in os.listdir(uploads_dir):
                if entry.lower().endswith('.zip'):
                    files.append({
                        'name': entry,
                        'url': f"/personnel/{employee.id}/files/extra/{entry}"
                    })
    except Exception as e:
        print(f"WARNING: Failed to list extra files for employee {employee.id}: {e}")

    return render_template(
        'employee_profile.html',
        user=user,
        employee=employee,
        docs_status=docs_status,
        employee_files=files
    )


FILE_FIELD_MAPPING = {
    'cv': ('cv_file', 'cv'),
    'portrait': ('portrait_file', 'portrait'),
    'health': ('health_file', 'health_certificate'),
    'id_card': ('id_card_file', 'id_card'),
    'passport': ('passport_file', 'passport'),
}


@administrative_personnel_bp.route('/personnel/<int:employee_id>/files/<string:file_key>')
@login_required
def download_employee_file(employee_id, file_key):
    """Download a zipped version of a stored employee document (CV, ID card, etc.)."""
    if file_key not in FILE_FIELD_MAPPING:
        return jsonify({'success': False, 'error': 'Unknown file type'}), 404

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    employee = Employee.query.get_or_404(employee_id)
    field_name, base_label = FILE_FIELD_MAPPING[file_key]
    data_url = getattr(employee, field_name, None)

    if not data_url:
        return jsonify({'success': False, 'error': 'File not found for this employee'}), 404

    # Decode data URL -> bytes and determine extension
    mime_type = 'application/octet-stream'
    b64data = data_url
    try:
        if isinstance(data_url, str) and data_url.startswith('data:'):
            header, b64data = data_url.split(',', 1)
            mime_type = header.split(';')[0].split(':', 1)[1] or mime_type
        raw_bytes = base64.b64decode(b64data)
    except Exception as e:
        print(f"ERROR: Failed to decode stored file for employee {employee_id}, field {field_name}: {e}")
        return jsonify({'success': False, 'error': 'Stored file is invalid'}), 500

    # Guess extension from MIME
    ext = 'bin'
    if mime_type in ('image/jpeg', 'image/jpg'):
        ext = 'jpg'
    elif mime_type == 'image/png':
        ext = 'png'
    elif mime_type == 'image/gif':
        ext = 'gif'
    elif mime_type in ('application/pdf', 'application/x-pdf'):
        ext = 'pdf'

    # Build in-memory zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        filename_in_zip = f"{base_label}.{ext}"
        zf.writestr(filename_in_zip, raw_bytes)
    zip_buffer.seek(0)

    safe_name = employee.full_name or f"employee_{employee.id}"
    download_name = f"{safe_name.replace(' ', '_').lower()}_{base_label}.zip"

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name=download_name,
        mimetype='application/zip'
    )


@administrative_personnel_bp.route('/personnel/<int:employee_id>/files/extra/<path:filename>')
@login_required
def download_extra_employee_file(employee_id, filename):
    """Download an extra uploaded zip file from disk for this employee."""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    employee = Employee.query.get_or_404(employee_id)

    uploads_dir = os.path.join(
        os.path.dirname(__file__),
        'static',
        'uploads',
        f'employee_{employee.id}'
    )
    full_path = os.path.join(uploads_dir, filename)
    if not os.path.isfile(full_path) or not full_path.lower().endswith('.zip'):
        return jsonify({'success': False, 'error': 'File not found'}), 404

    return send_file(full_path, as_attachment=True, download_name=filename, mimetype='application/zip')


@administrative_personnel_bp.route('/personnel/evaluate-cv')
@login_required
def evaluate_cv_page():
    """CV Evaluation page with department selection"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    departments = ['Development', 'HRM', 'Sales', 'Marketing', 'Finance', 'Operations']
    
    return render_template('evaluate_cv.html', user=user, departments=departments)


@administrative_personnel_bp.route('/personnel/<int:employee_id>/files/upload', methods=['POST'])
@login_required
def upload_employee_files(employee_id):
    """Upload additional files for an employee, saving each as a zip on disk."""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    employee = Employee.query.get_or_404(employee_id)

    files = request.files.getlist('files')
    if not files:
        return redirect(f'/personnel/{employee.id}/profile')

    uploads_dir = os.path.join(
        os.path.dirname(__file__),
        'static',
        'uploads',
        f'employee_{employee.id}'
    )
    os.makedirs(uploads_dir, exist_ok=True)

    for f in files:
        if not f or not f.filename:
            continue
        original_name = secure_filename(f.filename)
        if not original_name:
            continue
        # Create a zip file on disk containing the uploaded file
        zip_name = f"{original_name}.zip" if not original_name.lower().endswith('.zip') else original_name
        zip_path = os.path.join(uploads_dir, zip_name)
        try:
            file_bytes = f.read()
            with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                zf.writestr(original_name, file_bytes)
        except Exception as e:
            print(f"ERROR: Failed to save uploaded file for employee {employee.id}: {e}")
            continue

    return redirect(f'/personnel/{employee.id}/profile')

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


def _data_url_to_part(data_url):
    """Convert data URL (base64) to a Part object for Gemini."""
    try:
        if not data_url or not isinstance(data_url, str):
            return None
        if data_url.startswith('data:'):
            header, b64data = data_url.split(',', 1)
            mime = header.split(';')[0].split(':', 1)[1] or 'image/png'
        else:
            # Assume it's just base64 without header
            mime = 'image/png'
            b64data = data_url
        # Decode base64 to bytes and use Part.from_bytes() for proper handling
        file_bytes = base64.b64decode(b64data)
        return types.Part.from_bytes(data=file_bytes, mime_type=mime)
    except Exception as e:
        print(f"ERROR: Failed to convert data URL to part: {str(e)}")
        return None


def _parse_json_forgiving(text):
    """Extract the first JSON object in the text, forgiving surrounding content."""
    if not text:
        return {}
    try:
        return json.loads(text)
    except Exception:
        pass
    # Try to find a JSON block
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception:
            return {}
    return {}


@administrative_personnel_bp.route('/personnel/api/extract-cv', methods=['POST'])
@login_required
def extract_from_cv():
    """Extract personal info fields from uploaded CV image(s) using Gemini."""
    try:
        payload = request.get_json() or {}
        files = payload.get('files') or []
        if not files:
            return jsonify({'success': False, 'error': 'No files provided'}), 400

        inline_parts = []
        for f in files:
            part = _data_url_to_part(f)
            if part:
                inline_parts.append(part)
        if not inline_parts:
            return jsonify({'success': False, 'error': 'Invalid file format'}), 400

        instructions = (
            "You are given one or more CV/resume files (images or PDFs). "
            "Extract only the following fields if present. Return STRICT JSON with keys using these exact snake_case names. "
            "Do not include keys that are missing. Do not add commentary.\n\n"
            "Required keys if present: "
            "full_name, gender, date_of_birth, place_of_birth, hometown, personal_phone, personal_email, "
            "personal_tax_code, social_insurance_code, party_join_date, party_join_place, health_status, "
            "permanent_address, current_address, permanent_province, current_province, permanent_ward, current_ward, "
            "permanent_street, current_street, id_card_number, id_card_issue_date, id_card_expiry_date, id_card_issue_place, "
            "passport_number, passport_issue_date, passport_expiry_date, passport_issue_place"
        )

        # Build content for google-genai: text instructions + file parts
        parts = [types.Part.from_text(instructions)]
        parts.extend(inline_parts)

        # Wrap parts in Content object with user role
        content = types.Content(role="user", parts=parts)

        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[content],
        )

        text = getattr(response.candidates[0].content.parts[0], "text", "") if getattr(response, "candidates", None) else ""
        data = _parse_json_forgiving(text)

        # Only return known fields to prevent UI pollution
        allowed = {
            'full_name','gender','date_of_birth','place_of_birth','hometown',
            'personal_phone','personal_email','personal_tax_code','social_insurance_code',
            'party_join_date','party_join_place','health_status',
            'permanent_address','current_address','permanent_province','current_province',
            'permanent_ward','current_ward','permanent_street','current_street',
            'id_card_number','id_card_issue_date','id_card_expiry_date','id_card_issue_place',
            'passport_number','passport_issue_date','passport_expiry_date','passport_issue_place'
        }
        filtered = {k: v for k, v in (data or {}).items() if k in allowed and v}

        return jsonify({'success': True, 'data': filtered})
    except Exception as e:
        print(f"ERROR: CV extraction failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to extract data from CV: {str(e)}'
        }), 500


@administrative_personnel_bp.route('/personnel/api/evaluate-cv', methods=['POST'])
@login_required
def evaluate_cv():
    """Evaluate CV to determine if it suits the Development department using Gemini."""
    try:
        payload = request.get_json() or {}
        files = payload.get('files') or []
        department = payload.get('department', 'Development')  # Default to Development
        
        if not files:
            return jsonify({'success': False, 'error': 'No files provided'}), 400

        inline_parts = []
        for f in files:
            part = _data_url_to_part(f)
            if part:
                inline_parts.append(part)
        if not inline_parts:
            return jsonify({'success': False, 'error': 'Invalid file format'}), 400

        # Create evaluation prompt based on department
        department_requirements = {
            'Development': {
                'skills': ['programming', 'software development', 'coding', 'algorithms', 'data structures', 
                          'web development', 'mobile development', 'database', 'API', 'version control', 
                          'testing', 'debugging', 'problem solving'],
                'technologies': ['Python', 'JavaScript', 'Java', 'C++', 'React', 'Node.js', 'SQL', 
                                'Git', 'Docker', 'AWS', 'Agile', 'Scrum'],
                'experience': 'software development, programming projects, technical roles'
            },
            'HRM': {
                'skills': ['human resources management', 'recruitment', 'talent acquisition', 'employee relations', 
                          'performance management', 'compensation and benefits', 'training and development', 
                          'HR policies', 'labor law', 'organizational development', 'conflict resolution'],
                'technologies': ['HRIS', 'ATS', 'Microsoft Office', 'HR Analytics', 'Payroll Systems'],
                'experience': 'human resources, recruitment, employee management, HR administration'
            },
            'Sales': {
                'skills': ['communication', 'negotiation', 'customer relations', 'presentation', 
                          'relationship building', 'closing deals'],
                'technologies': ['CRM', 'Salesforce', 'Microsoft Office'],
                'experience': 'sales, business development, account management'
            },
            'Marketing': {
                'skills': ['digital marketing', 'SEO', 'content creation', 'social media', 
                          'analytics', 'campaign management', 'branding'],
                'technologies': ['Google Analytics', 'Facebook Ads', 'Adobe Creative Suite', 'HubSpot'],
                'experience': 'marketing, advertising, content creation'
            },
            'Finance': {
                'skills': ['financial analysis', 'accounting', 'budgeting', 'financial reporting', 
                          'risk management', 'auditing', 'tax planning'],
                'technologies': ['Excel', 'QuickBooks', 'SAP', 'Oracle Financials', 'Financial Software'],
                'experience': 'finance, accounting, financial analysis, auditing'
            },
            'Operations': {
                'skills': ['process improvement', 'project management', 'supply chain', 'logistics', 
                          'quality control', 'operations management', 'strategic planning'],
                'technologies': ['ERP Systems', 'Project Management Tools', 'Microsoft Office'],
                'experience': 'operations, process management, supply chain, logistics'
            }
        }

        req = department_requirements.get(department, department_requirements['Development'])

        instructions = (
            f"You are an HR evaluation expert. Analyze the provided CV/resume and evaluate if the candidate "
            f"is suitable for the {department} department.\n\n"
            f"**Department Requirements for {department}:**\n"
            f"- Key Skills: {', '.join(req['skills'])}\n"
            f"- Technologies/Tools: {', '.join(req['technologies'])}\n"
            f"- Relevant Experience: {req['experience']}\n\n"
            f"**Evaluation Criteria:**\n"
            f"1. Technical Skills Match (0-10): Rate how well the candidate's technical skills match the department requirements\n"
            f"2. Experience Relevance (0-10): Rate how relevant their work experience is to the department\n"
            f"3. Education Background (0-10): Rate how relevant their education is\n"
            f"4. Overall Suitability (0-10): Overall rating for the department\n\n"
            f"**Return a JSON object with the following structure:**\n"
            f"{{\n"
            f"  \"suitable\": true/false,\n"
            f"  \"overall_score\": 0-10,\n"
            f"  \"scores\": {{\n"
            f"    \"technical_skills\": 0-10,\n"
            f"    \"experience_relevance\": 0-10,\n"
            f"    \"education_background\": 0-10\n"
            f"  }},\n"
            f"  \"strengths\": [\"strength1\", \"strength2\", ...],\n"
            f"  \"weaknesses\": [\"weakness1\", \"weakness2\", ...],\n"
            f"  \"recommendation\": \"Brief recommendation text\",\n"
            f"  \"key_skills_found\": [\"skill1\", \"skill2\", ...],\n"
            f"  \"missing_skills\": [\"skill1\", \"skill2\", ...]\n"
            f"}}\n\n"
            f"Be thorough and objective in your evaluation. Consider the candidate's potential even if they don't have all required skills."
        )

        # Build content for google-genai: text instructions + file parts
        parts = [types.Part.from_text(instructions)]
        parts.extend(inline_parts)

        # Wrap parts in Content object with user role
        content = types.Content(role="user", parts=parts)

        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[content],
        )

        text = getattr(response.candidates[0].content.parts[0], "text", "") if getattr(response, "candidates", None) else ""
        evaluation_data = _parse_json_forgiving(text)

        # Validate and structure the response
        if not evaluation_data:
            return jsonify({
                'success': False,
                'error': 'Failed to parse evaluation response from AI'
            }), 500

        # Ensure required fields exist
        result = {
            'suitable': evaluation_data.get('suitable', False),
            'overall_score': float(evaluation_data.get('overall_score', 0)),
            'scores': {
                'technical_skills': float(evaluation_data.get('scores', {}).get('technical_skills', 0)),
                'experience_relevance': float(evaluation_data.get('scores', {}).get('experience_relevance', 0)),
                'education_background': float(evaluation_data.get('scores', {}).get('education_background', 0))
            },
            'strengths': evaluation_data.get('strengths', []),
            'weaknesses': evaluation_data.get('weaknesses', []),
            'recommendation': evaluation_data.get('recommendation', 'No recommendation provided'),
            'key_skills_found': evaluation_data.get('key_skills_found', []),
            'missing_skills': evaluation_data.get('missing_skills', []),
            'department': department
        }

        print(f"DEBUG: CV evaluation completed for {department} department")
        print(f"  Suitable: {result['suitable']}, Overall Score: {result['overall_score']}")

        return jsonify({
            'success': True,
            'evaluation': result
        })

    except Exception as e:
        print(f"ERROR: CV evaluation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Failed to evaluate CV: {str(e)}'
        }), 500
