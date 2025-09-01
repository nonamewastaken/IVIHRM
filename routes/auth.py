from flask import Blueprint, request, jsonify, session, make_response, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password=hashed_password,
        name=data.get('name', '')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

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

        session.clear()
        session['user_id'] = user.id
        session.modified = True

        response = make_response(jsonify({
            'message': 'Login successful',
            'user': {
                'email': user.email,
                'name': user.name
            }
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
        last_name=last_name
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return jsonify({
            'message': 'Signup successful',
            'redirect': '/complete-profile'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred during signup'}), 500

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
