#!/bin/python3
from tkinter import Tk,Frame,Button,Label,Entry,StringVar,DoubleVar,END
from tkinter.scrolledtext import ScrolledText
from PIL.Image import open as image_open
from PIL.ImageTk import PhotoImage
from texttable import Texttable
from matplotlib.pyplot import show
from re import compile
from functools import partial
#import modules
from student import create_student,update_student,remove_student,report
from course import create_course,course_performance,course_statistics
from batch import create_batch,students,courses,batch_performance,batch_statistics
from department import create_department,batches,batch_averages,department_statistics
from examination import Examination
#---
interface=Tk()
interface.resizable(False,False)
interface.title('Menu')
home_image=PhotoImage(image_open('images/home.png').resize((15,15)))
plus_image=PhotoImage(image_open('images/plus.ico').resize((15,15)))
minus_image=PhotoImage(image_open('images/minus.ico').resize((15,15)))
#button functions
def retrieve(var):
    val=var.get()
    if val=='':raise Error('Empty Entry')
    var.set('')
    return val
def add_marks():
    global course_row
    course_marks_input.append((
        roll_no:=StringVar(),
        student:=StringVar(),
        marks:=DoubleVar()
    ))
    marks_entries.extend((
        roll_entry:=Entry(course_creation,textvariable=roll_no),
        name_entry:=Entry(course_creation,textvariable=student),
        marks_entry:=Entry(course_creation,textvariable=marks)
    ))
    roll_entry.grid(column=0,row=course_row)
    name_entry.grid(column=1,row=course_row)
    marks_entry.grid(column=2,row=course_row)
    course_row+=1
    marks_add.grid_forget();marks_add.grid(column=1,row=course_row,sticky='e')
    marks_remove.grid_forget();marks_remove.grid(column=2,row=course_row,sticky='w')
    course_create.grid_forget();course_create.grid(columnspan=3,row=course_row+1,sticky='nsew')
def add_courses():
    global students_row,courses_row
    batch_courses_input.append(course_id:=StringVar())
    course_entries.append(course_entry:=Entry(batch_creation,textvariable=course_id))
    course_entry.grid(column=0,row=courses_row)
    courses_row+=1;students_row+=1
    courses_add.grid_forget();courses_add.grid(column=0,row=courses_row,sticky='e')
    courses_remove.grid_forget();courses_remove.grid(column=1,row=courses_row,sticky='w')
    students_heading.grid_forget();students_heading.grid(columnspan=2,row=courses_row+1,sticky='nsew')
    for i,student_entry in enumerate(student_entries,courses_row+2):
        student_entry.grid_forget()
        student_entry.grid(column=0,row=i)
    students_add.grid_forget();students_add.grid(column=0,row=students_row,sticky='e')
    students_remove.grid_forget();students_remove.grid(column=1,row=students_row,sticky='w')
    batch_create.grid_forget();batch_create.grid(columnspan=2,row=students_row+1,sticky='nsew')
def add_students():
    global students_row
    batch_students_input.append(student_id:=StringVar())
    student_entries.append(student_entry:=Entry(batch_creation,textvariable=student_id))
    student_entry.grid(column=0,row=students_row)
    students_row+=1
    students_add.grid_forget();students_add.grid(column=0,row=students_row,sticky='e')
    students_remove.grid_forget();students_remove.grid(column=1,row=students_row,sticky='w')
    batch_create.grid_forget();batch_create.grid(columnspan=2,row=students_row+1,sticky='nsew')
def add_batches():
    global batches_row
    department_batch_input.append(batch_id:=StringVar())
    batch_entries.append(batch_entry:=Entry(department_creation,textvariable=batch_id))
    batch_entry.grid(columnspan=2,row=batches_row)
    batches_row+=1
    batch_add.grid_forget();batch_add.grid(column=0,row=batches_row,sticky='e')
    batch_remove.grid_forget();batch_remove.grid(column=1,row=batches_row,sticky='w')
    department_create.grid_forget();department_create.grid(columnspan=2,row=batches_row+1,sticky='nsew')
