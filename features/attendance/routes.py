from flask import request, jsonify, render_template, redirect, session
from models import User, Attendance, db
from datetime import datetime, date, timedelta
from core.auth import login_required, api_login_required
from . import attendance_bp
import openpyxl
import os
import tempfile
from werkzeug.utils import secure_filename

@attendance_bp.route('/attendance')
@login_required
def attendance_dashboard():
    """Main attendance dashboard page - redirects to monthly attendance detail"""
    return redirect('/attendance/monthly_attendance_detail')

@attendance_bp.route('/attendance/admin')
@login_required
def attendance_admin():
    """Admin attendance management page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    # TODO: Add admin role check here
    # if not user.is_admin:
    #     return redirect('/attendance')
    
    return render_template('attendance_dashboard.html', user=user, is_admin=True)

@attendance_bp.route('/attendance/monthly_attendance_detail')
@login_required
def monthly_attendance_detail():
    """Monthly Attendance Detail page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('monthly_attendance_detail.html', user=user)

@attendance_bp.route('/attendance/attendance_summary')
@login_required
def attendance_summary():
    """Attendance Summary page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('attendance_summary.html', user=user)

@attendance_bp.route('/attendance/work_data')
@login_required
def work_data():
    """Work Data page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('work_data.html', user=user)

@attendance_bp.route('/api/check-in', methods=['POST'])
@api_login_required
def check_in():
    """Employee check-in API"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        current_time = datetime.now()
        today = current_time.date()
        
        # Check if already checked in today
        existing_checkin = Attendance.query.filter(
            Attendance.user_id == user.id,
            Attendance.date == today,
            Attendance.check_in_time.isnot(None)
        ).first()
        
        if existing_checkin:
            return jsonify({'error': 'Already checked in today'}), 400
        
        # Create new attendance record
        attendance = Attendance(
            user_id=user.id,
            date=today,
            check_in_time=current_time,
            status='present'
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            'message': 'Check-in successful',
            'check_in_time': current_time.strftime('%H:%M:%S'),
            'date': today.strftime('%Y-%m-%d')
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Check-in failed'}), 500

@attendance_bp.route('/api/check-out', methods=['POST'])
@api_login_required
def check_out():
    """Employee check-out API"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        current_time = datetime.now()
        today = current_time.date()
        
        # Find today's attendance record
        attendance = Attendance.query.filter(
            Attendance.user_id == user.id,
            Attendance.date == today,
            Attendance.check_in_time.isnot(None)
        ).first()
        
        if not attendance:
            return jsonify({'error': 'No check-in found for today'}), 400
        
        if attendance.check_out_time:
            return jsonify({'error': 'Already checked out today'}), 400
        
        # Update attendance record
        attendance.check_out_time = current_time
        attendance.work_hours = calculate_work_hours(attendance.check_in_time, current_time)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Check-out successful',
            'check_out_time': current_time.strftime('%H:%M:%S'),
            'work_hours': attendance.work_hours
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Check-out failed'}), 500

