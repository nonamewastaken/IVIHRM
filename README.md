# HRM System - Modular Architecture

A Flask-based Human Resource Management system with a clean, modular architecture designed for scalability and maintainability.

## Project Structure

```
HRM/
├── app.py                          # Main application entry point
├── models.py                       # Shared database models
├── requirements.txt                # Python dependencies
├── create_tables.py               # Database table creation script
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
│   │   └── templates/
│   │       ├── login.html
│   │       ├── signup.html
│   │       ├── reset_password.html
│   │       ├── new_password.html
│   │       └── check_inbox.html
│   ├── dashboard/                 # Dashboard feature
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── dashboard.html
│   ├── onboarding/                # User onboarding feature
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       ├── complete_profile.html
│   │       ├── organization_setup.html
│   │       └── people_count.html
│   ├── password_reset/            # Password reset feature
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── attendance/                # Attendance management feature
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       ├── overview.html
│   │       ├── attendance_history.html
│   │       ├── attendance_summary.html
│   │       ├── monthly_attendance_detail.html
│   │       └── work_data.html
│   ├── administrative_personnel/  # Personnel management feature
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   ├── personnel_dashboard.html
│   │   │   ├── add_employee.html
│   │   │   ├── employee_list.html
│   │   │   └── departments.html
│   │   └── static/
│   │       ├── css/
│   │       ├── images/
│   │       └── js/
│   ├── salary/                    # Salary management feature
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   ├── salary_dashboard.html
│   │   │   ├── calculate_salary.html
│   │   │   ├── payroll_list.html
│   │   │   └── salary_slips.html
│   │   └── static/
│   │       ├── css/
│   │       ├── images/
│   │       └── js/
│   └── decision/                  # Decision management feature
│       ├── __init__.py
│       ├── routes.py
│       ├── templates/
│       │   ├── decision_dashboard.html
│       │   ├── create_decision.html
│       │   ├── decision_list.html
│       │   └── hiring_decisions.html
│       └── static/
│           ├── css/
│           ├── images/
│           └── js/
├── shared/                        # Shared resources
│   ├── templates/
│   │   ├── base.html              # Base template
│   │   └── sidebar.html           # Sidebar template
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css           # Global styles
│   │   ├── js/
│   │   │   └── translations.js
│   │   └── images/
│   │       ├── building.png
│   │       ├── eye.png
│   │       ├── people-group.png
│   │       └── user.png
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── venv/                          # Virtual environment
```

## Main Folder Functions

### **Core Directory (`core/`)**
The core directory contains essential application functionality that is shared across all features:

- **`database.py`**: Database initialization and configuration using SQLAlchemy
- **`auth.py`**: Authentication utilities including login decorators and user session management
- **`decorators.py`**: Custom decorators for redirecting logged-in users and other common functionality

### **Features Directory (`features/`)**
The features directory contains modular, self-contained feature modules. Each feature has its own routes, templates, and static files:

- **`auth/`**: User authentication (login, signup, password reset)
- **`dashboard/`**: Main application dashboard and user interface
- **`onboarding/`**: User profile completion and organization setup
- **`password_reset/`**: Password reset functionality with email integration
- **`attendance/`**: Employee attendance tracking, check-in/out, and Excel import
- **`administrative_personnel/`**: Employee management, departments, and personnel administration
- **`salary/`**: Salary calculation, payroll management, and salary slip generation
- **`decision/`**: Decision management, hiring decisions, and organizational decisions

### **Shared Directory (`shared/`)**
The shared directory contains resources used across multiple features:

- **`templates/`**: Base templates (`base.html`, `sidebar.html`) for consistent UI
- **`static/`**: Global CSS, JavaScript, and images used across the application
- **`utils/`**: Helper functions and utilities for common operations

### **Config Directory (`config/`)**
Configuration management for different environments:

- **`settings.py`**: Application settings for development and production environments

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

### Attendance Management (`features/attendance/`)
- Employee check-in/check-out functionality
- Attendance history tracking
- Excel file import for bulk attendance data
- Monthly attendance reports and summaries
- Work data analysis and timesheet management
- Real-time attendance status tracking

### Administrative Personnel (`features/administrative_personnel/`)
- Employee management and administration
- Department management
- Employee list and profiles
- Personnel dashboard for HR operations

### Salary Management (`features/salary/`)
- Salary calculation and processing
- Payroll management
- Salary slip generation
- Salary dashboard for financial operations

### Decision Management (`features/decision/`)
- Organizational decision tracking
- Hiring decision management
- Decision creation and approval workflows
- Decision history and reporting

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd HRM
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database (Optional)**
   If the database tables don't exist, run:
   ```bash
   python create_tables.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   - Open your browser to `http://localhost:5001`
   - The application will automatically initialize the database on first run

### Required Files
- `requirements.txt` - Contains all Python dependencies
- `app.py` - Main application entry point
- `models.py` - Database models
- `create_tables.py` - Database initialization script (optional)

### Dependencies
The application requires the following Python packages:
- Flask 2.3.3 - Web framework
- Flask-SQLAlchemy 3.0.5 - Database ORM
- Flask-CORS 4.0.0 - Cross-origin resource sharing
- Flask-Mail 0.9.1 - Email functionality
- Werkzeug 2.3.7 - WSGI utilities
- SQLAlchemy 1.4.53 - Database toolkit
- openpyxl 3.1.2 - Excel file processing

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

- **User**: User accounts with complete profile information including personal details, contact info, and organization association
- **Organization**: Company/organization data with industry, size, and location information
- **Attendance**: Employee attendance records with check-in/out times, work hours, status tracking, and Excel import support

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

## Current Features Status

The system currently includes:
- ✅ User authentication and session management
- ✅ Employee attendance tracking with Excel import
- ✅ Personnel management and administration
- ✅ Salary calculation and payroll management
- ✅ Decision management and tracking
- ✅ Modular architecture for easy expansion

## Future Enhancements

This modular structure makes it easy to add:
- Performance review systems
- Document management
- Advanced reporting and analytics
- API endpoints for mobile applications
- Integration with external HR systems
- Advanced role-based access control
- Email notifications and alerts
- Data export and backup features

The architecture is designed to grow with your needs while maintaining clean separation of concerns and easy maintainability.
