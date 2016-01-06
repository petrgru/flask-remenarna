from flask import Blueprint

aplikace = Blueprint('aplikace', __name__, template_folder='templates')

import views
