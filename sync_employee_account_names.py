#!/usr/bin/env python3
"""
Migration script to sync employee user account names from employee.full_name
for existing accounts that have None or empty first_name/last_name.
Run this script once: python sync_employee_account_names.py
"""

from app import app
from models import User, Employee
from core.database import db

def sync_employee_account_names():
    """Sync employee user account names from employee.full_name"""
    
    with app.app_context():
        try:
            print("=" * 60)
            print("Employee Account Name Sync Script")
            print("=" * 60)
            print()
            
            # Get all employee user accounts
            employee_users = User.query.filter(User.employee_id.isnot(None)).all()
            print(f"📋 Found {len(employee_users)} employee user accounts")
            print()
            
            synced_count = 0
            skipped_count = 0
            error_count = 0
            
            for user in employee_users:
                try:
                    # Get the linked employee
                    employee = Employee.query.get(user.employee_id)
                    if not employee:
                        print(f"⚠️  Skipping user {user.email} - Linked employee not found")
                        skipped_count += 1
                        continue
                    
                    # Check if name needs syncing
                    if user.first_name and user.last_name:
                        print(f"⏭️  Skipping {user.email} - Name already set: {user.first_name} {user.last_name}")
                        skipped_count += 1
                        continue
                    
                    # Check if employee has full_name
                    if not employee.full_name:
                        print(f"⚠️  Skipping {user.email} - Employee has no full_name")
                        skipped_count += 1
                        continue
                    
                    # Extract and set name
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
                        print(f"✅ Synced name for {user.email}: {user.first_name} {user.last_name}")
                        synced_count += 1
                    else:
                        print(f"⚠️  Skipping {user.email} - Employee full_name is empty")
                        skipped_count += 1
                        
                except Exception as e:
                    print(f"❌ Error syncing name for {user.email}: {e}")
                    db.session.rollback()
                    error_count += 1
                    continue
            
            print()
            print("=" * 60)
            print("Sync Summary")
            print("=" * 60)
            print(f"✅ Synced: {synced_count} accounts")
            print(f"⏭️  Skipped: {skipped_count} accounts")
            if error_count > 0:
                print(f"❌ Errors: {error_count} accounts")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error during sync: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    sync_employee_account_names()

