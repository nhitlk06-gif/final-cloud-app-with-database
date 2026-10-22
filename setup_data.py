import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment
from datetime import date

# 1. Create Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created.")
else:
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("Superuser 'admin' updated.")

# 2. Create Student User
if not User.objects.filter(username='student').exists():
    student = User.objects.create_user('student', 'alex@example.com', 'student123', first_name='Alex', last_name='Johnson')
    print("Student user 'student' created.")
else:
    student = User.objects.get(username='student')
    student.first_name = 'Alex'
    student.last_name = 'Johnson'
    student.set_password('student123')
    student.save()
    print("Student user 'student' updated.")

# 3. Create Instructor
inst_user, _ = User.objects.get_or_create(username='prof_smith', defaults={'first_name': 'John', 'last_name': 'Smith'})
instructor, _ = Instructor.objects.get_or_create(user=inst_user, defaults={'full_time': True, 'total_learners': 120})

# 4. Create Course
course, created = Course.objects.get_or_create(
    name='Cloud Application Development',
    defaults={
        'description': 'Master modern web app development using Python, Django, SQL databases, and Cloud technologies.',
        'pub_date': date(2026, 1, 15),
        'total_enrollment': 1
    }
)
course.instructors.add(instructor)

# 5. Create Lessons
lesson1, _ = Lesson.objects.get_or_create(
    course=course,
    order=0,
    defaults={
        'title': 'Introduction to Cloud Architecture',
        'content': 'Learn fundamental concepts of cloud computing, containers, and web deployment strategies.'
    }
)

lesson2, _ = Lesson.objects.get_or_create(
    course=course,
    order=1,
    defaults={
        'title': 'Django Framework and Database Design',
        'content': 'Explore Django ORM, Models, Views, Templates, and SQL database management.'
    }
)

# 6. Create Questions and Choices
# Clear existing questions for clean setup
Question.objects.filter(course=course).delete()

# Q1
q1 = Question.objects.create(
    course=course,
    lesson=lesson1,
    question_text='Which pattern does the Django framework follow?',
    grade=50
)
Choice.objects.create(question=q1, choice_text='Model-View-Template (MVT)', is_correct=True)
Choice.objects.create(question=q1, choice_text='Model-View-Presenter (MVP)', is_correct=False)
Choice.objects.create(question=q1, choice_text='Single Page Application (SPA)', is_correct=False)

# Q2
q2 = Question.objects.create(
    course=course,
    lesson=lesson2,
    question_text='Which command is used to apply database schema changes in Django?',
    grade=50
)
Choice.objects.create(question=q2, choice_text='python manage.py migrate', is_correct=True)
Choice.objects.create(question=q2, choice_text='python manage.py runserver', is_correct=False)
Choice.objects.create(question=q2, choice_text='python manage.py check', is_correct=False)

# 7. Create Enrollment
enrollment, _ = Enrollment.objects.get_or_create(
    user=student,
    course=course,
    defaults={'mode': 'honor'}
)

print(f"Data setup completed successfully. Course: {course.name}, Questions: {Question.objects.count()}, Choices: {Choice.objects.count()}")
