import os
from math import ceil
import getpass
import mysql.connector
from tabulate import tabulate
con = mysql.connector.connect(host='localhost', user = 'root', passwd = 'root',
        database = 'student')
mycursor = con.cursor()

global_username = ''

def studentMenu():
    os.system('cls')
    stat = "SELECT * FROM student WHERE username = '%s'"
    mycursor.execute(stat % global_username)
    res = mycursor.fetchone()
    global_rollno = res[1]
    global_name = res[2]
    global_prog = res[3]
    global_deptid = res[4]
    global_sem = res[5]
    print("Welcome ", global_name)
    while(True):
        print("Enter 1 to view the timetable")
        print("Enter 2 to view the attendance status")
        print("Enter 3 to quit")
        ans = int(input())
        if(ans == 1):
            os.system('cls')
            stat = "SELECT day, slot, course_id FROM timetable WHERE program='%s' AND dept_id=%d AND semester='%s'"
            mycursor.execute(stat % (global_prog, global_deptid, global_sem))
            timetable = {}
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            for i in days:
                for j in range(1,8):
                    if(j == 1):
                        timetable[i] = ['-']
                    else:
                        timetable[i].append('-')
            for i in mycursor:
                day = i[0]
                slot = i[1]
                c = i[2]
                timetable[day][slot-1] = c
            head = ['DAY', 1, 2, 3, 4, 5, 6, 7]
            tab = []
            for i in days:
                l = [i]
                for j in timetable[i]:
                    if(j == '-'):
                        l.append("FREE")
                    else:
                        l.append(j)
                tab.append(l)
            print(tabulate(tab, headers=head))
        elif(ans == 2):
            os.system('cls')
            courses = []
            stat1 = "SELECT DISTINCT(course_id) FROM timetable WHERE \
                    program= '%s' AND dept_id = %d AND semester = %d"
            mycursor.execute(stat1 % (global_prog, global_deptid, global_sem))
            for i in mycursor:
                if(i[0] != '-'):
                    courses.append([i[0]])
            c = 0
            for i in courses:
                tname = global_prog + "_" + str(global_deptid) + "_" + str(global_sem) + "_" + i[0]
                stat3 = "SELECT COUNT(DISTINCT(DATE)) FROM %s"
                mycursor.execute(stat3 % tname)
                count = (mycursor.fetchone())[0]
                stat4 = "SELECT COUNT(*) FROM %s WHERE rollno = %d AND (STATUS=1 OR STATUS = 2)"
                mycursor.execute(stat4 % (tname, global_rollno))
                scount = (mycursor.fetchone())[0]
                if(count == 0):
                    courses[c].append(100)
                    c += 1
                    continue
                pcent = (scount/count)*100
                courses[c].append(pcent)
                c += 1
            print(tabulate(courses, headers=['COURSE', 'PERCENTAGE']))
        elif(ans == 3):
            break
        else:
            print("Enter a valid input\n")