def add_batches_for_exam():
    global exam_batch_row
    exam_batch_input.append(batch_id:=StringVar())
    exam_batch_entries.append(batch_entry:=Entry(hold_exam,textvariable=batch_id))
    batch_entry.grid(columnspan=2,row=exam_batch_row)
    exam_batch_row+=1
    exam_batches_add.grid_forget();exam_batches_add.grid(column=0,row=exam_batch_row,sticky='e')
    exam_batches_remove.grid_forget();exam_batches_remove.grid(column=1,row=exam_batch_row,sticky='w')
    start_exam.grid_forget();start_exam.grid(columnspan=2,row=exam_batch_row+1,sticky='nsew')
course_id_pattern=compile('^C0[0-9]{2}$')
batch_id_pattern=compile('^[A-Z]+[0-9]{2}$')
batch_name_pattern=compile('^[A-Z]+ (19|20)[0-9]{2}-(19|20)[0-9]{2}$')
def course_resolve(func):
    course=retrieve(course_name)
    if course_id_pattern.search(course)==None:
        return func(course_name=course)
    else:
        return func(course_id=course)
def clean_entries(entry_list):
    for i in entry_list:i.grid_forget()
    entry_list.clear()
def view_course_performance():
    sheet=Texttable()
    sheet.set_cols_align(('l','l','r'))
    sheet.add_row(['Class Roll','Name','Marks'])
    for roll,name,marks in course_resolve(course_performance):sheet.add_row([roll,name,marks])
    show_performance.configure(state='normal')
    show_performance.delete(0.0,END)
    show_performance.insert(0.0,sheet.draw())
    show_performance.configure(state='disabled')
def batch_resolve(func):
    batch=retrieve(batch_name)
    if batch_id_pattern.search(batch)!=None:
        return func(batch_id=batch)
    elif batch_name_pattern.search(batch)!=None:
        return func(batch_name=batch)
    else:
        raise Error('Not a valid batch name')
def view_batch_list(func,widget):
    widget.configure(state='normal')
    widget.delete(0.0,END)
    widget.insert(0.0,'\n'.join(batch_resolve(func)))
    widget.configure(state='disabled')
def view_student_average():
    sheet=Texttable()
    sheet.set_cols_align(['l','l','r'])
    sheet.add_row(['Student','Name','Percentage'])
    for roll,name,percentage in batch_resolve(batch_performance):
        sheet.add_row([roll,name,f'{percentage:.2f}%'])
    show_student_average.configure(state='normal')
    show_student_average.delete(0.0,END)
    show_student_average.insert(0.0,sheet.draw())
    show_student_average.configure(state='disabled')
def view_department_batches():
    show_batches.configure(state='normal')
    show_batches.delete(0.0,END)
    show_batches.insert(0.0,'\n'.join(batches(department_id=retrieve(department_id))))
    show_batches.configure(state='disabled')
def view_department_performance():
    sheet=Texttable()
    sheet.set_cols_align(['l','r'])
    sheet.add_row(['Batch','Average'])
    for batch,percentage in batch_averages(department_id=retrieve(department_id)):
        sheet.add_row([batch,f'{percentage:.2f}%'])
    show_averages.configure(state='normal')
    show_averages.delete(0.0,END)
    show_averages.insert(0.0,sheet.draw())
    show_averages.configure(state='disabled')
