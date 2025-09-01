from flask import request, jsonify, render_template
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta
import urllib.parse
from . import password_reset_bp

@password_reset_bp.route('/reset-password')
def reset_password_page():
    return render_template('reset_password.html')

@password_reset_bp.route('/check-inbox')
def check_inbox():
    email = request.args.get('email', '')
    return render_template('check_inbox.html', email=email)

@password_reset_bp.route('/api/request-password-reset', methods=['POST'])
def request_password_reset():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Please enter your email'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Email does not exist'}), 404

        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)

        try:
            db.session.commit()
            
            reset_link = f"http://{request.host}/reset-password/{urllib.parse.quote(token)}"
            
            email_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        background-color: #ffffff;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #FFE169;
                        padding: 40px;
                    }}
                    .content {{
                        text-align: center;
                    }}
                    h1 {{
                        font-size: 24px;
                        color: #1a1a1a;
                        margin-bottom: 20px;
                    }}
                    p {{
                        color: #1a1a1a;
                        margin-bottom: 30px;
                        font-size: 16px;
                    }}
                    .button {{
                        display: inline-block;
                        background-color: #1a1a1a;
                        color: white !important;
                        text-decoration: none;
                        padding: 12px 24px;
                        border-radius: 20px;
                        font-size: 16px;
                        margin: 20px 0;
                    }}
                    .footer {{
                        margin-top: 30px;
                        font-size: 14px;
                        color: #1a1a1a;
                    }}
                    .chat-link {{
                        color: #1a1a1a;
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="content">
                        <h1>Reset your password</h1>
                        <p>Just click the button below to set your password.</p>
                        <a href="{reset_link}" class="button" style="color: white !important;">Reset password</a>
                        <p>If you weren't expecting this email, please ignore this message.</p>
                        <div class="footer">
                            <p>Have a question? Reach out to us on <a href="#" class="chat-link">chat</a></p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """

            # Note: Email sending is commented out for the standalone version
            # You can uncomment and configure email settings if needed
            # from flask_mail import Message
            # msg = Message(
            #     subject='Reset your password',
            #     recipients=[email],
            #     html=email_html,
            #     sender='noreply@example.com'
            # )
            # mail.send(msg)

            return jsonify({'message': 'If your email is registered, you will receive reset instructions'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to send reset email. Please try again.'}), 500

    except Exception as e:
        return jsonify({'error': 'An error occurred. Please try again.'}), 500

@password_reset_bp.route('/reset-password/<token>')
def reset_password_with_token(token):
    try:
        decoded_token = urllib.parse.unquote(token)
        user = User.query.filter_by(reset_token=decoded_token).first()
        
        if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
            return render_template('new_password.html', token=token, error='Invalid or expired reset link. Please request a new one.')
        
        return render_template('new_password.html', token=token)
    except Exception as e:
        return render_template('new_password.html', token=token, error='Invalid reset link format. Please request a new one.')

@password_reset_bp.route('/api/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        decoded_token = urllib.parse.unquote(token)
        user = User.query.filter_by(reset_token=decoded_token).first()
        
        if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
            return jsonify({'error': 'Invalid or expired reset link'}), 400

        data = request.get_json()
        new_password = data.get('password')
        
        if not new_password:
            return jsonify({'error': 'Please enter a new password'}), 400

        try:
            if check_password_hash(user.password, new_password):
                return jsonify({'error': 'Your new password must not be the same as your previous one'}), 400

            user.password = generate_password_hash(new_password)
            user.reset_token = None
            user.reset_token_expiry = None
            db.session.commit()
            
            return jsonify({'message': 'Password reset successful'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to reset password'}), 500
    except Exception as e:
        return jsonify({'error': 'Invalid reset link format'}), 400
