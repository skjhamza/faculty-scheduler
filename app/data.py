from datetime import time
from app import db
from app.models import Department, Program, User, Teacher, Student, Room, Course, TimeSlot, Schedule

def init_db():
    """Initialize database with sample data"""
    
    # Create departments
    cs_dept = Department(name="Computer Science", code="CS")
    math_dept = Department(name="Mathematics", code="MATH")
    physics_dept = Department(name="Physics", code="PHY")
    db.session.add_all([cs_dept, math_dept, physics_dept])
    db.session.commit()

    # Create programs
    programs = [
        Program(name="Computer Science Engineering", code="CSE", level="ENGINEERING", duration=3, department=cs_dept),
        Program(name="Software Engineering", code="SE", level="ENGINEERING", duration=3, department=cs_dept),
        Program(name="Applied Mathematics", code="AM", level="SCIENCE", duration=3, department=math_dept),
        Program(name="Physics", code="PHY", level="SCIENCE", duration=3, department=physics_dept)
    ]
    db.session.add_all(programs)
    db.session.commit()

    # Create admin user
    admin = User(
        username="admin",
        email="admin@faculty.edu",
        type="admin"
    )
    admin.set_password("admin123")
    db.session.add(admin)

    # Create teachers
    teachers = [
        Teacher(
            username="john_doe",
            email="john.doe@faculty.edu",
            first_name="John",
            last_name="Doe",
            department=cs_dept,
            is_permanent=True
        ),
        Teacher(
            username="jane_smith",
            email="jane.smith@faculty.edu",
            first_name="Jane",
            last_name="Smith",
            department=math_dept,
            is_permanent=True
        ),
        Teacher(
            username="bob_wilson",
            email="bob.wilson@faculty.edu",
            first_name="Bob",
            last_name="Wilson",
            department=physics_dept,
            is_permanent=False
        )
    ]
    for teacher in teachers:
        teacher.set_password("password123")
    db.session.add_all(teachers)
    db.session.commit()

    # Create rooms
    rooms = [
        Room(
            name="A101",
            room_type="AMPHITHEATER",
            capacity=120,
            building="Building A",
            floor=1,
            has_projector=True
        ),
        Room(
            name="B201",
            room_type="TD_ROOM",
            capacity=40,
            building="Building B",
            floor=2,
            has_whiteboard=True
        ),
        Room(
            name="C301",
            room_type="TP_ROOM",
            capacity=25,
            building="Building C",
            floor=3,
            has_computers=True,
            has_projector=True
        )
    ]
    db.session.add_all(rooms)
    db.session.commit()

    # Create time slots
    time_slots = [
        TimeSlot(
            day_of_week=0,  # Monday
            start_time=time(8, 30),
            end_time=time(10, 0)
        ),
        TimeSlot(
            day_of_week=0,  # Monday
            start_time=time(10, 15),
            end_time=time(11, 45)
        ),
        TimeSlot(
            day_of_week=1,  # Tuesday
            start_time=time(8, 30),
            end_time=time(10, 0)
        ),
        TimeSlot(
            day_of_week=1,  # Tuesday
            start_time=time(10, 15),
            end_time=time(11, 45)
        )
    ]
    db.session.add_all(time_slots)
    db.session.commit()

    # Create courses
    courses = [
        Course(
            name="Introduction to Programming",
            code="CS101",
            course_type="LECTURE",
            credits=3,
            program=programs[0],
            teacher=teachers[0]
        ),
        Course(
            name="Calculus I",
            code="MATH101",
            course_type="TD",
            credits=4,
            program=programs[2],
            teacher=teachers[1]
        ),
        Course(
            name="Physics Lab",
            code="PHY101",
            course_type="TP",
            credits=2,
            program=programs[3],
            teacher=teachers[2]
        )
    ]
    db.session.add_all(courses)
    db.session.commit()

    # Create schedules
    schedules = [
        Schedule(
            course=courses[0],
            room=rooms[0],
            time_slot=time_slots[0],
            created_by=admin
        ),
        Schedule(
            course=courses[1],
            room=rooms[1],
            time_slot=time_slots[1],
            created_by=admin
        ),
        Schedule(
            course=courses[2],
            room=rooms[2],
            time_slot=time_slots[2],
            created_by=admin
        )
    ]
    db.session.add_all(schedules)
    db.session.commit()

    # Create students
    students = [
        Student(
            username="student1",
            email="student1@faculty.edu",
            first_name="Alice",
            last_name="Johnson",
            program=programs[0],
            enrollment_year=2023
        ),
        Student(
            username="student2",
            email="student2@faculty.edu",
            first_name="Bob",
            last_name="Brown",
            program=programs[1],
            enrollment_year=2023
        )
    ]
    for student in students:
        student.set_password("password123")
    db.session.add_all(students)
    db.session.commit()

if __name__ == '__main__':
    init_db()
