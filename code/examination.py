from csv import reader,writer
from numpy import nan,linspace
from collections import namedtuple
from matplotlib.pyplot import scatter,title,xlabel,ylabel,style,legend,close,savefig
from matplotlib.cm import Oranges as colormap #change to change colormap
Student=namedtuple('Performance',('student_id','average'))
class Examination:
    def __init__(self,*batches):
        self.name=input('Name of examination : ')
        exam_data={}
        course_name={}
        #remember data
        with open('databases/course.csv','r') as csvfile:
            csvfile.readline()
            for course_id,name,performance in reader(csvfile):
                exam_data[course_id]={} if performance=='' else dict((i.split(':') for i in performance.split('-')))
                course_name[course_id]=name
        self.batches=batches
        plot_data={}
        #input data
        self.student_performance=[]
        with open('databases/batch.csv','r') as batchcsv,open('databases/student.csv') as studentcsv:
            student_info=reader(studentcsv)
            for row in reader(batchcsv):
                batch_id=row[0]
                if batch_id in batches:
                    print(batch_id)
                    courses=row[3].split(':')
                    lcourses=len(courses)
                    students=row[4].split(':')
                    lstudents=len(students)
                    for student in students:
                        total=0
                        for info in student_info:
                            if info[0]==student:#found student id
                                print(f'\t{info[2]}')#print roll number
                                studentcsv.seek(0)
                                break
                        for course in courses:
                            entered=input(f'\t\t{course}: ')
                            marks=0 if entered=='' else float(entered)
                            total+=marks
                            exam_data[course][student]=marks
                            try:
                                plot_data[course][batch_id]+=marks/(lcourses*lstudents)
                            except KeyError:
                                try:
                                    plot_data[course][batch_id]=marks/(lcourses*lstudents)
                                except KeyError:
                                    plot_data[course]={batch_id:marks/(lcourses*lstudents)}
                        self.student_performance.append(Student(student,total/lcourses))
        #save data
        with open('databases/course.csv','w') as csvfile:
            db=writer(csvfile)
            db.writerow(['Course ID','Course Name','Marks Obtained'])
            for course in course_name:
                db.writerow([
                    course,
                    course_name[course],
                    '-'.join((f'{student}:{marks}' for student,marks in exam_data[course].items()))
                ])
        #arrange data
        self.data=[]
        self.courses=[]
        for course,course_data in plot_data.items():
            batch_data=[]
            for batch in batches:
                try:
                    batch_data.append(course_data[batch])
                except KeyError:
                    batch_data.append(nan)
            self.courses.append(course)
            self.data.append(batch_data)
    def statistics(self):
        style.use('Solarize_Light2')
        xlabel('Average Marks')
        ylabel('Batch')
        title(self.name)
        legend(
            (scatter(marks,self.batches,color=color,edgecolor='black') for marks,color in zip(self.data,colormap(linspace(0,1,len(self.data))))),
            self.courses
        )
        savefig(f'outputs/{self.name} Exam.png')
        close()
