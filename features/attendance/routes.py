from flask import request, jsonify, render_template, redirect, session
from models import User, Attendance, db
from datetime import datetime, date, timedelta
from core.auth import login_required, api_login_required
from . import attendance_bp

@attendance_bp.route('/attendance')
@login_required
def attendance_dashboard():
    """Main attendance dashboard page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('attendance_dashboard.html', user=user)

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