def facultyMenu():
    os.system('cls')
    quer = "SELECT faculty_id, faculty_name FROM faculty WHERE username='%s'"
    mycursor.execute(quer % global_username)
    res = mycursor.fetchone()
    f_id = res[0]
    print("Welcome ", res[1])
    while(True):
        print("Enter 1 to view the timetable")
        print("Enter 2 to view the attendance status")
        print("Enter 3 to mark attendance")
        print("Enter 4 to quit")
        ans = int(input())
        if(ans == 1):
            os.system('cls')
            timetable = {}
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            for i in days:
                for j in range(1,8):
                    if(j == 1):
                        timetable[i] = ['-']
                    else:
                        timetable[i].append('-')
            stat = "SELECT program, dept_id, semester, day, slot, course_id FROM TIMETABLE WHERE faculty_id = %d"
            mycursor.execute(stat % f_id)
            save = []
            for i in mycursor:
                save.append(i)
            for i in save:
                prog = i[0]
                dept_id = i[1]
                year = ceil(i[2]/2)
                day = i[3]
                slot = i[4]
                course = i[5]
                stat1 = "SELECT dept_name FROM department WHERE dept_id = %d"
                mycursor.execute(stat1 % dept_id)
                dname = (mycursor.fetchone())[0]
                timetable[day][slot-1] = "YEAR" + str(year) + " " + dname + " " + course 
            head = ['DAY', 1, 2, 3, 4, 5, 6, 7]
            tab = []
            for i in days:
                l = [i]
                for j in (timetable[i]):
                    if(j == '-'):
                        l.append('Free')
                    else:
                        l.append(j)
                tab.append(l)
            print(tabulate(tab, headers=head))
        elif(ans == 2):
            os.system('cls')
            courses = []
            stat1 = "SELECT course_id, program, dept_id, semester FROM teaches WHERE faculty_id=%d"
            mycursor.execute(stat1 % f_id)
            count = 0
            for i in mycursor:
                count += 1
                courses.append(i)
                print(count, i[0])
            print("Enter which course using the serial number")
            ans = int(input())
            course = courses[ans-1][0]
            prog = courses[ans-1][1]
            dept_id = courses[ans-1][2]
            sem = courses[ans-1][3]
            students = []
            stat2 = "SELECT rollnum FROM student WHERE program = '%s' AND\
                    dept_id = %d AND semester = %d"
            mycursor.execute(stat2 % (prog, dept_id, sem))
            for i in mycursor:
                students.append([i[0]])
            tname = prog + "_" + str(dept_id) + "_" + str(sem) + "_" + course
            stat3 = "SELECT COUNT(DISTINCT(DATE)) FROM %s"
            mycursor.execute(stat3 % tname)
            count = (mycursor.fetchone())[0]
            stat4 = "SELECT COUNT(*) FROM %s WHERE rollno = %d AND (STATUS=1 OR STATUS = 2)"
            c = 0
            for i in students:
                mycursor.execute(stat4 % (tname, i[0]))
                scount = (mycursor.fetchone())[0]
                pcent = (scount/count)*100
                students[c].append(pcent)
                c += 1
            head = ['RollNo', 'Percentage']
            print(tabulate(students, headers=head))
        elif(ans == 3):#mark attendance
            os.system('cls')
            courses = []
            stat1 = "SELECT course_id, program, dept_id, semester FROM teaches WHERE faculty_id=%d"
            mycursor.execute(stat1 % f_id)
            count = 0
            for i in mycursor:
                count += 1
                courses.append(i)
                print(count, i[0])
            print("Enter which course using the serial number")
            ans = int(input())
            course = courses[ans-1][0]
            prog = courses[ans-1][1]
            dept_id = courses[ans-1][2]
            sem = courses[ans-1][3]
            students = []
            stat2 = "SELECT rollnum FROM student WHERE program = '%s' AND\
                    dept_id = %d AND semester = %d"
            mycursor.execute(stat2 % (prog, dept_id, sem))
            for i in mycursor:
                students.append([i[0]])
            tname = prog + "_" + str(dept_id) + "_" + str(sem) + "_" + course
            print("Enter 0 for Absent\nEnter 1 for Present\nEnter 2 for OD")
            print("ROLL NUMBER\t\tSTATUS")
            c = 0
            for i in students:
                print(i[0],end = '\t\t\t')
                status=int(input())
                students[c].append(status)
                c += 1
            date='%d-%d-%d'
            day = input("Enter the date\n")
            month = input("Enter the month\n")
            year = input("Enter the year\n")
            date = day + '-' + month + year
            stat3 = "INSERT INTO %s VALUES('%s', %d, %d)"
            for i in students:
                mycursor.execute(stat3 % (tname, date, i[0], i[1]))
            print("DONE")
            con.commit()
        elif(ans == 4):
            break
        else:
            print("Enter a valid input\n")

