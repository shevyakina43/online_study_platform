# # **Задачі**

# ## **Задача 1. Базові SELECT**

# 1. Вивести всіх студентів, які зареєструвалися після 2024‑01‑01.
SELECT *
FROM students
WHERE reg_date > '2024-01-01';
# 2. Вивести всі курси категорії `"Data Science"`.
SELECT *
FROM courses
WHERE category = 'Data Science';


# ## **Задача 2. Групування та агрегація**

# 1. Порахувати кількість студентів у кожному місті.
SELECT city, COUNT(*) AS student_count
FROM students
GROUP BY city;
# 2. Порахувати кількість курсів у кожній категорії.
SELECT category, COUNT(*) AS course_count
FROM courses
GROUP BY category;
# 3. Порахувати середню оцінку по кожному курсу.
SELECT 
    c.course_name,
    AVG(p.score) AS avg_score
FROM courses c
JOIN enrollments e ON c.course_id = e.course_id
JOIN progress p ON e.enrollment_id = p.enrollment_id
GROUP BY c.course_name;


# ## **Задача 3. JOIN‑аналіз**

# 1. Вивести список курсів разом з іменами викладачів.
SELECT 
    c.course_name,
    i.full_name AS instructor_name
FROM courses c
JOIN instructors i 
    ON c.instructor_id = i.instructor_id
ORDER BY c.course_name;
# 2. Вивести студентів та назви курсів, на які вони записані.
SELECT
    s.full_name AS student_name,
    c.course_name
FROM students s
JOIN enrollments e 
    ON s.student_id = e.student_id
JOIN courses c 
    ON e.course_id = c.course_id
ORDER BY s.full_name, c.course_name;
# 3. Порахувати, скільки студентів у кожного викладача.
SELECT
    i.full_name AS instructor_name,
    COUNT(DISTINCT e.student_id) AS students_count
FROM instructors i
JOIN courses c 
    ON i.instructor_id = c.instructor_id
JOIN enrollments e 
    ON c.course_id = e.course_id
GROUP BY i.full_name
ORDER BY students_count DESC;


# ## **Задача 4. Аналітика прогресу**

# 1. Порахувати середню оцінку кожного студента.
SELECT
    s.full_name,
    ROUND(AVG(p.score), 2) AS avg_score
FROM students s
JOIN enrollments e 
    ON s.student_id = e.student_id
JOIN progress p 
    ON e.enrollment_id = p.enrollment_id
GROUP BY s.full_name
ORDER BY avg_score DESC;
# 2. Порахувати відсоток завершених уроків для кожного курсу.
SELECT
    c.course_name,
    ROUND(
        100.0 * 
        SUM(CASE WHEN p.completed THEN 1 ELSE 0 END) 
        / COUNT(*)
    , 2) AS completed_percent
FROM courses c
JOIN enrollments e 
    ON c.course_id = e.course_id
JOIN progress p 
    ON e.enrollment_id = p.enrollment_id
GROUP BY c.course_name
ORDER BY completed_percent DESC;
# 3. Знайти студентів, які завершили всі уроки у своїх курсах.
SELECT
    s.full_name
FROM students s
JOIN enrollments e 
    ON s.student_id = e.student_id
JOIN progress p 
    ON e.enrollment_id = p.enrollment_id
GROUP BY s.student_id, s.full_name
HAVING 
    COUNT(*) = SUM(CASE WHEN p.completed THEN 1 ELSE 0 END);


# ## **Задача 5. Віконні функції**

# 1. Для кожного курсу визначити рейтинг студентів за середнім балом.
SELECT
    c.course_name,
    s.full_name,
    ROUND(AVG(p.score), 2) AS avg_score,
    RANK() OVER (
        PARTITION BY c.course_id
        ORDER BY AVG(p.score) DESC
    ) AS rank_in_course
FROM courses c
JOIN enrollments e 
    ON c.course_id = e.course_id
JOIN students s 
    ON e.student_id = s.student_id
JOIN progress p 
    ON e.enrollment_id = p.enrollment_id
GROUP BY 
    c.course_id, c.course_name, 
    s.student_id, s.full_name
ORDER BY c.course_name, rank_in_course;
# 2. Порахувати кумулятивну кількість уроків, завершених студентом у хронологічному порядку.
#     - *Покрокове виконання та пояснення*
        
#         Нам потрібно порахувати **кумулятивну кількість уроків**, які завершив кожен студент, у хронологічному порядку. Це означає, що для кожного запису прогресу ми рахуємо загальну кількість завершених уроків від початку до поточного моменту.
        
#         Нам треба таблиці:
        
#         - `students` - щоб отримати інформацію про студентів
#         - `enrollments` - щоб зв'язати студентів із курсами та отримати дату запису
#         - `progress` - щоб отримати інформацію про завершені уроки
        
