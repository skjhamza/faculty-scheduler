from .user import User, Admin, Teacher, Student
from .department import Department, Program
from .schedule import Schedule, Course, TimeSlot
from .room import Room

__all__ = [
    'User', 'Admin', 'Teacher', 'Student',
    'Department', 'Program',
    'Schedule', 'Course', 'TimeSlot',
    'Room'
]
