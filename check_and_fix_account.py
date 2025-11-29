#!/usr/bin/env python3
"""
Script to check and fix a specific employee account name
"""

from app import app
from models import User, Employee
from core.database import db

def check_and_fix_account(email):
    """Check and fix account name for a specific email"""
    
    with app.app_context():
        try:
            print("=" * 60)
            print(f"Checking account: {email}")
            print("=" * 60)
            print()
            
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            if not user:
                print(f"❌ User account not found for email: {email}")
                return
            
            print(f"✅ Found user account:")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Role: {user.role}")
            print(f"   First Name: {user.first_name}")
            print(f"   Last Name: {user.last_name}")
            print(f"   Employee ID: {user.employee_id}")
            print()
            
            # Check if user has employee_id
            if not user.employee_id:
                print("⚠️  User account is not linked to an employee record")
                return
            
            # Get linked employee
            employee = Employee.query.get(user.employee_id)
            
            if not employee:
                print(f"⚠️  Linked employee record not found (employee_id: {user.employee_id})")
                return
            
            print(f"✅ Found linked employee:")
            print(f"   Employee ID: {employee.id}")
            print(f"   Full Name: {employee.full_name}")
            print()
            
            # Check if name needs syncing
            if not user.first_name or not user.last_name:
                print("🔧 Name is missing, syncing from employee.full_name...")
                
                if employee.full_name:
                    name_parts = employee.full_name.strip().split()
                    if name_parts:
                        user.first_name = name_parts[0].capitalize()
                        if len(name_parts) > 1:
                            # Capitalize each word in last_name
                            last_name_parts = [part.capitalize() for part in name_parts[1:]]
                            user.last_name = ' '.join(last_name_parts)
                        else:
                            user.last_name = None
                        
                        db.session.commit()
                        print(f"✅ Synced name: {user.first_name} {user.last_name}")
                    else:
                        print("⚠️  Employee full_name is empty")
                else:
                    print("⚠️  Employee has no full_name to sync from")
            else:
                print(f"ℹ️  Name is already set: {user.first_name} {user.last_name}")
                print("   Checking if it matches employee.full_name...")
                
                if employee.full_name:
                    expected_parts = employee.full_name.strip().split()
                    if expected_parts:
                        expected_first = expected_parts[0].capitalize()
                        if len(expected_parts) > 1:
                            last_name_parts = [part.capitalize() for part in expected_parts[1:]]
                            expected_last = ' '.join(last_name_parts)
                        else:
                            expected_last = None
                        
                        if user.first_name != expected_first or user.last_name != expected_last:
                            print("🔧 Name doesn't match, updating...")
                            user.first_name = expected_first
                            user.last_name = expected_last
                            db.session.commit()
                            print(f"✅ Updated name: {user.first_name} {user.last_name}")
                        else:
                            print("✅ Name matches employee.full_name")
            
            print()
            print("=" * 60)
            print("Final Account Status:")
            print("=" * 60)
            print(f"Email: {user.email}")
            print(f"Name: {user.first_name} {user.last_name}")
            print(f"Display Name: {user.name}")
            print(f"Employee Full Name: {employee.full_name}")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    import sys
    email = sys.argv[1] if len(sys.argv) > 1 else "zzzminhkhang27062008@gmail.com"
    check_and_fix_account(email)

