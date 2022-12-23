from csv import writer,reader
from texttable import Texttable
def create_student(**kwargs):
    batch_id=kwargs['batch']
    student_id=kwargs['student_id']
    with open('databases/student.csv','a') as csvfile:
        writer(csvfile).writerow([
            student_id,
            kwargs['name'],
            kwargs['class_roll_no'],
            batch_id
        ])
    rows=[]
    with open('databases/batch.csv','r') as csvfile:
        for row in reader(csvfile):
            if row[0]==batch_id:
                row[4]+=f':{student_id}'
            rows.append(row)
    with open('databases/batch.csv','w') as csvfile:
        db=writer(csvfile)
        for row in rows:
            db.writerow(row)
def update_student(**kwargs):#update by student id
    rows=[]
    EXIT_CODE=1
    with open('databases/student.csv','r') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0]==kwargs['student_id']:
                EXIT_CODE=0
                rows.append([
                    row[0],
                    kwargs['name'] if 'name' in kwargs else row[1],
                    kwargs['class_roll_no'] if 'class_roll_no' in kwargs else row[2],
                    kwargs['student_id'][:-2]
                ])
                break
            rows.append(row)
        for row in db:rows.append(row)#add remaining
    with open('databases/student.csv','w') as csvfile:#update file
        db=writer(csvfile)
        for row in rows:db.writerow(row)
    return EXIT_CODE
def remove_student(student_id):#remove by student id
    rows=[]
    EXIT_CODE=1
    with open('databases/student.csv','r') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0]==student_id:#found
                batch_id=row[3]
                EXIT_CODE=0
                break
            rows.append(row)
        for row in db:rows.append(row)#add remaining
    with open('databases/student.csv','w') as csvfile:#update file
        db=writer(csvfile)
        for row in rows:db.writerow(row)
    if EXIT_CODE==1:return 1#student not found
    rows=[]
    empty_batch=False
    with open('databases/batch.csv','r') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0]==batch_id:
                students=row[4].split(':')
                students.remove(student_id)
                courses=row[3].split(':')
                if len(students)==0:
                    empty_batch=True
                    department_name=row[2]
                else:
                    row[4]=':'.join(students)
                    rows.append(row)
                break
            rows.append(row)
        for row in db:rows.append(row)
    with open('databases/batch.csv','w') as csvfile:
        db=writer(csvfile)
        for row in rows:db.writerow(row)
    rows=[]
    with open('databases/course.csv','r') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0] in courses:
                try:
                    marks=row[2]
                    a=marks.index(student_id)
                    b=marks.find('-',a)
                    row[2]=marks[:a-1]+marks[b:]
                except ValueError:#no marks given
                    continue
            rows.append(row)
    with open('databases/course.csv','w') as csvfile:
        db=writer(csvfile)
        for row in rows:db.writerow(row)
    if not empty_batch:return 0
    rows=[]
    with open('databases/department.csv','r') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0]==department_name:
                batches=row[2].split(':')
                batches.remove(batch_id)
                row[2]=':'.join(batches)
                rows.append(row)
                break
            rows.append(row)
        for row in db:rows.append(row)
    with open('databases/department.csv','w') as csvfile:
        db=writer(csvfile)
        for row in rows:db.writerow(row)
def report(student_id):
    def grade(marks):
        if marks>=90:grade='A'
        elif marks>=80:grade='B'
        elif marks>=70:grade='C'
        elif marks>=60:grade='D'
        elif marks>=50:grade='E'
        else: return 'F','Failed'
        return (grade,'Passed')
    EXIT_CODE=1
    with open('databases/student.csv') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0]==student_id:
                _,name,roll,batch_id=row
                EXIT_CODE=0
                break
    if EXIT_CODE==1:return 1
    with open('databases/batch.csv') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0]==batch_id:
                exams=row[3].split(':')
                break
    marksheet=Texttable()
    marksheet.set_cols_align(('l','l','r','r','c','l'))
    marksheet.add_row(['Course','Course Id','Marks Obtained','Full Marks','Grade','Remarks'])
    total=0
    with open('databases/course.csv') as csvfile:
        db=reader(csvfile)
        for row in db:
            if row[0] in exams:
                performance=row[2]
                i=performance.index(student_id)
                a=performance.find(':',i)
                b=performance.find('-',i)
                marks=float(performance[a+1:b])
                total+=marks
                marksheet.add_row([
                    row[1],
                    row[0],
                    marks,
                    100,
                    *grade(marks)
                ])
    number=len(exams)
    marksheet.add_row(['Total','-',total,number*100,*grade(total/number)])
    with open(f'outputs/{student_id}-report_card.txt','w') as report:report.write(f'''
{name} ({roll})

{marksheet.draw()}

ID:{student_id}
Batch:{batch_id}
 ''')
    return EXIT_CODE
