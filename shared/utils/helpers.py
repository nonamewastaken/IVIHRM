"""Shared utility functions"""

def format_user_name(user):
    """Format user name for display"""
    if user.preferred_name:
        return user.preferred_name
    if user.first_name and user.last_name:
        return f"{user.first_name} {user.last_name}"
    return "User"

def get_company_name(user):
    """Get company name for display"""
    return user.organization.name if user.organization else "Your Company"