def exam():
    def get_marks(papers):
        for paper in papers:
            batch_label.configure(text=paper.batch)
            student_label.configure(text=paper.roll_no)
            course_label.configure(text=f'Marks in {paper.course}')
            accept_marks.wait_variable(marks_input)
            yield paper,float(marks_input.get())
    def view_student_performance():
        chart=Texttable()
        chart.set_cols_align(('l','r'))
        chart.add_row(['Student ID','Average'])
        for student,average in examination.student_performance.items():
            chart.add_row([student,average])
        show_exam_performance.configure(state='normal')
        show_exam_performance.delete(0.0,END)
        show_exam_performance.insert(0.0,chart.draw())
        show_exam_performance.configure(state='disabled')
    exam_title=f'{retrieve(exam_name)} Exam'
    examination=Examination(exam_title,*[i.get() for i in exam_batch_input])
    interface.title(exam_title)
    exam_batch_input.clear()
    clean_entries(exam_batch_entries)
    hold_exam.pack_forget()
    provide_marks.pack()
    examination.enter_marks(get_marks(examination.take_exam()))
    #After exam
    post_exam=Frame(interface)
    Button(post_exam,image=home_image,command=lambda:(post_exam.pack_forget(),menu.pack())).grid(row=0)
    Button(post_exam,text='View Exam Results',command=view_student_performance).grid(row=1)
    Button(post_exam,text='View Exam Scatter Plot',command=lambda:(examination.statistics(),show())).grid(row=2)
    (show_exam_performance:=ScrolledText(post_exam)).grid(row=3);show_exam_performance.configure(state='disabled')
    provide_marks.pack_forget()
    post_exam.pack()
    interface.title('Results')
#menu
menu=Frame(interface)
    #student
Button(menu,text='Create Student',command=lambda:(menu.pack_forget(),student_creation.pack(),interface.title('Create Student'))).grid(column=0,row=0,sticky='nsew')
Button(menu,text='Update Student',command=lambda:(menu.pack_forget(),student_update.pack(),interface.title('Update Student'))).grid(column=0,row=1,sticky='nsew')
Button(menu,text='Remove Student',command=lambda:(menu.pack_forget(),student_removal.pack(),interface.title('Remove Student'))).grid(column=0,row=2,sticky='nsew')
Button(menu,text='Generate Report',command=lambda:(menu.pack_forget(),report_generation.pack(),interface.title('Generate Report'))).grid(column=0,row=3,sticky='nsew')
    #course
Button(menu,text='Create Course',command=lambda:(menu.pack_forget(),course_creation.pack(),interface.title('Create Course'))).grid(column=1,row=0,sticky='nsew')
Button(menu,text='View Course Performance',command=lambda:(menu.pack_forget(),course_perform.pack(),interface.title('Course Performance'))).grid(column=1,row=1,sticky='nsew')
Button(menu,text='Course Statistics',command=lambda:(menu.pack_forget(),course_statisticize.pack(),interface.title('Course Statistics'))).grid(column=1,row=2,sticky='nsew')
    #batch
Button(menu,text='Create Batch',command=lambda:(menu.pack_forget(),batch_creation.pack(),interface.title('Create Batch'))).grid(column=2,row=0,sticky='nsew')
Button(menu,text='View Batch Students',command=lambda:(menu.pack_forget(),batch_students.pack(),interface.title('Batch Students'))).grid(column=2,row=1,sticky='nsew')
Button(menu,text='View Batch Courses',command=lambda:(menu.pack_forget(),batch_courses.pack(),interface.title('Batch Courses'))).grid(column=2,row=2,sticky='nsew')
Button(menu,text='View Batch Performance',command=lambda:(menu.pack_forget(),batch_performed.pack(),interface.title('Batch Performance'))).grid(column=2,row=3,sticky='nsew')
Button(menu,text='Batch Pie Chart',command=lambda:(menu.pack_forget(),batch_statisticize.pack(),interface.title('Batch Pie Chart'))).grid(column=2,row=4,sticky='nsew')
    #department
