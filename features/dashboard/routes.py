from flask import render_template, redirect, session, request, jsonify
from models import User, Organization
from core.database import db
from core.auth import login_required
from config.settings import Config
from . import dashboard_bp

@dashboard_bp.route('/')
def root():
    """Root route should show login page directly or redirect based on user role"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            # Redirect employee accounts to maintenance page
            if hasattr(user, 'role') and user.role == 'employee':
                return redirect('/employee/maintenance')
            # If profile is not completed, redirect to complete profile
            if not user.profile_completed:
                return redirect('/complete-profile')
            return redirect('/dashboard')
    return redirect('/login')

@dashboard_bp.route('/login')
def login_page():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            # Redirect employee accounts to maintenance page
            if hasattr(user, 'role') and user.role == 'employee':
                return redirect('/employee/maintenance')
            # If profile is not completed, redirect to complete profile
            if not user.profile_completed:
                return redirect('/complete-profile')
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
    return render_template('dashboard.html', user=user, user_name=user.name, company_name=company_name)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Re-query user object from database to get latest state (ensures fresh data after onboarding)
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    # Redirect employee accounts to maintenance page
    if hasattr(user, 'role') and user.role == 'employee':
        return redirect('/employee/maintenance')
    
    # If profile is not completed, redirect to complete profile
    if not user.profile_completed:
        return redirect('/complete-profile')
    
    company_name = user.organization.name if user.organization else "Your Company"
    return render_template('dashboard.html', user=user, user_name=user.name, company_name=company_name)

@dashboard_bp.route('/dashboard/today')
@login_required
def dashboard_today():
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('under_development.html', user=user, page_title="Today")

@dashboard_bp.route('/dashboard/notifications')
@login_required
def dashboard_notifications():
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('under_development.html', user=user, page_title="Notifications")

@dashboard_bp.route('/dashboard/quick-add')
@login_required
def dashboard_quick_add():
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('under_development.html', user=user, page_title="Quick Add")

@dashboard_bp.route('/dashboard/search')
@login_required
def dashboard_search():
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('under_development.html', user=user, page_title="Search")

@dashboard_bp.route('/dashboard/settings')
@login_required
def dashboard_settings():
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    return render_template('under_development.html', user=user, page_title="Settings")

@dashboard_bp.route('/company/view')
@login_required
def view_company():
    """View company information page"""
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    # Get company information
    organization = user.organization
    company_name = organization.name if organization else "Your Company"
    company_address = organization.location if organization else ""
    latitude = organization.latitude if organization else None
    longitude = organization.longitude if organization else None
    google_maps_api_key = Config.GOOGLE_MAPS_API_KEY
    
    return render_template(
        'view_company.html',
        user=user,
        company_name=company_name,
        company_address=company_address,
        latitude=latitude,
        longitude=longitude,
        google_maps_api_key=google_maps_api_key
    )

@dashboard_bp.route('/company/edit-address')
@login_required
def edit_company_address():
    """Edit company address page with Google Maps autocomplete"""
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    if not user.organization:
        return redirect('/dashboard')
    
    organization = user.organization
    company_name = organization.name
    current_address = organization.location or ""
    latitude = organization.latitude
    longitude = organization.longitude
    google_maps_api_key = Config.GOOGLE_MAPS_API_KEY
    
    return render_template(
        'edit_company_address.html',
        user=user,
        company_name=company_name,
        current_address=current_address,
        latitude=latitude,
        longitude=longitude,
        google_maps_api_key=google_maps_api_key
    )

@dashboard_bp.route('/employee/maintenance')
@login_required
def employee_maintenance():
    """Maintenance page for employee accounts"""
    user = User.query.get(session['user_id'])
    
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    # Only allow employee accounts to access this page
    if not hasattr(user, 'role') or user.role != 'employee':
        return redirect('/dashboard')
    
    return render_template('employee_maintenance.html', user=user)

@dashboard_bp.route('/company/api/update-address', methods=['POST'])
@login_required
def update_company_address():
    """API endpoint to update company address and coordinates"""
    user = User.query.get(session['user_id'])
    
    if not user or not user.organization:
        return jsonify({'success': False, 'error': 'User or organization not found'}), 404
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        address = data.get('address', '').strip()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Validate coordinates if provided
        if latitude is not None:
            try:
                latitude = float(latitude)
                if not (-90 <= latitude <= 90):
                    return jsonify({'success': False, 'error': 'Invalid latitude value'}), 400
            except (ValueError, TypeError):
                return jsonify({'success': False, 'error': 'Invalid latitude format'}), 400
        
        if longitude is not None:
            try:
                longitude = float(longitude)
                if not (-180 <= longitude <= 180):
                    return jsonify({'success': False, 'error': 'Invalid longitude value'}), 400
            except (ValueError, TypeError):
                return jsonify({'success': False, 'error': 'Invalid longitude format'}), 400
        
        # Update organization
        organization = user.organization
        organization.location = address if address else None
        organization.latitude = latitude
        organization.longitude = longitude
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Address updated successfully',
            'address': address,
            'latitude': latitude,
            'longitude': longitude
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Failed to update address: {str(e)}'}), 500