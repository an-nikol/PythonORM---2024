import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Student


def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )

    student = Student()
    student.student_id = 'FE0054'
    student.first_name = 'Jane'
    student.last_name = 'Smith'
    student.email = 'jane.smith@university.com'
    student.save()

    student_other = Student(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )
    student_other.save()

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )


def get_students_info():
    all_students = []

    for student in Student.objects.all():
        all_students.append(f"Student №{student.student_id}: {student.first_name} "
                            f"{student.last_name}; Email: {student.email}")

    return '\n'.join(all_students)


def update_students_emails():
    for student_obj in Student.objects.all():
        student_obj.email = student_obj.email.replace(student_obj.email.split('@')[1], 'uni-students.com')
        student_obj.save()


def truncate_students():
    Student.objects.all().delete()


# Run and print your queries
