from flask import render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.routes import admin_bp
from app.models import Department, Program, User, Teacher, Student, Room, Course, Schedule
from app.utils.decorators import admin_required
from flask_login import login_required, current_user

# Dashboard
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    departments_count = Department.query.count()
    teachers_count = Teacher.query.count()
    students_count = Student.query.count()
    rooms_count = Room.query.count()
    
    return render_template('admin/dashboard.html',
                         departments_count=departments_count,
                         teachers_count=teachers_count,
                         students_count=students_count,
                         rooms_count=rooms_count)

# Department Management
@admin_bp.route('/departments')
@login_required
@admin_required
def departments():
    departments = Department.query.all()
    return render_template('admin/departments/index.html', departments=departments)

@admin_bp.route('/departments/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_department():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        
        if Department.query.filter_by(code=code).first():
            flash('Department code already exists', 'error')
            return redirect(url_for('admin.create_department'))
        
        department = Department(name=name, code=code)
        db.session.add(department)
        
        try:
            db.session.commit()
            flash('Department created successfully', 'success')
            return redirect(url_for('admin.departments'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating department', 'error')
    
    return render_template('admin/departments/create.html')

# Program Management
@admin_bp.route('/programs')
@login_required
@admin_required
def programs():
    programs = Program.query.all()
    return render_template('admin/programs/index.html', programs=programs)

@admin_bp.route('/programs/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_program():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        level = request.form.get('level')
        duration = request.form.get('duration')
        department_id = request.form.get('department_id')
        
        program = Program(
            name=name,
            code=code,
            level=level,
            duration=duration,
            department_id=department_id
        )
        db.session.add(program)
        
        try:
            db.session.commit()
            flash('Program created successfully', 'success')
            return redirect(url_for('admin.programs'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating program', 'error')
    
    departments = Department.query.all()
    return render_template('admin/programs/create.html', departments=departments)

# Room Management
@admin_bp.route('/rooms')
@login_required
@admin_required
def rooms():
    rooms = Room.query.all()
    return render_template('admin/rooms/index.html', rooms=rooms)

@admin_bp.route('/rooms/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_room():
    if request.method == 'POST':
        name = request.form.get('name')
        room_type = request.form.get('room_type')
        capacity = request.form.get('capacity')
        building = request.form.get('building')
        floor = request.form.get('floor')
        has_projector = 'has_projector' in request.form
        has_computers = 'has_computers' in request.form
        
        room = Room(
            name=name,
            room_type=room_type,
            capacity=capacity,
            building=building,
            floor=floor,
            has_projector=has_projector,
            has_computers=has_computers
        )
        db.session.add(room)
        
        try:
            db.session.commit()
            flash('Room created successfully', 'success')
            return redirect(url_for('admin.rooms'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating room', 'error')
    
    return render_template('admin/rooms/create.html')

# Schedule Management
@admin_bp.route('/schedules')
@login_required
@admin_required
def schedules():
    schedules = Schedule.query.all()
    return render_template('admin/schedules/index.html', schedules=schedules)

@admin_bp.route('/schedules/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_schedule():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        room_id = request.form.get('room_id')
        time_slot_id = request.form.get('time_slot_id')
        
        schedule = Schedule(
            course_id=course_id,
            room_id=room_id,
            time_slot_id=time_slot_id,
            created_by_id=current_user.id
        )
        
        # Check for conflicts
        conflicts = schedule.check_conflicts()
        if conflicts:
            flash('Schedule conflicts detected', 'error')
            return redirect(url_for('admin.create_schedule'))
        
        db.session.add(schedule)
        
        try:
            db.session.commit()
            flash('Schedule created successfully', 'success')
            return redirect(url_for('admin.schedules'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating schedule', 'error')
    
    courses = Course.query.all()
    rooms = Room.query.all()
    time_slots = TimeSlot.query.all()
    return render_template('admin/schedules/create.html',
                         courses=courses,
                         rooms=rooms,
                         time_slots=time_slots)

# API Endpoints for AJAX requests
@admin_bp.route('/api/check-schedule-conflicts', methods=['POST'])
@login_required
@admin_required
def check_schedule_conflicts():
    data = request.get_json()
    schedule = Schedule(
        course_id=data['course_id'],
        room_id=data['room_id'],
        time_slot_id=data['time_slot_id']
    )
    conflicts = schedule.check_conflicts()
    return jsonify({'conflicts': bool(conflicts)})
