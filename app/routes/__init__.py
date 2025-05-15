from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
teacher_bp = Blueprint('teacher', __name__)
student_bp = Blueprint('student', __name__)

# Import routes
from . import auth
from . import admin
from . import teacher
from . import student

__all__ = ['auth_bp', 'admin_bp', 'teacher_bp', 'student_bp']
