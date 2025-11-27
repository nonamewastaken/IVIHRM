from flask import request, jsonify, render_template, redirect, session
from models import User, Organization, db
from datetime import datetime
from core.auth import api_login_required
from config.settings import Config
from . import onboarding_bp

@onboarding_bp.route('/complete-profile')
def complete_profile():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    
    if user.profile_completed:
        return redirect('/dashboard')
        
    # Get stored profile data from session
    profile_data = session.get('profile_data', {})
        
    return render_template('complete_profile.html', user=user, profile_data=profile_data)

@onboarding_bp.route('/api/complete-profile', methods=['POST'])
@api_login_required
def submit_complete_profile():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['citizenship', 'dateOfBirth', 'phoneNumber']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Store profile data in session
        session['profile_data'] = {
            'citizenship': data['citizenship'],
            'date_of_birth': data['dateOfBirth'],
            'phone_number': data['phoneNumber']
        }
        return jsonify({
            'message': 'Profile data stored',
            'redirect': '/organization-setup'
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to store profile data'}), 500

@onboarding_bp.route('/organization-setup')
def organization_setup():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    if user.organization_id:
        return redirect('/dashboard')

    # Get stored organization data from session
    organization_data = session.get('organization_data', {})
    google_maps_api_key = Config.GOOGLE_MAPS_API_KEY
    
    return render_template('organization_setup.html', organization_data=organization_data, user=user, google_maps_api_key=google_maps_api_key)

@onboarding_bp.route('/api/setup-organization', methods=['POST'])
@api_login_required
def setup_organization():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['organizationName', 'location']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Store organization data in session (including optional coordinates)
        session['organization_data'] = {
            'name': data['organizationName'],
            'location': data['location'],
            'latitude': data.get('latitude'),  # Optional
            'longitude': data.get('longitude')  # Optional
        }
        
        return jsonify({
            'message': 'Organization data stored',
            'redirect': '/people-count'
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to store organization data'}), 500

@onboarding_bp.route('/people-count')
def people_count():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')

    if user.organization_id:
        return redirect('/dashboard')

    # Get stored size data from session
    size_data = session.get('size_data', {})
    
    return render_template('people_count.html', size_data=size_data, user=user)

@onboarding_bp.route('/api/update-organization-size', methods=['POST'])
@api_login_required
def update_organization_size():
    data = request.get_json()
    
    if not data or 'size' not in data:
        return jsonify({'error': 'Missing size field'}), 400

    try:
        # Store size data in session first
        session['size_data'] = {
            'size': data['size']
        }

        # Only create organization and update user if this is final submission
        if data.get('isSubmitting', True):  # Default to True for backward compatibility
            # Check if required session data exists
            if 'organization_data' not in session:
                return jsonify({'error': 'Organization data missing. Please go back and complete organization setup.'}), 400
            
            if 'profile_data' not in session:
                return jsonify({'error': 'Profile data missing. Please go back and complete profile setup.'}), 400
            
            # Create new organization with all the stored data (including coordinates if available)
            org_data = session['organization_data']
            org = Organization(
                name=org_data['name'],
                location=org_data['location'],
                size=data['size'],
                latitude=org_data.get('latitude'),  # Optional coordinates
                longitude=org_data.get('longitude')  # Optional coordinates
            )
            db.session.add(org)
            db.session.flush()  # Get the org.id before commit
            
            # Update user with all the stored data
            user = User.query.get(session['user_id'])
            if not user:
                db.session.rollback()
                return jsonify({'error': 'User not found. Please log in again.'}), 401
            
            profile_data = session['profile_data']
            user.citizenship = profile_data.get('citizenship')
            user.date_of_birth = profile_data.get('date_of_birth')
            user.phone = profile_data.get('phone_number')
            user.organization_id = org.id
            user.profile_completed = True
            
            # Commit all changes to database
            db.session.commit()

            # Clear temporary session data after successful commit (but keep user_id in session)
            session.pop('profile_data', None)
            session.pop('organization_data', None)
            session.pop('size_data', None)
            
            # Ensure session is saved
            session.modified = True

            # Keep user logged in and redirect to dashboard
            return jsonify({
                'message': 'Setup completed successfully',
                'redirect': '/dashboard'
            }), 200
        else:
            # If not final submission, just store the data and return success
            return jsonify({
                'message': 'Size data stored',
                'redirect': None
            }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to complete setup'}), 500
