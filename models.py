from datetime import datetime
from core.database import db

# User model (enhanced for complete onboarding)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    preferred_name = db.Column(db.String(80))
    date_of_birth = db.Column(db.String(20))
    citizenship = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    tax_residence = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_completed = db.Column(db.Boolean, default=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    
    # Relationship
    organization = db.relationship('Organization', back_populates='users')

    @property
    def name(self):
        if self.preferred_name:
            return self.preferred_name
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return "None"

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'preferred_name': self.preferred_name,
            'profile_completed': self.profile_completed,
            'organization_id': self.organization_id
        }

# Employee model for personnel management
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    full_name = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10))  # male, female
    date_of_birth = db.Column(db.String(20))  # dd/mm/yyyy format
    place_of_birth = db.Column(db.String(200))
    hometown = db.Column(db.String(200))
    marital_status = db.Column(db.String(20))  # single, married, other
    ethnicity = db.Column(db.String(100))
    religion = db.Column(db.String(100))
    
    # Contact Information
    personal_phone = db.Column(db.String(20), nullable=False)
    personal_email = db.Column(db.String(120), nullable=False)
    
    # Tax and Insurance
    personal_tax_code = db.Column(db.String(50))
    social_insurance_code = db.Column(db.String(50))
    
    # Party Information
    party_join_date = db.Column(db.String(20))  # dd/mm/yyyy format
    party_join_place = db.Column(db.String(200))
    
    # Health Information
    health_status = db.Column(db.String(50))
    emergency_contact = db.Column(db.String(200))
    
    # Address Information
    permanent_address = db.Column(db.Text)
    permanent_province = db.Column(db.String(100))
    permanent_ward = db.Column(db.String(100))
    permanent_street = db.Column(db.String(200))
    
    current_address = db.Column(db.Text)
    current_province = db.Column(db.String(100))
    current_ward = db.Column(db.String(100))
    current_street = db.Column(db.String(200))
    
    # ID Card Information
    id_card_number = db.Column(db.String(50), nullable=False)
    id_card_issue_date = db.Column(db.String(20), nullable=False)  # dd/mm/yyyy format
    id_card_expiry_date = db.Column(db.String(20))
    id_card_issue_place = db.Column(db.String(200), nullable=False)
    
    # Passport Information
    passport_number = db.Column(db.String(50))
    passport_issue_date = db.Column(db.String(20))  # dd/mm/yyyy format
    passport_expiry_date = db.Column(db.String(20))
    passport_issue_place = db.Column(db.String(200))
    
    # File uploads (stored as file paths or base64)
    cv_file = db.Column(db.Text)  # CV image
    portrait_file = db.Column(db.Text)  # Portrait photo
    health_file = db.Column(db.Text)  # Health certificate
    id_card_file = db.Column(db.Text)  # ID card images
    passport_file = db.Column(db.Text)  # Passport images
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'place_of_birth': self.place_of_birth,
            'hometown': self.hometown,
            'marital_status': self.marital_status,
            'ethnicity': self.ethnicity,
            'religion': self.religion,
            'personal_phone': self.personal_phone,
            'personal_email': self.personal_email,
            'personal_tax_code': self.personal_tax_code,
            'social_insurance_code': self.social_insurance_code,
            'party_join_date': self.party_join_date,
            'party_join_place': self.party_join_place,
            'health_status': self.health_status,
            'emergency_contact': self.emergency_contact,
            'permanent_address': self.permanent_address,
            'permanent_province': self.permanent_province,
            'permanent_ward': self.permanent_ward,
            'permanent_street': self.permanent_street,
            'current_address': self.current_address,
            'current_province': self.current_province,
            'current_ward': self.current_ward,
            'current_street': self.current_street,
            'id_card_number': self.id_card_number,
            'id_card_issue_date': self.id_card_issue_date,
            'id_card_expiry_date': self.id_card_expiry_date,
            'id_card_issue_place': self.id_card_issue_place,
            'passport_number': self.passport_number,
            'passport_issue_date': self.passport_issue_date,
            'passport_expiry_date': self.passport_expiry_date,
            'passport_issue_place': self.passport_issue_place,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Organization model
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(80))
    size = db.Column(db.String(50))
    location = db.Column(db.String(120))
    logo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', back_populates='organization')

# Attendance model
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Made nullable for Excel import
    date = db.Column(db.Date, nullable=True)  # Made nullable for Excel import
    check_in_time = db.Column(db.DateTime)
    check_out_time = db.Column(db.DateTime)
    work_hours = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='present')  # present, absent, late, half_day
    notes = db.Column(db.Text)
    
    # Excel import fields
    employee_no = db.Column(db.String(50))  # Employee number from Excel
    employee_name = db.Column(db.String(200))  # Employee name from Excel
    year = db.Column(db.Integer)  # Year for monthly data
    month = db.Column(db.Integer)  # Month for monthly data
    daily_attendance = db.Column(db.Text)  # Comma-separated daily attendance data
    other_data = db.Column(db.Text)  # JSON string of other columns data
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='attendance_records')
    
    def __repr__(self):
        return f'<Attendance {self.user_id} - {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'check_in_time': self.check_in_time.strftime('%H:%M:%S') if self.check_in_time else None,
            'check_out_time': self.check_out_time.strftime('%H:%M:%S') if self.check_out_time else None,
            'work_hours': self.work_hours,
            'status': self.status,
            'notes': self.notes
        }
