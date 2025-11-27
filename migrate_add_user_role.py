#!/usr/bin/env python3
"""
Migration script to add role and employee_id columns to User table
Run this script to update the database schema: python migrate_add_user_role.py
"""

import sqlite3
import os
from config.settings import DevelopmentConfig

def migrate_database():
    """Add role and employee_id columns to User table"""
    
    # Get database path
    db_path = DevelopmentConfig.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"📦 Database found at: {db_path}")
        print("🔍 Checking current schema...")
        
        # Get current columns
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"   Current columns: {columns}")
        
        changes_made = False
        
        # Add role column if it doesn't exist
        if 'role' not in columns:
            print("   ➕ Adding 'role' column...")
            cursor.execute("ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'admin'")
            changes_made = True
            print("   ✅ 'role' column added successfully")
        else:
            print("   ✓ 'role' column already exists")
        
        # Add employee_id column if it doesn't exist
        if 'employee_id' not in columns:
            print("   ➕ Adding 'employee_id' column...")
            cursor.execute("ALTER TABLE user ADD COLUMN employee_id INTEGER")
            changes_made = True
            print("   ✅ 'employee_id' column added successfully")
        else:
            print("   ✓ 'employee_id' column already exists")
        
        # Update existing users to have role='admin' if role is NULL
        if 'role' in columns or changes_made:
            cursor.execute("UPDATE user SET role = 'admin' WHERE role IS NULL")
            updated_count = cursor.rowcount
            if updated_count > 0:
                print(f"   🔄 Updated {updated_count} existing users to have role='admin'")
        
        # Commit changes
        if changes_made:
            conn.commit()
            print("\n✅ Migration completed successfully!")
        else:
            print("\n✓ Database already up to date - no changes needed")
        
        # Verify the changes
        print("\n🔍 Verifying migration...")
        cursor.execute("PRAGMA table_info(user)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"   Updated columns: {new_columns}")
        
        # Check if role column exists and show sample data
        if 'role' in new_columns:
            cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'employee'")
            employee_count = cursor.fetchone()[0]
            print(f"   Users with role='admin': {admin_count}")
            print(f"   Users with role='employee': {employee_count}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.close()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("User Role Migration Script")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    print()
    print("=" * 60)
    if success:
        print("✅ Migration script completed!")
        print("\nYou can now restart your application.")
    else:
        print("❌ Migration script failed!")
        print("Please check the error messages above.")
    print("=" * 60)

