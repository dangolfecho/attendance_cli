import os
import getpass
import mysql.connector
from tabulate import tabulate
con = mysql.connector.connect(host='localhost', user = 'root', passwd = 'root',
        database = 'student')
mycursor = con.cursor()

global_username = ""
global_rollno = 0
global_name = ''
global_prog = ''
global_deptid = 0
global_sem = 0

def studentMenu():
    global global_username
    global global_rollno
    global global_name
    global global_prog
    global global_deptid
    global global_sem
    while(True):
        stat = "SELECT * FROM student WHERE username = '%s'"
        mycursor.execute(stat % global_username)
        res = mycursor.fetchone()
        global_rollno = res[1]
        global_name = res[2]
        global_prog = res[3]
        global_deptid = res[4]
        global_sem = res[5]
        print("Enter 1 to view the timetable")
        print("Enter 2 to view the attendance status")
        print("Enter 3 to quit")
        ans = int(input())
        if(ans == 1):
            stat = "SELECT * FROM timetable WHERE program='%s' AND dept_id=%d AND semester='%s'"
            mycursor.execute(stat % (global_prog, global_deptid, global_sem))
            res = mycursor.fetchall()
            print(tabulate(res))
        elif(ans == 2):
            print("HI")
        elif(ans == 3):
            break
        else:
            print("Enter a valid input")

def facultyMenu():
    quer = "SELECT faculty_id FROM faculty WHERE username='%s'"
    mycursor.execute(quer % global_username)
    res = mycursor.fetchone()
    f_id = res[0]
    while(True):
        print("Enter 1 to view the timetable")
        print("Enter 2 to view the attendance status")
        print("Enter 3 to mark attendance")
        print("Enter 4 to quit")
        ans = int(input())
        if(ans == 1):
            time_table = {}
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            for i in days:
                for j in range(1,8):
                    if(j == 1):
                        timetable[i] = ['-']
                    else:
                        timetable[i].append('-')
            stat = "SELECT program, dept_id, semester, day, slot, course_id FROM TIMETABLE WHERE faculty_id = %d"
            mycursor.execute(stat % f_id)
            for i in mycursor:
                prog = i[0]
                dept_id = i[1]
                year = ceil(i[2]/2)
                day = i[3]
                slot = i[4]
                course = i[5]
                timetable[day][slot-1] = str(year) + " " + course
            print(tabulate(timetable))
        elif(ans == 2):
            courses = []
            stat1 = "SELECT course_id, program, dept_id, semester FROM teaches WHERE faculty_id=%d"
            mycursor.execute(stat1 % f_id)
            count = 0
            for i in mycursor:
                save.append(i)
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
            stat2 = "SELECT "
        elif(ans == 3):#mark attendance
            courses = []
            stat1 = "SELECT course_id FROM teaches WHERE faculty_id=%d"
            mycursor.execute(stat1 % f_id)
            count = 0
            for i in mycursor:
                count += 1
                courses.append(i)
                print(count, i)
            print("Enter which course using the serial number")
            ans = int(input())
            ans -= 1
        elif(ans == 4):
            break
        else:
            print("Enter a valid input")

def hodMenu():
    while(True):
        print("Enter 1 to create a course")
        print("Enter 2 to assign faculties to courses")
        print("Enter 3 to create the timtable")
        print("Enter 4 to add a new faculty")
        print("Enter 5 to view the faculties for a department")
        print("Enter 6 to quit")
        ans = int(input())
        if(ans == 1):
            course_id = input("Enter the course id\n")
            title = input("Enter the course's title\n")
            dept_id = int(input("Enter the department\n"))
            ccredits = int(input("Enter the number of credits\n"))
            ctype=input("Enter T for theory course and P for practical")
            stat = "INSERT INTO courses VALUES('%s', '%s', %d, %d, %d"
            if(ctype == 'T'):
                mycursor.execute(stat % (course_id, title, dept_id, ccredits, 1))
            elif(ctype == 'P'):
                mycursor.execute(stat % (course_id, title, dept_id, ccredits, 0))
            else:
                print("Enter a valid course type")

        elif(ans == 2):
            fac_id = int(input("Enter the faculty id\n"))
            course_id = input("Enter the course id\n")
            program = input("Enter the program\n")
            dept_id = int(input("Enter the department id\n"))
            semester = int(input("Enter the semester\n"))
            stat = "INSERT INTO teaches VALUES(%d, '%s', '%s', %d, %d)"
            mycursor.execute(stat % (fac_id, course_id, program, dept_id, semester))
            print("Added!")
        elif(ans== 3):
            prog = input("Enter the program name\n")
            dept_id = int(input("Enter the department id\n"))
            sem = int(input("Enter the semester number\n"))
            table_name = prog + '_' + str(dept_id) + '_' + str(sem)
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            print("Enter free if no class is scheduled\n")
            stat1 = "Enter the class at slot %d on %s"
            stat2 = "INSERT INTO timetable VALUES('%s', %d, %d, %d, '%s', %d, '%s')"
            s = set()
            for i in days:
                for j in range(1,8):
                    print(stat1 % (i, j))
                    course_id = input()
                    if(course_id != "free"):
                        mycursor.execute(stat2 % (prog, dept_id, sem, i\
                                , j, course_id))
                        s.add(course_id)
                    else:
                        mycursor.execute(stat2 % (prog, dept_id, sem, i\
                                , j, "-"))
            for i in s:
                tt = table_name + '_' + i
                stat3 = "CREATE TABLE %s(\
                        DATE VARCHAR(30) NOT NULL,\
                        ROLLNO INTEGER NOT NULL,\
                        STATUS INTEGER)"
                mycursor.execute(stat3 % tt)
                    
        elif(ans == 4):
            fac_id = int(input("Enter the faculty id\n"))
            name = input("Enter the name\n")
            dept_id = int(input("Enter department id\n"))
            desig = input("Enter their designation\n")
            stat = "INSERT INTO faculty VALUES(%d, '%s', %d, '%s');"
            mycursor.execute(stat % (fac_id, name, dept_id, desig))
            print("The new faculty has been added!")
        elif(ans == 5):
            print("HI")
        elif(ans == 6):
            break
        else:
            print("Enter a valid input")


def accept():
    global global_username
    username = input("Enter the username\n")
    password = getpass.getpass("Enter the password\n")
    query = "SELECT password, type FROM login WHERE username = "
    query += "'" + username + "';"
    mycursor.execute(query)
    res = mycursor.fetchone()
    if(mycursor.rowcount == 0):
        print("Incorrect username!")
    else:
        if(password == res[0]):
            global_username = username
            print(global_username)
            print("Login successful!")
            if(res[1] == 1):
                studentMenu()
            elif(res[1] == 2):
                facultyMenu()
            elif(res[1] == 3):
                hodMenu()
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
    print("Done")
