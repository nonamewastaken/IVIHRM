#!/usr/bin/env python3
"""
Script to create database tables manually
Run this if the tables don't exist: python create_tables.py
"""

from app import app
from core.database import db
import models

def create_tables():
    """Create all database tables"""
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            print("Tables created:", list(db.metadata.tables.keys()))
            
            # Test if we can query the attendance table
            try:
                count = Attendance.query.count()
                print(f"✅ Attendance table is accessible (contains {count} records)")
            except Exception as e:
                print(f"❌ Error accessing attendance table: {e}")
                
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            raise e

if __name__ == '__main__':
    create_tables()