def adminMenu():
    os.system('cls')
    print("Login successful!")
    while(True):
        print("Enter 1 to create a course")
        print("Enter 2 to assign faculties to courses")
        print("Enter 3 to create the timtable")
        print("Enter 4 to add a new faculty")
        print("Enter 5 to view the faculties for a department")
        print("Enter 6 to quit")
        ans = int(input())
        if(ans == 1):
            os.system('cls')
            course_id = input("Enter the course id\n")
            title = input("Enter the course's title\n")
            dept_id = int(input("Enter the department\n"))
            ccredits = int(input("Enter the number of credits\n"))
            ctype=input("Enter T for theory course and P for practical\n")
            stat = "INSERT INTO courses VALUES('%s', '%s', %d, %d, %d)"
            if(ctype == 'T'):
                mycursor.execute(stat % (course_id, title, dept_id, ccredits, 1))
            elif(ctype == 'P'):
                mycursor.execute(stat % (course_id, title, dept_id, ccredits, 0))
            else:
                print("Enter a valid course type")
            con.commit()

        elif(ans == 2):
            os.system('cls')
            fac_id = int(input("Enter the faculty id\n"))
            course_id = input("Enter the course id\n")
            program = input("Enter the program\n")
            dept_id = int(input("Enter the department id\n"))
            semester = int(input("Enter the semester\n"))
            stat = "INSERT INTO teaches VALUES(%d, '%s', '%s', %d, %d)"
            mycursor.execute(stat % (fac_id, course_id, program, dept_id, semester))
            print("Added!")
            con.commit()
        elif(ans== 3):
            os.system('cls')
            prog = input("Enter the program name\n")
            dept_id = int(input("Enter the department id\n"))
            sem = int(input("Enter the semester number\n"))
            table_name = prog + '_' + str(dept_id) + '_' + str(sem)
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            print("Enter free if no class is scheduled\n")
            stat1 = "Enter the class at slot %d on %s"
            stat2 = "INSERT INTO timetable VALUES('%s', %d, %d, '%s', %d, %d, '%s')"
            s = set()
            for i in days:
                for j in range(1,8):
                    print(stat1 % (j, i))
                    course_id = input()
                    if(course_id != "free"):
                        stat5 = "SELECT faculty_id FROM teaches WHERE\
                                course_id = '%s' AND program = '%s' AND\
                                dept_id = %d AND semester = %d"
                        mycursor.execute(stat5 %(course_id, prog, dept_id, sem))
                        fac_id = (mycursor.fetchone())[0]
                        mycursor.execute(stat2 % (prog, dept_id, sem, i, j, fac_id, course_id))
                        s.add(course_id)
                    else:
                        mycursor.execute(stat2 % (prog, dept_id, sem, i\
                                , j, 0, "-"))
            print("Timetable created!")
            for i in s:
                tt = table_name + '_' + i
                stat3 = "CREATE TABLE %s(\
                        DATE VARCHAR(30) NOT NULL,\
                        ROLLNO INTEGER NOT NULL,\
                        STATUS INTEGER)"
                mycursor.execute(stat3 % tt)
            con.commit()
                    
        elif(ans == 4):
            os.system('cls')
            stat0 = "SELECT MAX(faculty_id) FROM faculty"
            mycursor.execute(stat0)
            b = mycursor.fetchone()
            fac_id = b[0] + 1
            #fac_id = int(input("Enter the faculty id\n"))
            name = input("Enter the name\n")
            dept_id = int(input("Enter department id\n"))
            desig = input("Enter their designation\n")
            username = input("Enter their username\n")
            stat = "INSERT INTO faculty VALUES('%s', %d, '%s', %d, '%s');"
            mycursor.execute(stat % (username, fac_id, name, dept_id, desig))
            print("The new faculty has been added!")
            con.commit()
        elif(ans == 5):
            stat1 = "SELECT * FROM department"
            mycursor.execute(stat1)
            c = 0
            depts = []
            for i in mycursor:
                depts.append([i[0], i[1]])
            print(tabulate(depts, headers=['Dept No', 'Department Name']))
            choice = int(input("Enter the department id"))
            stat2 = "SELECT faculty_id, faculty_name FROM faculty WHERE dept_id = %d"
            mycursor.execute(stat2 % choice)
            facmem = []
            for i in mycursor:
                facmem.append([i[0], i[1]]) 
            print(tabulate(facmem, headers=['Faculty Id', 'Faculty Name']))
        elif(ans == 6):
            break
        else:
            print("Enter a valid input\n")


def accept():
    global global_username
    username = input("Enter the username\n")
    password = getpass.getpass("Enter the password\n")
    query = "SELECT password, type FROM login WHERE username = '%s'"
    mycursor.execute(query % username)
    res = mycursor.fetchone()
    if(mycursor.rowcount == 0):
        print("Incorrect username!")
    else:
        if(password == res[0]):
            global_username = username
            if(res[1] == 1):
                studentMenu()
            elif(res[1] == 2):
                facultyMenu()
            elif(res[1] == 3):
                adminMenu()
        else:
            print("Incorrect password!")
    
def menu():
    while(True):
        os.system('cls')
        print("Welcome to the Attendance Tracker")
        print("Enter 1 to login")
        print("Enter 2 to exit")
        a = int(input())
        if(a == 1):
            accept()
        elif(a == 2):
            break

if __name__ == '__main__':
    menu()
    print("BEWARE : 85% attendance is necessary to write your exams!")
    con.commit()
