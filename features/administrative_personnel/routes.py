from flask import render_template, redirect, session, request, jsonify
from models import User, Employee
from core.database import db
from core.auth import login_required
from . import administrative_personnel_bp
import base64
import os
from datetime import datetime

@administrative_personnel_bp.route('/personnel')
@login_required
def personnel_overview():
    """Personnel Overview - Default page for Personnel section"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('overview.html', user=user)

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
    
    return render_template('add_employee.html', user=user)

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
    
    return render_template('departments.html', user=user)

@administrative_personnel_bp.route('/personnel/api/employee', methods=['POST'])
@login_required
def save_employee():
    """Save employee data to database"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Helper function to convert empty strings to None
        def empty_to_none(value):
            if value and str(value).strip():
                return str(value).strip()
            return None
        
        # Create new employee record
        employee = Employee(
            # Basic Information
            full_name=empty_to_none(data.get('full_name')),
            gender=empty_to_none(data.get('gender')),
            date_of_birth=empty_to_none(data.get('date_of_birth')),
            place_of_birth=empty_to_none(data.get('place_of_birth')),
            hometown=empty_to_none(data.get('hometown')),
            marital_status=empty_to_none(data.get('marital_status')),
            ethnicity=empty_to_none(data.get('ethnicity')),
            religion=empty_to_none(data.get('religion')),
            
            # Contact Information
            personal_phone=empty_to_none(data.get('personal_phone')),
            personal_email=empty_to_none(data.get('personal_email')),
            
            # Tax and Insurance
            personal_tax_code=empty_to_none(data.get('personal_tax_code')),
            social_insurance_code=empty_to_none(data.get('social_insurance_code')),
            
            # Party Information
            party_join_date=empty_to_none(data.get('party_join_date')),
            party_join_place=empty_to_none(data.get('party_join_place')),
            
            # Health Information
            health_status=empty_to_none(data.get('health_status')),
            emergency_contact=empty_to_none(data.get('emergency_contact')),
            
            # Address Information
            permanent_address=empty_to_none(data.get('permanent_address')),
            permanent_province=empty_to_none(data.get('permanent_province')),
            permanent_ward=empty_to_none(data.get('permanent_ward')),
            permanent_street=empty_to_none(data.get('permanent_street')),
            
            current_address=empty_to_none(data.get('current_address')),
            current_province=empty_to_none(data.get('current_province')),
            current_ward=empty_to_none(data.get('current_ward')),
            current_street=empty_to_none(data.get('current_street')),
            
            # ID Card Information
            id_card_number=empty_to_none(data.get('id_card_number')),
            id_card_issue_date=empty_to_none(data.get('id_card_issue_date')),
            id_card_expiry_date=empty_to_none(data.get('id_card_expiry_date')),
            id_card_issue_place=empty_to_none(data.get('id_card_issue_place')),
            
            # Passport Information
            passport_number=empty_to_none(data.get('passport_number')),
            passport_issue_date=empty_to_none(data.get('passport_issue_date')),
            passport_expiry_date=empty_to_none(data.get('passport_expiry_date')),
            passport_issue_place=empty_to_none(data.get('passport_issue_place')),
            
            # File uploads (store as base64 for now)
            cv_file=empty_to_none(data.get('cv_file')),
            portrait_file=empty_to_none(data.get('portrait_file')),
            health_file=empty_to_none(data.get('health_file')),
            id_card_file=empty_to_none(data.get('id_card_file')),
            passport_file=empty_to_none(data.get('passport_file'))
        )
        
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
