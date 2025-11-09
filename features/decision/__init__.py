from flask import Blueprint

decision_bp = Blueprint('decision', __name__, static_folder='static', template_folder='templates')

from . import routes