#         ### **students**
        
#         | Поле | Тип | Опис |
#         | --- | --- | --- |
#         | student_id | SERIAL PK | Унікальний ID студента |
#         | full_name | TEXT | ПІБ |
#         | city | TEXT | Місто |
#         | reg_date | DATE | Дата реєстрації |
        
#         ### **enrollments**
        
#         | Поле | Тип | Опис |
#         | --- | --- | --- |
#         | enrollment_id | SERIAL PK | ID запису |
#         | student_id | INT FK | Студент |
#         | course_id | INT FK | Курс |
#         | enroll_date | DATE | Дата запису |
        
#         ### **progress**
        
#         | Поле | Тип | Опис |
#         | --- | --- | --- |
#         | progress_id | SERIAL PK | ID прогресу |
#         | enrollment_id | INT FK | Запис |
#         | lesson_number | INT | Номер уроку |
#         | score | NUMERIC | Оцінка |
#         | completed | BOOLEAN | Чи завершено |
        
#         Оскільки в таблиці `progress` немає поля з датою виконання уроку, ми використовуємо:
        
#         - `enroll_date` з таблиці `enrollments` як базову дату
#         - `lesson_number` як порядок виконання уроків всередині курсу
        
#         Припускаємо, що уроки виконуються послідовно: урок 1, потім урок 2, потім урок 3 тощо.
        
#         ### **Використання віконної функції**
        
#         **SQL-запит (з заняття)**
        
#         ```sql
#         SELECT
#             s.full_name,
#             e.enroll_date,
#             SUM(CASE WHEN p.completed THEN 1 ELSE 0 END)
#                 OVER (PARTITION BY s.student_id ORDER BY p.lesson_number) 
#                 AS cumulative_completed
#         FROM students s
#         JOIN enrollments e ON s.student_id = e.student_id
#         JOIN progress p ON e.enrollment_id = p.enrollment_id
#         ORDER BY s.student_id, e.enroll_date, p.lesson_number;
#         ```
        
#         Для підрахунку кумулятивної суми використовуємо віконну функцію `SUM() OVER()` з параметрами:
        
#         - `PARTITION BY student_id` - розділяємо дані по кожному студенту окремо
#         - `ORDER BY enroll_date, lesson_number` - сортуємо по даті запису на курс та номеру уроку
#         - `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - рахуємо від початку до поточного рядка
        
#         - **Інший, більш загальний, спосіб**
            
#             **SQL-запит**
            
#             ```sql
#             -- Створюємо базовий SELECT із JOIN'ами
#             SELECT 
#                 s.full_name,                     -- ПІБ студента
#                 e.enroll_date,
                
#                 -- Додаємо віконну функцію для кумулятивного підрахунку
#                 SUM(
#                     CASE 
#                         WHEN p.completed THEN 1          -- Якщо урок завершено, додаємо 1
#                         ELSE 0                           -- Якщо не завершено, додаємо 0
#                     END
#                 ) OVER (
#                     PARTITION BY s.student_id           -- Окремо для кожного студента
#                     ORDER BY e.enroll_date, p.lesson_number  -- У хронологічному порядку
#                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- Від початку до поточного рядка
#                 ) AS cumulative_lessons_completed        -- Назва стовпця результату
            
#             -- JOIN'имо всі необхідні таблиці
#             FROM students s
#             INNER JOIN enrollments e ON s.student_id = e.student_id
#             INNER JOIN progress p ON e.enrollment_id = p.enrollment_id
            
#             -- Сортуємо результат для зручності перегляду
#             ORDER BY s.student_id, e.enroll_date, p.lesson_number;
#             ```
            
#             > **ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW**
#             > 
            
#             > Визначає "рамку вікна": від самого першого рядка (UNBOUNDED PRECEDING) до поточного рядка (CURRENT ROW). Це і є кумулятивний підрахунок.
#             > 
        
#         **Приклад результату**
        
#         ![image.png](attachment:8fa6d172-1644-4af8-9687-f40340dc32f6:image.png)
        
#         Додамо групування
        
# 3. Для кожної категорії курсів знайти топ‑1 курс за кількістю студентів.
SELECT
    category,
    course_name,
    students_count
FROM (
    SELECT
        c.category,
        c.course_name,
        COUNT(DISTINCT e.student_id) AS students_count,
        RANK() OVER (
            PARTITION BY c.category
            ORDER BY COUNT(DISTINCT e.student_id) DESC
        ) AS rnk
    FROM courses c
    JOIN enrollments e 
        ON c.course_id = e.course_id
    GROUP BY 
        c.category,
        c.course_id,
        c.course_name
) t
WHERE rnk = 1
ORDER BY category;