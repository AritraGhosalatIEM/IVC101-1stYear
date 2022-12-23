from csv import reader,writer
from numpy import nan,linspace
from collections import namedtuple
from matplotlib.pyplot import scatter,title,xlabel,ylabel,style,legend,close,savefig
from matplotlib.cm import Oranges as colormap #change to change colormap
Student=namedtuple('Performance',('student_id','average'))
Paper=namedtuple('Paper',('batch','student','roll_no','course','students','courses'))
class Examination:
    def __init__(self,exam_name,*batches):
        self.name=exam_name
        self.batches=batches
        self.course_name={}
        self.exam_data={}
        #remember data
        with open('databases/course.csv','r') as csvfile:
            csvfile.readline()
            for course_id,name,performance in reader(csvfile):
                self.exam_data[course_id]={} if performance=='' else dict((i.split(':') for i in performance.split('-')))
                self.course_name[course_id]=name
        self.student_performance={}
    def take_exam(self):
        with open('databases/batch.csv','r') as batchcsv,open('databases/student.csv') as studentcsv:
            student_info=reader(studentcsv)
            for row in reader(batchcsv):
                batch_id=row[0]
                if batch_id in self.batches:
                    courses=row[3].split(':')
                    lcourses=len(courses)
                    students=row[4].split(':')
                    lstudents=len(students)
                    for student in students:
                        total=0
                        for info in student_info:
                            if info[0]==student:#found student id
                                studentcsv.seek(0)
                                break
                        for course in courses:
                            yield Paper(batch_id,student,info[2],course,lstudents,lcourses)
    def enter_marks(self,exam):
        #get data
        plot_data={}
        for paper,marks in exam:
            try:
                self.student_performance[paper.student]+=marks/paper.courses
            except KeyError:
                self.student_performance[paper.student]=marks/paper.courses
            self.exam_data[paper.course][paper.student]=marks
            try:
                plot_data[paper.course][paper.batch]+=marks/paper.students
            except KeyError:
                try:
                    plot_data[paper.course][paper.batch]=marks/paper.students
                except KeyError:
                    plot_data[paper.course]={paper.batch:marks/paper.students}
        #save data
        with open('databases/course.csv','w') as csvfile:
            db=writer(csvfile)
            db.writerow(['Course ID','Course Name','Marks Obtained'])
            for course in self.course_name:
                db.writerow([
                    course,
                    self.course_name[course],
                    '-'.join((f'{student}:{marks}' for student,marks in self.exam_data[course].items()))
                ])
        #arrange data
        self.data=[]
        self.courses=[]
        for course,course_data in plot_data.items():
            batch_data=[]
            for batch in self.batches:
                try:
                    batch_data.append(course_data[batch])
                except KeyError:
                    batch_data.append(nan)
            self.courses.append(course)
            self.data.append(batch_data)
        self.courses,self.data=tuple(zip(*((x,y) for x,y in sorted(zip(self.courses,self.data)))))#sort data
    def statistics(self):
        close()
        style.use('Solarize_Light2')
        xlabel('Average Marks')
        ylabel('Batch')
        title(self.name)
        legend(
            (scatter(marks,self.batches,color=color,edgecolor='black') for marks,color in zip(self.data,colormap(linspace(0,1,len(self.data))))),
            self.courses
        )
        savefig(f'outputs/{self.name} Exam.pdf')
