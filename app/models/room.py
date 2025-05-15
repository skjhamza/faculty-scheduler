from app import db
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    room_type = db.Column(db.String(20), nullable=False)  # 'AMPHITHEATER', 'TD_ROOM', 'TP_ROOM'
    capacity = db.Column(db.Integer, nullable=False)
    building = db.Column(db.String(50))
    floor = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Equipment and facilities
    has_projector = db.Column(db.Boolean, default=False)
    has_computers = db.Column(db.Boolean, default=False)
    has_whiteboard = db.Column(db.Boolean, default=True)
    
    # Relationships
    schedules = db.relationship('Schedule', backref='room', lazy='dynamic')
    
    def __repr__(self):
        return f'<Room {self.name} ({self.room_type})>'
    
    @property
    def is_available(self):
        """Check if room is currently available"""
        current_time = datetime.now().time()
        current_day = datetime.now().weekday()
        
        current_schedule = self.schedules.join(TimeSlot).filter(
            TimeSlot.day_of_week == current_day,
            TimeSlot.start_time <= current_time,
            TimeSlot.end_time >= current_time,
            Schedule.is_active == True
        ).first()
        
        return current_schedule is None
    
    def get_schedule(self, date=None):
        """Get room schedule for a specific date"""
        if date is None:
            date = datetime.now()
        
        return self.schedules.join(TimeSlot).filter(
            TimeSlot.day_of_week == date.weekday(),
            Schedule.is_active == True
        ).order_by(TimeSlot.start_time).all()
    
    def is_suitable_for_course(self, course):
        """Check if room is suitable for a specific course type"""
        if course.course_type == 'LECTURE' and self.room_type != 'AMPHITHEATER':
            return False
        elif course.course_type == 'TD' and self.room_type != 'TD_ROOM':
            return False
        elif course.course_type == 'TP' and self.room_type != 'TP_ROOM':
            return False
        
        # Check if room capacity is sufficient
        # Assuming we have access to the course's student count
        # student_count = course.program.students.count()
        # return self.capacity >= student_count
        return True
    
    @staticmethod
    def get_available_rooms(time_slot_id, course_type=None, min_capacity=0):
        """Get available rooms for a specific time slot"""
        query = Room.query.filter(Room.is_active == True)
        
        if course_type:
            if course_type == 'LECTURE':
                query = query.filter(Room.room_type == 'AMPHITHEATER')
            elif course_type == 'TD':
                query = query.filter(Room.room_type == 'TD_ROOM')
            elif course_type == 'TP':
                query = query.filter(Room.room_type == 'TP_ROOM')
        
        if min_capacity > 0:
            query = query.filter(Room.capacity >= min_capacity)
        
        # Exclude rooms that are already scheduled for this time slot
        busy_rooms = db.session.query(Schedule.room_id).filter(
            Schedule.time_slot_id == time_slot_id,
            Schedule.is_active == True
        )
        
        return query.filter(~Room.id.in_(busy_rooms)).all()
