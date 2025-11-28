#!/usr/bin/env python3
"""
Migration script to add latitude and longitude columns to Organization table
Run this script to update the database schema: python migrate_add_organization_coordinates.py
"""

import sqlite3
import os
from config.settings import DevelopmentConfig

def migrate_database():
    """Add latitude and longitude columns to Organization table"""
    
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
        cursor.execute("PRAGMA table_info(organization)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"   Current columns: {columns}")
        
        changes_made = False
        
        # Add latitude column if it doesn't exist
        if 'latitude' not in columns:
            print("   ➕ Adding 'latitude' column...")
            cursor.execute("ALTER TABLE organization ADD COLUMN latitude REAL")
            changes_made = True
            print("   ✅ 'latitude' column added successfully")
        else:
            print("   ✓ 'latitude' column already exists")
        
        # Add longitude column if it doesn't exist
        if 'longitude' not in columns:
            print("   ➕ Adding 'longitude' column...")
            cursor.execute("ALTER TABLE organization ADD COLUMN longitude REAL")
            changes_made = True
            print("   ✅ 'longitude' column added successfully")
        else:
            print("   ✓ 'longitude' column already exists")
        
        # Commit changes
        if changes_made:
            conn.commit()
            print("\n✅ Migration completed successfully!")
        else:
            print("\n✓ Database already up to date - no changes needed")
        
        # Verify the changes
        print("\n🔍 Verifying migration...")
        cursor.execute("PRAGMA table_info(organization)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"   Updated columns: {new_columns}")
        
        # Check if columns exist
        if 'latitude' in new_columns and 'longitude' in new_columns:
            print("   ✅ Both latitude and longitude columns are present")
        
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
    print("Organization Coordinates Migration Script")
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

