from flask import render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.routes import student_bp
from app.models import Program, Course, Schedule, TimeSlot
from app.utils.decorators import student_required
from flask_login import login_required, current_user
from datetime import datetime, timedelta

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    # Get student's program
    program = current_user.program
    
    # Get today's schedule
    today = datetime.now()
    today_schedule = Schedule.query.join(Course).filter(
        Course.program_id == current_user.program_id,
        Schedule.is_active == True
    ).all()
    
    # Get next class
    next_class = Schedule.query.join(Course).filter(
        Course.program_id == current_user.program_id,
        Schedule.is_active == True,
        TimeSlot.start_time > datetime.now().time()
    ).order_by(TimeSlot.start_time).first()
    
    return render_template('student/dashboard.html',
                         program=program,
                         today_schedule=today_schedule,
                         next_class=next_class)

@student_bp.route('/schedule')
@login_required
@student_required
def schedule():
    # Get date parameters
    week = request.args.get('week', 0, type=int)
    
    # Calculate date range
    today = datetime.now()
    start_of_week = today + timedelta(days=-today.weekday(), weeks=week)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get weekly schedule
    schedules = Schedule.query.join(Course).filter(
        Course.program_id == current_user.program_id,
        Schedule.is_active == True
    ).all()
    
    # Organize schedules by day and time slot
    weekly_schedule = {day: [] for day in range(7)}
    for schedule in schedules:
        weekly_schedule[schedule.time_slot.day_of_week].append(schedule)
    
    return render_template('student/schedule.html',
                         weekly_schedule=weekly_schedule,
                         start_date=start_of_week,
                         end_date=end_of_week,
                         week=week)

@student_bp.route('/courses')
@login_required
@student_required
def courses():
    # Get all courses for student's program
    courses = Course.query.filter_by(program_id=current_user.program_id).all()
    
    return render_template('student/courses.html',
                         courses=courses)

@student_bp.route('/courses/<int:course_id>')
@login_required
@student_required
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Ensure the student has access to this course
    if course.program_id != current_user.program_id:
        flash('You do not have access to this course', 'error')
        return redirect(url_for('student.courses'))
    
    # Get course schedules
    schedules = Schedule.query.filter_by(
        course_id=course_id,
        is_active=True
    ).all()
    
    return render_template('student/course_details.html',
                         course=course,
                         schedules=schedules)

@student_bp.route('/program')
@login_required
@student_required
def program():
    program = current_user.program
    department = program.department
    
    # Get all courses for the program
    courses = Course.query.filter_by(program_id=program.id).all()
    
    return render_template('student/program.html',
                         program=program,
                         department=department,
                         courses=courses)

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    if request.method == 'POST':
        # Update profile information
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        
        # Handle password change if requested
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if current_password and new_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'error')
                return redirect(url_for('student.profile'))
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return redirect(url_for('student.profile'))
            
            current_user.set_password(new_password)
        
        try:
            db.session.commit()
            flash('Profile updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile', 'error')
        
        return redirect(url_for('student.profile'))
    
    return render_template('student/profile.html')

# API Endpoints for AJAX requests
@student_bp.route('/api/schedule/next', methods=['GET'])
@login_required
@student_required
def get_next_schedule():
    """Get the next scheduled class"""
    now = datetime.now()
    next_schedule = Schedule.query.join(Course).filter(
        Course.program_id == current_user.program_id,
        Schedule.is_active == True,
        TimeSlot.start_time > now.time(),
        TimeSlot.day_of_week >= now.weekday()
    ).order_by(
        TimeSlot.day_of_week,
        TimeSlot.start_time
    ).first()
    
    if next_schedule:
        return jsonify({
            'course': next_schedule.course.name,
            'room': next_schedule.room.name,
            'time': next_schedule.time_slot.start_time.strftime('%H:%M'),
            'day': next_schedule.time_slot.day_of_week
        })
    
    return jsonify({'message': 'No upcoming classes'})

@student_bp.route('/api/schedule/today', methods=['GET'])
@login_required
@student_required
def get_today_schedule():
    """Get today's schedule"""
    now = datetime.now()
    schedules = Schedule.query.join(Course).filter(
        Course.program_id == current_user.program_id,
        Schedule.is_active == True,
        TimeSlot.day_of_week == now.weekday()
    ).order_by(TimeSlot.start_time).all()
    
    schedule_list = [{
        'course': schedule.course.name,
        'room': schedule.room.name,
        'start_time': schedule.time_slot.start_time.strftime('%H:%M'),
        'end_time': schedule.time_slot.end_time.strftime('%H:%M')
    } for schedule in schedules]
    
    return jsonify(schedule_list)
