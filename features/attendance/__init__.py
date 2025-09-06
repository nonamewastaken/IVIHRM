from flask import Blueprint

attendance_bp = Blueprint('attendance', __name__, static_folder='static')

from . import routes

