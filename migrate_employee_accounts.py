#!/usr/bin/env python3
"""
Migration script to create user accounts for existing employees
that don't have accounts yet. Uses personal_email and generates random passwords.
Run this script once: python migrate_employee_accounts.py
"""

from app import app
from models import User, Employee
from core.database import db
from werkzeug.security import generate_password_hash
import secrets
import string

def migrate_employee_accounts():
    """Create user accounts for employees that don't have accounts"""
    
    with app.app_context():
        try:
            print("=" * 60)
            print("Employee Account Migration Script")
            print("=" * 60)
            print()
            
            # Get all employees
            employees = Employee.query.all()
            print(f"📋 Found {len(employees)} employees in database")
            print()
            
            created_count = 0
            skipped_count = 0
            error_count = 0
            
            for employee in employees:
                # Check if employee already has a linked user account
                existing_user = User.query.filter_by(employee_id=employee.id).first()
                
                if existing_user:
                    print(f"⏭️  Skipping {employee.full_name} - Already has account ({existing_user.email})")
                    skipped_count += 1
                    continue
                
                # Check if employee has personal email
                if not employee.personal_email:
                    print(f"⏭️  Skipping {employee.full_name} - No personal email")
                    skipped_count += 1
                    continue
                
                # Check if email is already taken by another user
                email_taken = User.query.filter_by(email=employee.personal_email).filter(User.employee_id != employee.id).first()
                if email_taken:
                    print(f"⚠️  Skipping {employee.full_name} - Email {employee.personal_email} already taken by another user")
                    skipped_count += 1
                    continue
                
                # Generate random password
                alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
                random_password = ''.join(secrets.choice(alphabet) for i in range(16))
                
                # Get organization_id from first admin user (if available)
                admin_user = User.query.filter_by(role='admin').first()
                organization_id = admin_user.organization_id if admin_user else None
                
                # Split full name into first and last name
                name_parts = employee.full_name.split() if employee.full_name else []
                first_name = name_parts[0] if name_parts else None
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else None
                
                # Create employee user account
                employee_user = User(
                    email=employee.personal_email,
                    password=generate_password_hash(random_password),
                    role='employee',
                    employee_id=employee.id,
                    organization_id=organization_id,
                    profile_completed=True,
                    first_name=first_name,
                    last_name=last_name
                )
                
                db.session.add(employee_user)
                db.session.commit()
                
                print(f"✅ Created account for {employee.full_name}")
                print(f"   Email: {employee.personal_email}")
                print(f"   Password: {random_password}")
                print()
                
                created_count += 1
                
            except Exception as e:
                print(f"❌ Error creating account for {employee.full_name}: {e}")
                db.session.rollback()
                error_count += 1
                continue
            
            print()
            print("=" * 60)
            print("Migration Summary")
            print("=" * 60)
            print(f"✅ Created: {created_count} accounts")
            print(f"⏭️  Skipped: {skipped_count} employees")
            if error_count > 0:
                print(f"❌ Errors: {error_count} employees")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    migrate_employee_accounts()

