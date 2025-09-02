from flask import Blueprint

attendance_bp = Blueprint('attendance', __name__, template_folder='templates', static_folder='static')

from . import routes

