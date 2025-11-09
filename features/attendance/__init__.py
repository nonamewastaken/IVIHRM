from flask import Blueprint

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance', static_folder='static', template_folder='templates')

from . import routes

