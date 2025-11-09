from flask import Blueprint

administrative_personnel_bp = Blueprint('administrative_personnel', __name__, static_folder='static', template_folder='templates')

from . import routes
