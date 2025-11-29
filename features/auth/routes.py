from flask import request, jsonify, session, make_response, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from . import auth_bp

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """Legacy register endpoint - use /api/signup instead"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Parse name if provided (for backward compatibility)
    name = data.get('name', '').strip()
    first_name = None
    last_name = None
    if name:
        name_parts = name.split(' ', 1)
        first_name = name_parts[0].capitalize() if name_parts else None
        last_name = name_parts[1].capitalize() if len(name_parts) > 1 else None

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        role='admin'  # Register creates admin accounts
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        print(f"ERROR in register: {str(e)}")
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        if not request.is_json:
            return jsonify({'error': 'Missing JSON in request'}), 400

        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Please enter both email and password'}), 400

        if not data['email'].strip() or not data['password'].strip():
            return jsonify({'error': 'Please enter both email and password'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return jsonify({'error': 'Email does not exist'}), 404

        if not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Incorrect password'}), 401

        # Ensure user has a role (default to 'admin' if missing)
        if not hasattr(user, 'role') or not user.role:
            user.role = 'admin'
            try:
                db.session.commit()
            except Exception as e:
                print(f"Warning: Could not update user role: {e}")
                db.session.rollback()

        session.clear()
        session['user_id'] = user.id
        session['user_role'] = user.role
        session.modified = True

        # All users (admin and employee) go to dashboard
        redirect_url = '/dashboard'

        response = make_response(jsonify({
            'message': 'Login successful',
            'user': {
                'email': user.email,
                'name': user.name,
                'role': user.role if hasattr(user, 'role') else 'admin'
            },
            'redirect': redirect_url
        }))
        
        return response, 200

    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName', '').strip()
    last_name = data.get('lastName', '').strip()

    if not email or not password:
        return jsonify({'error': 'Please enter both email and password'}), 400

    if not first_name or not last_name:
        return jsonify({'error': 'Please enter both first and last name'}), 400

    first_name = first_name.capitalize()
    last_name = last_name.capitalize()

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        email=email, 
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        role='admin'  # Signup creates admin accounts
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        session['user_role'] = 'admin'  # Explicitly set role in session
        session.modified = True
        return jsonify({
            'message': 'Signup successful',
            'redirect': '/complete-profile',
            'user': {
                'email': new_user.email,
                'name': new_user.name,
                'role': new_user.role
            }
        })
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        print(f"ERROR in signup: {str(e)}")
        return jsonify({'error': f'An error occurred during signup: {str(e)}'}), 500

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully', 'redirect': '/login'}), 200

@auth_bp.route('/logout', methods=['GET'])
def logout_get():
    session.clear()
    return redirect('/login')

@auth_bp.route('/api/check-login', methods=['GET'])
def check_login():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return jsonify({'error': 'User not found'}), 401

    return jsonify({
        'message': 'Logged in',
        'user': {
            'email': user.email,
            'name': user.name
        }
    }), 200
