from app import db
from datetime import datetime

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    programs = db.relationship('Program', backref='department', lazy='dynamic')
    teachers = db.relationship('Teacher', backref='department', lazy='dynamic')
    admins = db.relationship('Admin', backref='department', lazy='dynamic')
    
    def __repr__(self):
        return f'<Department {self.name}>'
    
    def get_teachers_count(self):
        return self.teachers.count()
    
    def get_students_count(self):
        return sum(program.students.count() for program in self.programs)

class Program(db.Model):
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True)
    level = db.Column(db.String(20))  # 'License', 'Master', etc.
    duration = db.Column(db.Integer)  # Duration in semesters
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', backref='program', lazy='dynamic')
    courses = db.relationship('Course', backref='program', lazy='dynamic')
    
    def __repr__(self):
        return f'<Program {self.name} ({self.level})>'
    
    def get_current_semester(self):
        """Calculate current semester based on academic calendar"""
        # TODO: Implement semester calculation logic
        return 1
    
    def get_total_credits(self):
        """Calculate total credits for the program"""
        return sum(course.credits for course in self.courses)
    
    def get_students_by_year(self, year):
        """Get students enrolled in a specific year"""
        return self.students.filter_by(enrollment_year=year).all()
    
    def get_active_courses(self):
        """Get currently active courses for the program"""
        current_semester = self.get_current_semester()
        return self.courses.filter_by(semester=current_semester).all()
