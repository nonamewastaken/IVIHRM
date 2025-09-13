from flask import Blueprint

salary_bp = Blueprint('salary', __name__, static_folder='static', template_folder='templates')

from . import routes
