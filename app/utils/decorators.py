from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*roles):
    """Decorator to restrict access based on user roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.type not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator for admin-only routes"""
    return role_required('admin')(f)

def teacher_required(f):
    """Decorator for teacher-only routes"""
    return role_required('teacher')(f)

def student_required(f):
    """Decorator for student-only routes"""
    return role_required('student')(f)
