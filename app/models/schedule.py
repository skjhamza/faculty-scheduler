from app import db
from datetime import datetime, time

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0-6 (Monday-Sunday)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    def __repr__(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f'<TimeSlot {days[self.day_of_week]} {self.start_time}-{self.end_time}>'
    
    @staticmethod
    def create_default_slots():
        """Create default time slots for the week"""
        default_slots = [
            (time(8, 30), time(10, 0)),
            (time(10, 15), time(11, 45)),
            (time(13, 0), time(14, 30)),
            (time(14, 45), time(16, 15)),
            (time(16, 30), time(18, 0))
        ]
        
        for day in range(6):  # Monday to Saturday
            for start, end in default_slots:
                slot = TimeSlot(day_of_week=day, start_time=start, end_time=end)
                db.session.add(slot)
        db.session.commit()

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    course_type = db.Column(db.String(20))  # 'LECTURE', 'TD', 'TP'
    semester = db.Column(db.Integer)
    
    # Foreign Keys
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    
    # Relationships
    schedules = db.relationship('Schedule', backref='course', lazy='dynamic')
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'
    
    def get_weekly_hours(self):
        """Calculate total weekly hours for this course"""
        return self.schedules.count() * 1.5  # Assuming each session is 1.5 hours

class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields for tracking changes
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Schedule {self.course.code} - {self.time_slot}>'
    
    def check_conflicts(self):
        """Check for scheduling conflicts"""
        conflicts = Schedule.query.filter(
            Schedule.time_slot_id == self.time_slot_id,
            Schedule.id != self.id,
            Schedule.is_active == True
        ).filter(
            (Schedule.room_id == self.room_id) |  # Same room
            (Schedule.course.has(program_id=self.course.program_id))  # Same program
        ).all()
        return conflicts
    
    @staticmethod
    def get_teacher_schedule(teacher_id, start_date=None, end_date=None):
        """Get schedule for a specific teacher"""
        query = Schedule.query.join(Course).filter(
            Course.teacher_id == teacher_id,
            Schedule.is_active == True
        )
        if start_date:
            query = query.filter(Schedule.created_at >= start_date)
        if end_date:
            query = query.filter(Schedule.created_at <= end_date)
        return query.all()
    
    @staticmethod
    def get_room_schedule(room_id, date=None):
        """Get schedule for a specific room"""
        query = Schedule.query.filter(
            Schedule.room_id == room_id,
            Schedule.is_active == True
        )
        if date:
            query = query.join(TimeSlot).filter(TimeSlot.day_of_week == date.weekday())
        return query.all()
