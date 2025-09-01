# HRM System - Modular Architecture

A Flask-based Human Resource Management system with a clean, modular architecture designed for scalability and maintainability.

## Project Structure

```
HRM-3/
├── app.py                          # Main application entry point
├── models.py                       # Shared database models
├── requirements.txt                # Python dependencies
├── users.db                        # SQLite database
├── config/                         # Configuration files
│   ├── __init__.py
│   └── settings.py                 # Application settings
├── core/                          # Core application functionality
│   ├── __init__.py
│   ├── database.py                # Database initialization
│   ├── auth.py                    # Authentication utilities
│   └── decorators.py              # Custom decorators
├── features/                      # Feature-based modules
│   ├── __init__.py
│   ├── auth/                      # Authentication feature
│   │   ├── __init__.py
│   │   ├── routes.py              # Auth routes
│   │   ├── templates/
│   │   │   ├── login.html
│   │   │   ├── signup.html
│   │   │   ├── reset_password.html
│   │   │   ├── new_password.html
│   │   │   └── check_inbox.html
│   │   └── static/
│   │       ├── css/
│   │       └── js/
│   ├── dashboard/                 # Dashboard feature
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   └── dashboard.html
│   │   └── static/
│   ├── onboarding/                # User onboarding feature
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   ├── complete_profile.html
│   │   │   ├── organization_setup.html
│   │   │   └── people_count.html
│   │   └── static/
│   └── password_reset/            # Password reset feature
│       ├── __init__.py
│       ├── routes.py
│       └── templates/
├── shared/                        # Shared resources
│   ├── templates/
│   │   └── base.html              # Base template
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css           # Global styles
│   │   ├── js/
│   │   │   └── translations.js
│   │   └── images/
│   │       ├── arrow-left.png
│   │       ├── building.png
│   │       └── [other shared images]
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── tests/                         # Test files
    ├── __init__.py
    ├── test_auth.py
    ├── test_dashboard.py
    └── test_onboarding.py
```

## Architecture Benefits

### 1. **Feature Isolation**
- Each feature is self-contained with its own routes, templates, and static files
- Easy to add new features without affecting existing ones
- Clear boundaries make debugging and updates easier

### 2. **Shared Resources**
- Common assets (images, global CSS) are in a shared location
- Base templates provide consistent styling across features
- Utility functions are centralized for reuse

### 3. **Scalability**
- New features can be added by creating new directories under `features/`
- Each feature can have its own database models, services, and business logic
- Team members can work on different features independently

### 4. **Maintainability**
- Clear separation of concerns
- Easy to locate and fix bugs
- Consistent structure across all features

## Key Features

### Authentication (`features/auth/`)
- User registration and login
- Password reset functionality
- Session management
- Authentication decorators

### Dashboard (`features/dashboard/`)
- Main application dashboard
- User profile display
- Company information

### Onboarding (`features/onboarding/`)
- User profile completion
- Organization setup
- Employee count configuration

### Password Reset (`features/password_reset/`)
- Password reset request
- Email-based reset links
- Secure token handling

## Getting Started

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python3 app.py
   ```

3. **Access the Application**
   - Open your browser to `http://localhost:5001`
   - The application will automatically initialize the database

## Configuration

The application uses a configuration system located in `config/settings.py`:

- **Development**: Default configuration with SQLite database
- **Production**: Production-ready settings (configure as needed)

## Adding New Features

To add a new feature:

1. Create a new directory under `features/`
2. Add `__init__.py`, `routes.py`, and template/static directories
3. Create a Blueprint in `__init__.py`
4. Register the Blueprint in `app.py`
5. Add any shared utilities to `shared/utils/`

## Database Models

All database models are defined in `models.py` and use SQLAlchemy:

- **User**: User accounts with profile information
- **Organization**: Company/organization data

## Security Features

- Password hashing with Werkzeug
- Session management
- CSRF protection
- Secure cookie settings

## Development Guidelines

1. **Feature Development**: Keep feature-specific code within feature directories
2. **Shared Code**: Place reusable code in `shared/` or `core/`
3. **Templates**: Use the base template for consistent styling
4. **Static Files**: Organize assets by feature or place in shared if used globally
5. **Testing**: Add tests in the `tests/` directory

## Future Enhancements

This modular structure makes it easy to add:
- Employee management features
- Payroll systems
- Time tracking
- Performance reviews
- Document management
- API endpoints
- Mobile applications

The architecture is designed to grow with your needs while maintaining clean separation of concerns and easy maintainability.
