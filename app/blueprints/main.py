from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    # Ensure this template exists
    return render_template('index.html')


@main_bp.route('/home')
def home():
    # Ensure this template exists
    return render_template('index.html')
