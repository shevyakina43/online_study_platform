CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    full_name TEXT,
    city TEXT,
    reg_date DATE
);
INSERT INTO students (full_name, city, reg_date) VALUES
('Anna Kovalenko', 'Kyiv', '2024-01-12'),
('Dmytro Shevchenko', 'Lviv', '2024-02-05'),
('Olena Bondar', 'Kharkiv', '2024-03-18'),
('Serhii Melnyk', 'Odesa', '2024-01-25'),
('Iryna Tkachenko', 'Dnipro', '2024-04-02'),
('Maksym Horbunov', 'Kyiv', '2024-02-20'),
('Kateryna Polishchuk', 'Lviv', '2024-03-01'),
('Yurii Kravets', 'Kharkiv', '2024-03-22'),
('Sofiia Levchenko', 'Odesa', '2024-04-10'),
('Vladyslav Chernenko', 'Kyiv', '2024-01-30');


CREATE TABLE instructors (
    instructor_id SERIAL PRIMARY KEY,
    full_name TEXT,
    specialization TEXT
);
INSERT INTO instructors (full_name, specialization) VALUES
('Oleh Marchenko', 'Data Science'),
('Tetiana Ivanova', 'Web Development'),
('Roman Sydorenko', 'Machine Learning'),
('Natalia Hlushko', 'UI/UX Design'),
('Andrii Petrenko', 'Databases');


CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name TEXT,
    category TEXT,
    instructor_id INT REFERENCES instructors(instructor_id)
);
INSERT INTO courses (course_name, category, instructor_id) VALUES
('Python for Beginners', 'Programming', 1),
('Data Analysis with SQL', 'Data Science', 5),
('Machine Learning Basics', 'Machine Learning', 3),
('Frontend Development with React', 'Web Development', 2),
('UI/UX Fundamentals', 'Design', 4),
('Advanced SQL Analytics', 'Data Science', 5),
('Deep Learning Intro', 'Machine Learning', 3),
('JavaScript Essentials', 'Programming', 2);


CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    enroll_date DATE
);
INSERT INTO enrollments (student_id, course_id, enroll_date) VALUES
(1, 1, '2024-02-01'),
(1, 2, '2024-02-10'),
(2, 2, '2024-02-15'),
(2, 4, '2024-03-01'),
(3, 3, '2024-03-20'),
(3, 6, '2024-03-25'),
(4, 1, '2024-02-05'),
(4, 5, '2024-04-01'),
(5, 2, '2024-04-05'),
(5, 7, '2024-04-12'),
(6, 4, '2024-03-10'),
(7, 5, '2024-03-15'),
(8, 6, '2024-04-02'),
(9, 3, '2024-04-15'),
(10, 1, '2024-02-20');


CREATE TABLE progress (
    progress_id SERIAL PRIMARY KEY,
    enrollment_id INT REFERENCES enrollments(enrollment_id),
    lesson_number INT,
    score NUMERIC,
    completed BOOLEAN
);
INSERT INTO progress (enrollment_id, lesson_number, score, completed) VALUES
(1, 1, 85, TRUE), (1, 2, 90, TRUE), (1, 3, 88, TRUE),
(2, 1, 92, TRUE), (2, 2, 87, TRUE), (2, 3, 95, TRUE),
(3, 1, 78, TRUE), (3, 2, 82, TRUE), (3, 3, 80, FALSE),
(4, 1, 88, TRUE), (4, 2, 90, TRUE),
(5, 1, 91, TRUE), (5, 2, 89, TRUE), (5, 3, 93, TRUE),
(6, 1, 85, TRUE), (6, 2, 87, TRUE),
(7, 1, 70, TRUE), (7, 2, 75, FALSE),
(8, 1, 95, TRUE), (8, 2, 97, TRUE),
(9, 1, 88, TRUE), (9, 2, 92, TRUE), (9, 3, 90, TRUE),
(10, 1, 84, TRUE), (10, 2, 86, TRUE),
(11, 1, 80, TRUE), (11, 2, 82, TRUE),
(12, 1, 98, TRUE), (12, 2, 96, TRUE),
(13, 1, 75, TRUE), (13, 2, 78, TRUE),
(14, 1, 89, TRUE), (14, 2, 91, TRUE), (14, 3, 94, TRUE),
(15, 1, 82, TRUE), (15, 2, 85, TRUE), (15, 3, 88, TRUE);