@attendance_bp.route('/api/attendance-status', methods=['GET'])
@api_login_required
def attendance_status():
    """Get current attendance status for today"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        today = date.today()
        attendance = Attendance.query.filter_by(
            user_id=user.id,
            date=today
        ).first()
        
        if not attendance:
            return jsonify({
                'status': 'not_checked_in',
                'message': 'Not checked in today'
            }), 200
        
        if attendance.check_in_time and not attendance.check_out_time:
            return jsonify({
                'status': 'checked_in',
                'check_in_time': attendance.check_in_time.strftime('%H:%M:%S'),
                'message': 'Checked in, ready to check out'
            }), 200
        
        if attendance.check_in_time and attendance.check_out_time:
            return jsonify({
                'status': 'checked_out',
                'check_in_time': attendance.check_in_time.strftime('%H:%M:%S'),
                'check_out_time': attendance.check_out_time.strftime('%H:%M:%S'),
                'work_hours': attendance.work_hours,
                'message': 'Completed for today'
            }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get attendance status'}), 500

@attendance_bp.route('/api/attendance-history', methods=['GET'])
@api_login_required
def attendance_history():
    """Get attendance history for the current user"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get date range from query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            # Default to last 30 days
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Query attendance records
        attendance_records = Attendance.query.filter(
            Attendance.user_id == user.id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).order_by(Attendance.date.desc()).all()
        
        # Format response
        history = []
        for record in attendance_records:
            history.append({
                'date': record.date.strftime('%Y-%m-%d'),
                'check_in_time': record.check_in_time.strftime('%H:%M:%S') if record.check_in_time else None,
                'check_out_time': record.check_out_time.strftime('%H:%M:%S') if record.check_out_time else None,
                'work_hours': record.work_hours,
                'status': record.status,
                'notes': record.notes
            })
        
        return jsonify({
            'history': history,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get attendance history'}), 500

@attendance_bp.route('/attendance-history')
@login_required
def attendance_history_page():
    """Attendance history page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('attendance_history.html', user=user)

def calculate_work_hours(check_in_time, check_out_time):
    """Calculate work hours between check-in and check-out"""
    if not check_in_time or not check_out_time:
        return 0
    
    time_diff = check_out_time - check_in_time
    hours = time_diff.total_seconds() / 3600
    return round(hours, 2)


# ========================= Timesheet Boards (Summary) =========================
@attendance_bp.route('/api/timesheet-boards', methods=['GET'])
@api_login_required
def list_timesheet_boards():
    """List timesheet summary boards created by managers.

    This is a stub endpoint that currently returns an empty list with
    pagination metadata and echoes back filter parameters. It is intended to
    power the Summary tab UI. Later, this can be wired to real persistence.
    """
    try:
        # Parse filters
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        query_text = request.args.get('q')
        unit = request.args.get('unit')
        board_type = request.args.get('type')
        status = request.args.get('status')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        # Placeholder data (empty state by default)
        items = []
        total = 0

        # Response structure
        return jsonify({
            'items': items,
            'page': page,
            'page_size': page_size,
            'total': total,
            'filters': {
                'q': query_text,
                'unit': unit,
                'type': board_type,
                'status': status,
                'from_date': from_date,
                'to_date': to_date
            }
        }), 200
    except Exception:
        return jsonify({'error': 'Failed to load timesheet boards'}), 500


@attendance_bp.route('/api/work-data', methods=['GET'])
@api_login_required
def list_work_data():
    """List raw attendance work data records per employee (stub).

    Accepts filters similar to the example UI and returns a paginated list.
    """
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        q = request.args.get('q')
        department = request.args.get('department')
        method = request.args.get('method')
        shift = request.args.get('shift')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        items = []
        total = 0

        return jsonify({
            'items': items,
            'page': page,
            'page_size': page_size,
            'total': total,
            'filters': {
                'q': q,
                'department': department,
                'method': method,
                'shift': shift,
                'from_date': from_date,
                'to_date': to_date
            }
        }), 200
    except Exception:
        return jsonify({'error': 'Failed to load work data'}), 500


@attendance_bp.route('/api/import-excel', methods=['POST'])
@api_login_required
def import_excel():
    """Import attendance data from Excel file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Invalid file format. Please upload an Excel file (.xlsx or .xls)'}), 400
        
        # Get month and year from request
        month = request.form.get('month', '9')  # Default to September
        year = request.form.get('year', str(datetime.now().year))  # Default to current year
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        file.save(temp_file.name)
        
        try:
            # Open Excel file
            workbook = openpyxl.load_workbook(temp_file.name)
            worksheet = workbook.active
            
            # Validate Excel format
            validation_result = validate_excel_format(worksheet)
            if not validation_result['valid']:
                return jsonify({
                    'error': 'Invalid Excel format',
                    'details': validation_result['errors']
                }), 400
            
            # Process Excel data
            processed_data = process_excel_data(worksheet, month)
            
            # Clear existing data for the month (replace mode)
            clear_monthly_data(int(year), int(month))
            
            # Save processed data to database
            save_attendance_data(processed_data, int(year), int(month))
            
            return jsonify({
                'message': 'Excel file imported successfully',
                'rows_imported': len(processed_data),
                'month': month
            }), 200
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file.name)
            
    except Exception as e:
        return jsonify({'error': f'Import failed: {str(e)}'}), 500


def validate_excel_format(worksheet):
    """Validate that Excel file has the correct format"""
    errors = []
    
    # Check if worksheet has data
    if worksheet.max_row < 5:  # At least 4 header rows + 1 data row
        errors.append("Excel file must have at least 4 header rows and 1 data row")
        return {'valid': False, 'errors': errors}
    
    # Check header structure (simplified validation)
    # Row 1: Main headers
    # Row 2: Day of week headers  
    # Row 3: Day numbers
    # Row 4: Sub-headers
    
    # Basic validation - check if first few cells contain expected headers
    expected_headers = ['No.', 'Employee', 'Detailed workdays of month']
    
    for i, expected in enumerate(expected_headers):
        cell_value = worksheet.cell(row=1, column=i+1).value
        if not cell_value or expected.lower() not in str(cell_value).lower():
            errors.append(f"Expected header '{expected}' not found in column {i+1}")
    
    return {'valid': len(errors) == 0, 'errors': errors}


def process_excel_data(worksheet, month):
    """Process Excel data and return structured attendance data"""
    processed_data = []
    
    # Get number of days in the month
    year = datetime.now().year
    if month in ['1', '3', '5', '7', '8', '10', '12']:
        days_in_month = 31
    elif month in ['4', '6', '9', '11']:
        days_in_month = 30
    else:  # February
        days_in_month = 29 if year % 4 == 0 else 28
    
    # Process data rows (starting from row 5, after 4 header rows)
    for row_num in range(5, min(worksheet.max_row + 1, 30)):  # Max 25 data rows
        row_data = {}
        
        # Get basic info
        row_data['row_number'] = worksheet.cell(row=row_num, column=1).value
        row_data['employee_name'] = worksheet.cell(row=row_num, column=2).value
        
        if not row_data['employee_name']:
            continue  # Skip empty rows
        
        # Get daily attendance data (columns 3 to 3+days_in_month-1)
        daily_data = []
        for day in range(1, days_in_month + 1):
            cell_value = worksheet.cell(row=row_num, column=2 + day).value
            daily_data.append(cell_value if cell_value is not None else '')
        
        row_data['daily_attendance'] = daily_data
        
        # Get other columns data
        col_offset = 2 + days_in_month
        row_data['standard_workdays'] = worksheet.cell(row=row_num, column=col_offset).value
        row_data['admin_workdays'] = worksheet.cell(row=row_num, column=col_offset + 1).value
        row_data['business_trip_workdays'] = worksheet.cell(row=row_num, column=col_offset + 2).value
        
        # Overtime data (4 columns)
        row_data['overtime_o1'] = worksheet.cell(row=row_num, column=col_offset + 3).value
        row_data['overtime_o2'] = worksheet.cell(row=row_num, column=col_offset + 4).value
        row_data['overtime_o3'] = worksheet.cell(row=row_num, column=col_offset + 5).value
        row_data['overtime_total'] = worksheet.cell(row=row_num, column=col_offset + 6).value
        
        # Continue with other columns...
        # (This is a simplified version - you can expand based on your exact needs)
        
        processed_data.append(row_data)
    
    return processed_data


def clear_monthly_data(year, month):
    """Clear existing attendance data for the specified month"""
    # This is a placeholder - you might want to implement this based on your needs
    # For now, we'll just clear all attendance data
    Attendance.query.delete()
    db.session.commit()


def save_attendance_data(processed_data, year, month):
    """Save processed attendance data to database"""
    try:
        for data in processed_data:
            # Create attendance record for each day
            for day, attendance_value in enumerate(data['daily_attendance'], 1):
                if attendance_value and str(attendance_value).strip():
                    # Create a basic attendance record
                    # You can expand this based on your specific data structure
                    attendance = Attendance(
                        user_id=1,  # Placeholder - you might want to map this properly
                        date=date(year, month, day),
                        status='present' if attendance_value else 'absent',
                        notes=f"Imported from Excel: {data['employee_name']}"
                    )
                    db.session.add(attendance)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
