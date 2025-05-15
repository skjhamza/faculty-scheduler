from flask import render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.routes import teacher_bp
from app.models import Course, Schedule, TimeSlot
from app.utils.decorators import teacher_required
from flask_login import login_required, current_user
from datetime import datetime, timedelta

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    # Get teacher's courses
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    
    # Get weekly teaching hours
    weekly_hours = current_user.calculate_weekly_hours()
    
    # Get today's schedule
    today = datetime.now()
    today_schedule = Schedule.get_teacher_schedule(
        teacher_id=current_user.id,
        start_date=today,
        end_date=today + timedelta(days=1)
    )
    
    return render_template('teacher/dashboard.html',
                         courses=courses,
                         weekly_hours=weekly_hours,
                         today_schedule=today_schedule)

@teacher_bp.route('/schedule')
@login_required
@teacher_required
def schedule():
    # Get date parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Get teacher's schedule
    schedules = Schedule.get_teacher_schedule(
        teacher_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    
    return render_template('teacher/schedule.html',
                         schedules=schedules,
                         start_date=start_date,
                         end_date=end_date)

@teacher_bp.route('/courses')
@login_required
@teacher_required
def courses():
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/courses.html', courses=courses)

@teacher_bp.route('/courses/<int:course_id>')
@login_required
@teacher_required
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Ensure the teacher has access to this course
    if course.teacher_id != current_user.id:
        flash('You do not have access to this course', 'error')
        return redirect(url_for('teacher.courses'))
    
    # Get course schedules
    schedules = Schedule.query.filter_by(course_id=course_id).all()
    
    return render_template('teacher/course_details.html',
                         course=course,
                         schedules=schedules)

@teacher_bp.route('/statistics')
@login_required
@teacher_required
def statistics():
    # Get teaching statistics
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    
    # Calculate hours by course type
    lecture_hours = sum(course.get_weekly_hours() for course in courses 
                       if course.course_type == 'LECTURE')
    td_hours = sum(course.get_weekly_hours() for course in courses 
                  if course.course_type == 'TD')
    tp_hours = sum(course.get_weekly_hours() for course in courses 
                  if course.course_type == 'TP')
    
    # Get total teaching hours
    total_hours = lecture_hours + td_hours + tp_hours
    
    return render_template('teacher/statistics.html',
                         courses=courses,
                         lecture_hours=lecture_hours,
                         td_hours=td_hours,
                         tp_hours=tp_hours,
                         total_hours=total_hours)

@teacher_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@teacher_required
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
                return redirect(url_for('teacher.profile'))
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return redirect(url_for('teacher.profile'))
            
            current_user.set_password(new_password)
        
        try:
            db.session.commit()
            flash('Profile updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile', 'error')
        
        return redirect(url_for('teacher.profile'))
    
    return render_template('teacher/profile.html')

# API Endpoints for AJAX requests
@teacher_bp.route('/api/schedule/next', methods=['GET'])
@login_required
@teacher_required
def get_next_schedule():
    """Get the next scheduled class"""
    now = datetime.now()
    next_schedule = Schedule.query.join(Course).filter(
        Course.teacher_id == current_user.id,
        Schedule.start_time > now
    ).order_by(Schedule.start_time).first()
    
    if next_schedule:
        return jsonify({
            'course': next_schedule.course.name,
            'room': next_schedule.room.name,
            'time': next_schedule.start_time.strftime('%H:%M'),
            'date': next_schedule.start_time.strftime('%Y-%m-%d')
        })
    
    return jsonify({'message': 'No upcoming classes'})
