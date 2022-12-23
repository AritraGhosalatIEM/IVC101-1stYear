LATEX=xelatex
Departments=ECE\nIT\nCSE\nME
Sections=A\nB\nC\nD\nE\nF\nG\nH
Students=50-100
Courses=Physics Mathematics Biology Electrical Mechanics Python Design Entrepreneurship ESP SDP
project:latex/project.tex latex/template.tex 
	for path in outputs/*-report_card.txt;do\
		file=$$(basename "$$path");\
		echo "\\subsubsection*{$$(echo $$file | sed 's/_/\\_/g')}\n\\\\fontsize{12pt}{\\\\baselineskip}\\selectfont\n\\VerbatimInput[frame=lines,breaklines,breakanywhere,]{outputs/$$file}\n \\\\fontsize{14pt}{\\\\baselineskip}\\selectfont" >> latex/outputs.tex;\
	done
	for path in outputs/Course\ Statistics-*.pdf;do\
		file=$$(basename "$$path");\
		echo "\\subsubsection*{$$file}\n\\includegraphics{outputs/$$file}" >> latex/outputs.tex;\
	done
	for path in outputs/Batch\ Statistics-*.pdf;do\
		file=$$(basename "$$path");\
		echo "\\subsubsection*{$$file}\n\\includegraphics{outputs/$$file}" >> latex/outputs.tex;\
	done
	for path in outputs/Department\ Statistics-*.pdf;do\
		file=$$(basename "$$path");\
		echo "\\subsubsection*{$$file}\n\\includegraphics{outputs/$$file}" >> latex/outputs.tex;\
	done
	for path in outputs/*Exam.pdf;do\
		file=$$(basename "$$path");\
		echo "\\subsubsection*{$$file}\n\\includegraphics{outputs/$$file}" >> latex/outputs.tex;\
	done
	-$(LATEX) -interaction=nonstopmode -shell-escape latex/project.tex
	mv project.pdf F_28_Aritra\ Ghosal.pdf
databases/student.csv:
	echo "Student ID,Name,Class Roll No,Batch ID" > databases/student.csv;\
	IFS=';';\
	for name in $$(faker -r $$(shuf -i $(Students) -n 1) -l en_IN -s ';' name | tr -d '\n');do\
		batch="$$(printf '$(Departments)' | shuf -n 1)$$(shuf -i 1989-2022 -n 1 | cut -b 3-)";\
		echo "$$batch$$(shuf -i 100-199 -n 1 | cut -b 2-),$$name,$$(printf '$(Sections)' | shuf -n 1)-$$(shuf -i 100-199 -n 1 | cut -b 2-),$$batch" >> databases/student.csv;\
	done
databases/course.csv:databases/batch.csv
	echo "Course ID,Course Name,Marks obtained" > databases/course.csv;\
	courses="$(Courses)";\
	i=100;\
	for course in $$courses;do\
		i=$$((i+1));\
		course_id="C0$$(echo $$i | cut -b 2-)";\
		echo -n "$$course_id,$$course," >> databases/course.csv;\
		for student in $$(grep "$$course_id" databases/batch.csv | cut -d ',' -f 5 | tr ':' '\n' | sort -u);do\
			echo -n "$$student:$$(shuf -i 30-100 -n 1)-" >> databases/course.csv;\
		done;\
		echo >> databases/course.csv;\
	done;\
	sed -i 's/-$$//' databases/course.csv
databases/batch.csv:databases/student.csv
	subjects=$$(echo "$(Courses)" | wc -w);\
	for department in $$(printf "$(Departments)");do\
		eval $$department=$$(shuf -i 101-1$$subjects -n $$(shuf -i 1-$$subjects -n 1) | sort | sed 's/.\(..\)/C0\1/' | tr '\n' ':' | rev | cut -b 2- | rev);\
	done;\
	echo "Batch ID,Batch Name,Department Name,List of Courses,List of Students" > databases/batch.csv;\
	for batch in $$(sed '1d;s/.*,.*,.*,\(.*\)/\1/' databases/student.csv | sort -u);do\
		year=$$(echo $$batch | sed 's/.*\([0-9][0-9]\)/\1/');\
		department=$$(echo $$batch | sed 's/\(.*\)[0-9][0-9]/\1/');\
		if [ $$year -gt 22 ];then\
			year="19$$year";\
		else\
			year="20$$year";\
		fi;\
		echo -n "$$batch,$$department $$year-$$((year+4)),$$department," >> databases/batch.csv;\
		echo -n "$$(eval echo \$$$$department)," >> databases/batch.csv;\
		sed -n "s/\(^$$department[0-9]*\).*$$batch$$/\1/p" databases/student.csv | tr '\n' ':' >> databases/batch.csv;\
		echo >> databases/batch.csv;\
		sed -i 's/:$$//' databases/batch.csv;\
	done;
databases/department.csv:databases/batch.csv
	echo "Department ID,Department Name,List of Batches" > databases/department.csv
	echo -n "CSE,Computer Science and Engineering," >> databases/department.csv
	sed -n 's/\(CSE[0-9]*\),.*,.*,.*,.*/\1/p' databases/batch.csv | tr '\n' ':' >> databases/department.csv
	echo >> databases/department.csv
	echo -n "ECE,Electronics and Communication Engineering," >> databases/department.csv
	sed -n 's/\(ECE[0-9]*\),.*,.*,.*,.*/\1/p' databases/batch.csv | tr '\n' ':' >> databases/department.csv
	echo >> databases/department.csv
	echo -n "IT,Information Technology," >> databases/department.csv
	sed -n 's/\(IT[0-9]*\),.*,.*,.*,.*/\1/p' databases/batch.csv | tr '\n' ':' >> databases/department.csv
	echo >> databases/department.csv
	sed -i 's/:$$//' databases/department.csv
data: databases/student.csv databases/course.csv databases/batch.csv databases/department.csv
output:code/batch.py code/course.py code/department.py code/examination.py code/main.py
	(code/main.py)&\
	app=$$!;\
	sleep 2;\
	(window_id=$$(xdotool search --name Menu);\
	xinput test-xi2 --root | \
	grep --line-buffered RawKeyRelease |\
	while read _;do\
		maim "outputs/screenshots/$$(xdotool getwindowname $$window_id).png" -u -i $$window_id;\
	done)&\
	watch=$$!;\
	wait $$app;\
	kill $$watch
clean_data:
	rm databases/*
clean_output:
	rm outputs/screenshots/*
	-rm outputs/*
clean:
	-rm latex/outputs.tex
	-rm -r project.aux project.log project.out _minted-project
	-rm -r code/__pycache__
all:project clean
.PHONY: clean all clean_data clean_output output data project
