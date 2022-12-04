#!/bin/python3
from re import search
#import from modules
from student import create_student,update_student,remove_student,report
from course import create_course,course_performance,course_statistics
from batch import create_batch,students,courses,batch_performance,batch_statistics
from department import create_department,batches,batch_averages,department_statistics
from examination import Examination
def input_marks():
    while True:
        roll_number=input('\n\t\t\tClass Roll Number: ')
        if roll_number=='':
            break
        yield {
            'roll number':roll_number,
            'name':input('\t\t\tStudent Name: '),
            'marks':float(input('\t\t\tMarks: '))
        }
def input_array(data,id):
    print(f'\t\t\tEnter the {data} for {id}')
    while True:
        data=input('\t\t\t\t: ')
        if data=='':break
        yield data
while True:
    choice=input('''
1. Student
2. Course
3. Batch
4. Department
5. Examination

: ''')
    if choice=='':break
    elif choice=='1':
        choice=input('''
    1. Create a new student
    2. Update details of a student
    3. Remove a student
    4. Generate report of a student

    : ''')
        if choice=='1':
            create_student(
                student_id=input('\t\tStudent ID: '),
                name=input('\t\tStudent Name: '),
                class_roll_no=input('\t\tClass Roll No: '),
                batch=input('\t\tBatch ID: ')
            )
        elif choice=='2':
            update_student(
                student_id=input('\t\tStudent ID: '),
                name=input('\t\tStudent Name: '),
                class_roll_no=input('\t\tClass Roll No: '),
            )
        elif choice=='3':
            remove_student(
                student_id=input('\t\tStudent ID: ')
            )
        elif choice=='4':
            report(
                student_id=input('\t\tStudent ID: ')
            )
    elif choice=='2':
        choice=input('''
    1. Create a new course
    2. View performance of all students
    3. Create course statistics

    : ''')
        if choice=='1':
            create_course(
                course_id=input('\t\tCourse ID: '),
                course_name=input('\t\tCourse Name: '),
                marks=[student for student in input_marks()]
            )
        elif choice=='2':
            course=input('\t\tCourse: ')
            if search('^C0[0-9]{2}$',course):
                for i in course_performance(course_id=course):
                    print('\t\t\t',i)
            else:
                for i in course_performance(course_name=course):
                    print('\t\t\t',i)
        elif choice=='3':
            course=input('\t\tCourse: ')
            if search('^C0[0-9]{2}$',course):
                course_statistics(course_id=course)
            else:
                course_statistics(course_name=course)
    elif choice=='3':
        choice=input('''
    1. Create a new batch
    2. View list of students in a batch
    3. View list of courses taught in a batch
    4. View performance of a batch
    5. Create pie chart of percentage of all students

    : ''')
        batch_id=input('\t\tBatch ID: ')
        if choice=='1':
            create_batch(
                batch_id=batch_id,
                batch_name=input('\t\tBatch Name: '),
                department_name=input('\t\tDepartment Name: '),
                courses=[i for i in input_array('courses',batch_id)],
                students=[i for i in input_array('students',batch_id)]
            )
        elif choice=='2':
            print('\t\t',students(batch_id=batch_id))
        elif choice=='3':
            print('\t\t\t',courses(batch_id=batch_id))
        elif choice=='4':
            for i in batch_performance(batch_id=batch_id):print('\t\t\t',i)
        elif choice=='5':
            batch_statistics(batch_id=batch_id)
    elif choice=='4':
        choice=input('''
    1. Create a new department
    2. View batches of a department
    3. View average performance of batches of a department
    4. Create statistics of a department

    :''')
        department_id=input('\t\tDepartment ID: ')
        if choice=='1':
            create_department(
                department_id=department_id,
                department_name=input('\t\tDepartment Name: '),
                batches=[i for i in input_array('batches',department_id)]
            )
        elif choice=='2':
            print('\t\t\t',batches(department_id=department_id))
        elif choice=='3':
            for i in batch_averages(department_id=department_id):
                print(i)
        elif choice=='4':
            department_statistics(department_id=department_id)
    elif choice=='5':
        print('''
    Hold an examination:
''')
        exam=Examination(*[i for i in input_array('batches','exam')])
        choice=input('''
    1. View student perfomance in the examination
    2. Create examination statistics

    : ''')
        if choice=='1':
            print(exam.student_performance)
        elif choice=='2':
            exam.statistics()
