-- Reset tables
DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS time_slots;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS programs;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS users;

-- Create tables
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE programs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    level VARCHAR(20) NOT NULL,
    duration INTEGER NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teachers (
    id INTEGER PRIMARY KEY REFERENCES users(id),
    department_id INTEGER REFERENCES departments(id),
    is_permanent BOOLEAN DEFAULT false,
    weekly_hours INTEGER DEFAULT 0
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY REFERENCES users(id),
    program_id INTEGER REFERENCES programs(id),
    student_id VARCHAR(20) UNIQUE,
    enrollment_year INTEGER
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    room_type VARCHAR(20) NOT NULL,
    capacity INTEGER NOT NULL,
    building VARCHAR(50) NOT NULL,
    floor INTEGER NOT NULL,
    has_projector BOOLEAN DEFAULT false,
    has_computers BOOLEAN DEFAULT false,
    has_whiteboard BOOLEAN DEFAULT true,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    course_type VARCHAR(20) NOT NULL,
    credits INTEGER NOT NULL,
    program_id INTEGER REFERENCES programs(id),
    teacher_id INTEGER REFERENCES teachers(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE time_slots (
    id SERIAL PRIMARY KEY,
    day_of_week INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    room_id INTEGER REFERENCES rooms(id),
    time_slot_id INTEGER REFERENCES time_slots(id),
    created_by_id INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Departments
INSERT INTO departments (name, code) VALUES
('Computer Science', 'CS'),
('Mathematics', 'MATH'),
('Physics', 'PHY'),
('Electrical Engineering', 'EE'),
('Mechanical Engineering', 'ME'),
('Civil Engineering', 'CE'),
('Chemistry', 'CHEM'),
('Biology', 'BIO');

-- Insert Programs
INSERT INTO programs (name, code, level, duration, department_id) VALUES
('Computer Science Engineering', 'CSE', 'ENGINEERING', 3, 1),
('Software Engineering', 'SE', 'ENGINEERING', 3, 1),
('Data Science', 'DS', 'ENGINEERING', 2, 1),
('Applied Mathematics', 'AM', 'SCIENCE', 3, 2),
('Pure Mathematics', 'PM', 'SCIENCE', 3, 2),
('Physics', 'PHY', 'SCIENCE', 3, 3),
('Electronics', 'EE', 'ENGINEERING', 3, 4),
('Mechanical Design', 'MD', 'ENGINEERING', 3, 5),
('Structural Engineering', 'SE', 'ENGINEERING', 3, 6),
('Chemical Engineering', 'CE', 'ENGINEERING', 3, 7),
('Biotechnology', 'BT', 'SCIENCE', 3, 8);

-- Insert Admin User
INSERT INTO users (username, email, password_hash, type, first_name, last_name)
VALUES ('admin', 'admin@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'admin', 'Admin', 'User');

-- Insert Teachers
INSERT INTO users (username, email, password_hash, type, first_name, last_name) VALUES
('john_doe', 'john.doe@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'John', 'Doe'),
('jane_smith', 'jane.smith@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'Jane', 'Smith'),
('bob_wilson', 'bob.wilson@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'Bob', 'Wilson'),
('alice_johnson', 'alice.johnson@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'Alice', 'Johnson'),
('david_brown', 'david.brown@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'David', 'Brown'),
('sarah_davis', 'sarah.davis@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'Sarah', 'Davis'),
('michael_miller', 'michael.miller@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'Michael', 'Miller'),
('emma_wilson', 'emma.wilson@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'Emma', 'Wilson'),
('james_taylor', 'james.taylor@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'James', 'Taylor'),
('laura_anderson', 'laura.anderson@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'teacher', 'Laura', 'Anderson');

-- Insert Teachers Details
INSERT INTO teachers (id, department_id, is_permanent, weekly_hours) VALUES
(2, 1, true, 18),  -- John Doe - CS
(3, 2, true, 16),  -- Jane Smith - Math
(4, 3, false, 12), -- Bob Wilson - Physics
(5, 4, true, 18),  -- Alice Johnson - EE
(6, 5, true, 16),  -- David Brown - ME
(7, 6, true, 18),  -- Sarah Davis - CE
(8, 7, false, 12), -- Michael Miller - Chemistry
(9, 8, true, 16),  -- Emma Wilson - Biology
(10, 1, true, 18), -- James Taylor - CS
(11, 2, false, 12); -- Laura Anderson - Math

-- Insert Students
INSERT INTO users (username, email, password_hash, type, first_name, last_name) VALUES
('student1', 'student1@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'student', 'Alex', 'Johnson'),
('student2', 'student2@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'student', 'Emily', 'Brown'),
('student3', 'student3@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'student', 'Daniel', 'Wilson'),
('student4', 'student4@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'student', 'Sophia', 'Davis'),
('student5', 'student5@faculty.edu', 'pbkdf2:sha256:260000$YOUR_HASH', 'student', 'Oliver', 'Miller');

-- Insert Students Details
INSERT INTO students (id, program_id, student_id, enrollment_year) VALUES
(12, 1, 'CSE2023001', 2023),
(13, 2, 'SE2023001', 2023),
(14, 3, 'DS2023001', 2023),
(15, 4, 'AM2023001', 2023),
(16, 5, 'PM2023001', 2023);

-- Insert Rooms
INSERT INTO rooms (name, room_type, capacity, building, floor, has_projector, has_computers, has_whiteboard) VALUES
('A101', 'AMPHITHEATER', 120, 'Building A', 1, true, false, true),
('A102', 'AMPHITHEATER', 100, 'Building A', 1, true, false, true),
('B201', 'TD_ROOM', 40, 'Building B', 2, true, false, true),
('B202', 'TD_ROOM', 35, 'Building B', 2, true, false, true),
('C301', 'TP_ROOM', 25, 'Building C', 3, true, true, true),
('C302', 'TP_ROOM', 25, 'Building C', 3, true, true, true),
('D101', 'AMPHITHEATER', 150, 'Building D', 1, true, false, true),
('D201', 'TD_ROOM', 45, 'Building D', 2, true, false, true),
('E301', 'TP_ROOM', 30, 'Building E', 3, true, true, true),
('E302', 'TP_ROOM', 30, 'Building E', 3, true, true, true);

-- Insert Courses
INSERT INTO courses (name, code, course_type, credits, program_id, teacher_id) VALUES
('Introduction to Programming', 'CS101', 'LECTURE', 3, 1, 2),
('Data Structures', 'CS201', 'TD', 3, 1, 2),
('Algorithms', 'CS202', 'TP', 3, 1, 10),
('Calculus I', 'MATH101', 'LECTURE', 4, 4, 3),
('Linear Algebra', 'MATH201', 'TD', 3, 4, 11),
('Physics Mechanics', 'PHY101', 'LECTURE', 3, 6, 4),
('Electronics Basics', 'EE101', 'LECTURE', 3, 7, 5),
('Machine Design', 'ME101', 'TD', 3, 8, 6),
('Structural Analysis', 'CE101', 'LECTURE', 3, 9, 7),
('Organic Chemistry', 'CHEM101', 'TP', 3, 10, 8);

-- Insert Time Slots
INSERT INTO time_slots (day_of_week, start_time, end_time) VALUES
(0, '08:30', '10:00'), -- Monday
(0, '10:15', '11:45'),
(0, '13:30', '15:00'),
(0, '15:15', '16:45'),
(1, '08:30', '10:00'), -- Tuesday
(1, '10:15', '11:45'),
(1, '13:30', '15:00'),
(1, '15:15', '16:45'),
(2, '08:30', '10:00'), -- Wednesday
(2, '10:15', '11:45'),
(2, '13:30', '15:00'),
(2, '15:15', '16:45'),
(3, '08:30', '10:00'), -- Thursday
(3, '10:15', '11:45'),
(3, '13:30', '15:00'),
(3, '15:15', '16:45'),
(4, '08:30', '10:00'), -- Friday
(4, '10:15', '11:45'),
(4, '13:30', '15:00'),
(4, '15:15', '16:45');

-- Insert Schedules
INSERT INTO schedules (course_id, room_id, time_slot_id, created_by_id, is_active) VALUES
(1, 1, 1, 1, true),   -- CS101 - Monday 8:30
(2, 3, 2, 1, true),   -- CS201 - Monday 10:15
(3, 5, 3, 1, true),   -- CS202 - Monday 13:30
(4, 2, 5, 1, true),   -- MATH101 - Tuesday 8:30
(5, 4, 6, 1, true),   -- MATH201 - Tuesday 10:15
(6, 1, 9, 1, true),   -- PHY101 - Wednesday 8:30
(7, 7, 13, 1, true),  -- EE101 - Thursday 8:30
(8, 8, 14, 1, true),  -- ME101 - Thursday 10:15
(9, 7, 17, 1, true),  -- CE101 - Friday 8:30
(10, 9, 18, 1, true); -- CHEM101 - Friday 10:15
