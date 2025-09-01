from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