Button(menu,text='Create Department',command=lambda:(menu.pack_forget(),department_creation.pack(),interface.title('Create Department'))).grid(column=3,row=0,sticky='nsew')
Button(menu,text='View Department Batches',command=lambda:(menu.pack_forget(),department_batches.pack(),interface.title('Department Batches'))).grid(column=3,row=1,sticky='nsew')
Button(menu,text='View Department Performance',command=lambda:(menu.pack_forget(),department_performance.pack(),interface.title('Department Performance'))).grid(column=3,row=2,sticky='nsew')
Button(menu,text='Department Line Plot',command=lambda:(menu.pack_forget(),department_statisticize.pack(),interface.title('Department Line Plot'))).grid(column=3,row=3,sticky='nsew')
    #examination
Button(menu,text='Take Exam',command=lambda:(menu.pack_forget(),hold_exam.pack(),interface.title('Hold Exam'))).grid(column=0,columnspan=4,row=5,sticky='nsew')
#entry variables
student_id=StringVar();student_name=StringVar();roll_no=StringVar();batch_id=StringVar()
course_id=StringVar();course_name=StringVar()
batch_id=StringVar();batch_name=StringVar();
department_id=StringVar();department_name=StringVar()
exam_name=StringVar();marks_input=DoubleVar()
#create Student
student_creation=Frame(interface)
Button(student_creation,image=home_image,command=lambda:(student_creation.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(student_creation,text='Student ID:').grid(column=0,row=1,sticky='e')
Entry(student_creation,textvariable=student_id).grid(column=1,row=1,stick='w')
Label(student_creation,text='Student Name:').grid(column=0,row=2,sticky='e')
Entry(student_creation,textvariable=student_name).grid(column=1,row=2,stick='w')
Label(student_creation,text='Class Roll Number').grid(column=0,row=3,sticky='e')
Entry(student_creation,textvariable=roll_no).grid(column=1,row=3,stick='w')
Label(student_creation,text='Batch ID:').grid(column=0,row=4,sticky='e')
Entry(student_creation,textvariable=batch_id).grid(column=1,row=4,stick='w')
Button(student_creation,text='Create',command=lambda:
    create_student(
        student_id=retrieve(student_id),
        name=retrieve(student_name),
        class_roll_no=retrieve(roll_no),
        batch=retrieve(batch_id)
    )
).grid(row=5,columnspan=2,sticky='nsew')
#update Student
student_update=Frame(interface)
Button(student_update,image=home_image,command=lambda:(student_update.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(student_update,text='Student ID:').grid(column=0,row=1,sticky='e')
Entry(student_update,textvariable=student_id).grid(column=1,row=1,stick='w')
Label(student_update,text='Student Name:').grid(column=0,row=2,sticky='e')
Entry(student_update,textvariable=student_name).grid(column=1,row=2,stick='w')
Label(student_update,text='Class Roll Number').grid(column=0,row=3,sticky='e')
Entry(student_update,textvariable=roll_no).grid(column=1,row=3,stick='w')
Button(student_update,text='Update',command=lambda:
    update_student(
        student_id=retrieve(student_id),
        name=retrieve(student_name),
        class_roll_no=retrieve(roll_no)
    )
).grid(row=4,columnspan=2,sticky='nsew')
#remove Student
student_removal=Frame(interface)
Button(student_removal,image=home_image,command=lambda:(student_removal.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(student_removal,text='Student ID:').grid(column=0,row=1,sticky='e')
Entry(student_removal,textvariable=student_id).grid(column=1,row=1,stick='w')
Button(student_removal,text='Remove',command=lambda:remove_student(retrieve(student_id))).grid(row=2,columnspan=2,sticky='nsew')
#report Student
report_generation=Frame(interface)
Button(report_generation,image=home_image,command=lambda:(report_generation.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(report_generation,text='Student ID:').grid(column=0,row=1,sticky='e')
Entry(report_generation,textvariable=student_id).grid(column=1,row=1,stick='w')
Button(report_generation,text='Generate Report',command=lambda:
    report(retrieve(student_id))
).grid(row=2,columnspan=2,sticky='nsew')
#create Course
course_creation=Frame(interface)
course_marks_input=[]
marks_entries=[]
Button(course_creation,image=home_image,command=lambda:(course_creation.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(course_creation,text='Course ID:').grid(column=0,columnspan=2,row=1,sticky='e')
Entry(course_creation,textvariable=course_id).grid(column=2,row=1,stick='w')
Label(course_creation,text='Course Name').grid(column=0,columnspan=2,row=2,sticky='e')
Entry(course_creation,textvariable=course_name).grid(column=2,row=2,sticky='w')
Label(course_creation,text='Class Roll No').grid(column=0,row=3,sticky='nsew')
Label(course_creation,text='Student Name').grid(column=1,row=3,sticky='nsew')
Label(course_creation,text='Marks').grid(column=2,row=3,sticky='nsew')
course_row=4
(marks_add:=Button(course_creation,image=plus_image,command=add_marks)).grid(column=1,row=4,sticky='e')
(marks_remove:=Button(course_creation,image=minus_image,command=lambda:(course_marks_input.pop(),marks_entries.pop().grid_forget(),marks_entries.pop().grid_forget()))).grid(column=2,row=4,sticky='w')
(course_create:=Button(course_creation,text='Create',command=lambda:(
    create_course(
        course_id=retrieve(course_id),
        course_name=retrieve(course_name),
        marks=[{
            'roll number':retrieve(roll_val),
            'name':retrieve(name_val),
            'marks':retrieve(marks_val)
        } for roll_val,name_val,marks_val in course_marks_input]
    ),
    [entry.grid_forget() for entry in marks_entries],
    marks_entries.clear(),
    course_marks_input.clear()
))).grid(columnspan=3,row=5,sticky='nsew')
#performance Course
course_perform=Frame(interface)
Button(course_perform,image=home_image,command=lambda:(course_perform.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(course_perform,text='Course:').grid(column=0,row=1,sticky='e')
Entry(course_perform,textvariable=course_name).grid(column=1,row=1,sticky='w')
Button(course_perform,text='View',command=view_course_performance).grid(columnspan=2,row=2,sticky='nsew')
show_performance=ScrolledText(course_perform,width=60,height=10);show_performance.grid(columnspan=2,row=3,sticky='nsew');show_performance.configure(state='disabled')
#statisticize course
course_statisticize=Frame(interface)
Button(course_statisticize,image=home_image,command=lambda:(course_statisticize.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(course_statisticize,text='Course:').grid(column=0,row=1,sticky='e')
Entry(course_statisticize,textvariable=course_name).grid(column=1,row=1,sticky='w')
Button(course_statisticize,text='View',command=lambda:(course_resolve(course_statistics),show())).grid(columnspan=2,row=2,sticky='nsew')
#create Batch
batch_creation=Frame(interface)
courses_row=5;students_row=7
batch_courses_input=[];batch_students_input=[]
course_entries=[];student_entries=[]
Button(batch_creation,image=home_image,command=lambda:(batch_creation.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(batch_creation,text='Batch ID:').grid(column=0,row=1,sticky='e')
Entry(batch_creation,textvariable=batch_id).grid(column=1,row=1,sticky='w')
Label(batch_creation,text='Batch Name:').grid(column=0,row=2,sticky='e')
Entry(batch_creation,textvariable=batch_name).grid(column=1,row=2,sticky='w')
Label(batch_creation,text='Department ID:').grid(column=0,row=3,sticky='e')
Entry(batch_creation,textvariable=department_name).grid(column=1,row=3,sticky='w')
Label(batch_creation,text='Courses').grid(columnspan=2,row=4,sticky='nsew')
(courses_add:=Button(batch_creation,image=plus_image,command=add_courses)).grid(column=0,row=5,sticky='e')
(courses_remove:=Button(batch_creation,image=minus_image,command=lambda:(course_entries.pop().grid_forget(),batch_courses_input.pop()))).grid(column=1,row=5,sticky='w')
(students_heading:=Label(batch_creation,text='Students')).grid(columnspan=2,row=6,sticky='nsew')
(students_add:=Button(batch_creation,image=plus_image,command=add_students)).grid(column=0,row=7,sticky='e')
(students_remove:=Button(batch_creation,image=minus_image,command=lambda:(student_entries.pop().grid_forget(),batch_students_input.pop()))).grid(column=1,row=7,sticky='w')
(batch_create:=Button(batch_creation,text='Create',command=lambda:(
    create_batch(
        batch_id=retrieve(batch_id),
        batch_name=retrieve(batch_name),
        department_name=retrieve(department_name),
        courses=[retrieve(i) for i in batch_courses_input],
        students=[retrieve(i) for i in batch_students_input]
    ),
    batch_courses_input.clear(),
    batch_students_input.clear(),
    clean_entries(course_entries),
    clean_entries(student_entries)
))).grid(columnspan=2,row=8,sticky='nsew')
#batch students
batch_students=Frame(interface)
Button(batch_students,image=home_image,command=lambda:(batch_students.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(batch_students,text='Batch:').grid(column=0,row=1,sticky='e')
Entry(batch_students,textvariable=batch_name).grid(column=1,row=1,sticky='w')
(show_students:=ScrolledText(batch_students,width=10,height=3)).grid(columnspan=2,row=3,sticky='nsew');show_students.configure(state='disabled')
Button(batch_students,text='View',command=partial(view_batch_list,students,show_students)).grid(columnspan=2,row=2,sticky='nsew')
#batch courses
batch_courses=Frame(interface)
Button(batch_courses,image=home_image,command=lambda:(batch_courses.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(batch_courses,text='Batch:').grid(column=0,row=1,sticky='e')
Entry(batch_courses,textvariable=batch_name).grid(column=1,row=1,sticky='w')
(show_courses:=ScrolledText(batch_courses,width=10,height=5)).grid(columnspan=2,row=3,sticky='nsew');show_courses.configure(state='disabled')
Button(batch_courses,text='View',command=partial(view_batch_list,courses,show_courses)).grid(columnspan=2,row=2,sticky='nsew')
#batch performance
batch_performed=Frame(interface)
Button(batch_performed,image=home_image,command=lambda:(batch_performed.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(batch_performed,text='Batch:').grid(column=0,row=1,sticky='e')
Entry(batch_performed,textvariable=batch_name).grid(column=1,row=1,sticky='w')
Button(batch_performed,text='View',command=view_student_average).grid(columnspan=2,row=2,sticky='nsew')
(show_student_average:=ScrolledText(batch_performed,width=50,height=10)).grid(columnspan=2,row=3,sticky='nsew');show_student_average.configure(state='disabled')
#batch statisticize
batch_statisticize=Frame(interface)
Button(batch_statisticize,image=home_image,command=lambda:(batch_statisticize.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(batch_statisticize,text='Batch:').grid(column=0,row=1,sticky='e')
Entry(batch_statisticize,textvariable=batch_name).grid(column=1,row=1,sticky='w')
Button(batch_statisticize,text='View',command=lambda:(batch_resolve(batch_statistics),show())).grid(columnspan=2,row=2,sticky='nsew')
#create Department
department_creation=Frame(interface)
batch_entries=[]
department_batch_input=[]
Button(department_creation,image=home_image,command=lambda:(department_creation.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(department_creation,text='Department ID:').grid(column=0,row=1,sticky='e')
Entry(department_creation,textvariable=department_id).grid(column=1,row=1,sticky='w')
Label(department_creation,text='Department Name:').grid(column=0,row=2,sticky='e')
Entry(department_creation,textvariable=department_name).grid(column=1,row=2,sticky='w')
Label(department_creation,text='Batches').grid(columnspan=2,row=3,sticky='nsew')
batches_row=4
(batch_add:=Button(department_creation,image=plus_image,command=add_batches)).grid(column=0,row=4,sticky='e')
(batch_remove:=Button(department_creation,image=minus_image,command=lambda:(batch_entries.pop().grid_forget(),department_batch_input.pop()))).grid(column=1,row=4,sticky='w')
(department_create:=Button(department_creation,text='Create',command=lambda:(
    create_department(
        department_id=retrieve(department_id),
        department_name=retrieve(department_name),
        batches=[retrieve(i) for i in department_batch_input]
    ),
    department_batch_input.clear(),
    clean_entries(batch_entries)
))).grid(columnspan=2,row=5,sticky='nsew')
#department batches
department_batches=Frame(interface)
Button(department_batches,image=home_image,command=lambda:(department_batches.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(department_batches,text='Department ID:').grid(column=0,row=1,sticky='e')
Entry(department_batches,textvariable=department_id).grid(column=1,row=1,sticky='w')
Button(department_batches,text='View',command=view_department_batches).grid(columnspan=2,row=2,sticky='nsew')
(show_batches:=ScrolledText(department_batches,width=10,height=8)).grid(columnspan=2,row=3,sticky='nsew');show_batches.configure(state='disabled')
#department performance
department_performance=Frame(interface)
Button(department_performance,image=home_image,command=lambda:(department_performance.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(department_performance,text='Department ID:').grid(column=0,row=1,sticky='e')
Entry(department_performance,textvariable=department_id).grid(column=1,row=1,sticky='w')
Button(department_performance,text='View',command=view_department_performance).grid(columnspan=2,row=2,sticky='nsew')
(show_averages:=ScrolledText(department_performance,width=10,height=10)).grid(columnspan=2,row=3,sticky='nsew');show_averages.configure(state='disabled')
#department statisticize
department_statisticize=Frame(interface)
Button(department_statisticize,image=home_image,command=lambda:(department_statisticize.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(department_statisticize,text='Department ID:').grid(column=0,row=1,sticky='e')
Entry(department_statisticize,textvariable=department_id).grid(column=1,row=1,sticky='w')
Button(department_statisticize,text='View',command=lambda:(
    department_statistics(department_id=retrieve(department_id)),
    show()
)).grid(columnspan=2,row=2,sticky='nsew')
#hold exam
exam_batch_input=[]
exam_batch_entries=[]
hold_exam=Frame(interface)
Button(hold_exam,image=home_image,command=lambda:(hold_exam.pack_forget(),menu.pack(),interface.title('Menu'))).grid(column=0,row=0,sticky='e')
Label(hold_exam,text='Examination:').grid(column=0,row=1,sticky='e')
Entry(hold_exam,textvariable=exam_name).grid(column=1,row=1,sticky='w')
Label(hold_exam,text='Batches').grid(columnspan=2,row=2,sticky='nsew')
exam_batch_row=3
(exam_batches_add:=Button(hold_exam,image=plus_image,command=add_batches_for_exam)).grid(column=0,row=3,sticky='e')
(exam_batches_remove:=Button(hold_exam,image=minus_image,command=lambda:(exam_batch_input.pop(),exam_batch_entries.pop().grid_forget()))).grid(column=1,row=3,sticky='w')
(start_exam:=Button(hold_exam,text='Start Exam',command=exam)).grid(columnspan=2,row=4,sticky='nsew')
#take exam
provide_marks=Frame(interface)
Label(provide_marks,text='Batch: ').grid(column=0,row=0)
Label(provide_marks,text='Student: ').grid(column=0,row=1)
(batch_label:=Label(provide_marks)).grid(column=1,row=0)
(student_label:=Label(provide_marks)).grid(column=1,row=1)
(course_label:=Label(provide_marks)).grid(column=0,row=2)
(exam_marks_entry:=Entry(provide_marks)).grid(column=1,row=2)
(accept_marks:=Button(provide_marks,text='Enter',command=lambda:(marks_input.set(exam_marks_entry.get()),exam_marks_entry.delete(0,END)))).grid(columnspan=2,row=3)
#---
menu.pack()
interface.mainloop()
