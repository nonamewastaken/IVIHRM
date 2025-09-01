from flask import Blueprint

password_reset_bp = Blueprint('password_reset', __name__, template_folder='templates', static_folder='static')

from . import routes
