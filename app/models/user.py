from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Admin(User):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

class Teacher(User):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    is_permanent = db.Column(db.Boolean, default=True)
    weekly_hours = db.Column(db.Integer, default=0)
    courses = db.relationship('Course', backref='teacher', lazy='dynamic')
    
    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }
    
    def calculate_weekly_hours(self):
        """Calculate total weekly teaching hours"""
        total_hours = 0
        for course in self.courses:
            total_hours += course.duration
        self.weekly_hours = total_hours
        return total_hours

class Student(User):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    enrollment_year = db.Column(db.Integer)
    student_id = db.Column(db.String(20), unique=True)  # Student ID number
    
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
