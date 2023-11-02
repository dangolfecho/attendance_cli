import mysql.connector
con = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'root',
        database = 'student')
mycursor = con.cursor()

def createTables():
    stat1 = "CREATE TABLE login(\
    username varchar(30) PRIMARY KEY,\
    password varchar(30),\
    type integer)"
    stat2 = "CREATE TABLE department(\
    dept_id INTEGER PRIMARY KEY,\
    dept_name varchar(30))"
    stat3 = "CREATE TABLE courses(\
    course_id varchar(30) PRIMARY KEY,\
    title varchar(30),\
    dept_id INTEGER NOT NULL,\
    FOREIGN KEY (dept_id) references department(dept_id),\
    credits integer,\
    type integer)"
    stat4 = "CREATE TABLE faculty(\
    username varchar(30) PRIMARY KEY,\
    faculty_id INTEGER DISTINCT,\
    faculty_name varchar(30),\
    dept_id INTEGER NOT NULL,\
    designation varchar(30),\
    FOREIGN KEY (dept_id) references department(dept_id))"
    stat5 = "CREATE TABLE teaches(\
    faculty_id INTEGER NOT NULL,\
    course_id VARCHAR(30) NOT NULL,\
    program VARCHAR(30),\
    dept_id INTEGER NOT NULL,
    semester INTEGER,\
    FOREIGN KEY (faculty_id) references faculty(faculty_id),\
    FOREIGN KEY (dept_id) references department (department_id),\
    FOREIGN KEY (course_id) references courses(course_id))"
    stat6 = "CREATE TABLE timetable(\
    program varchar(30),\
    dept_id integer NOT NULL,\
    semester integer,\
    day varchar(30),\
    slot integer,\
    faculty_id INTEGER NOT NULL,\
    course_id varchar(30) NOT NULL,\
    FOREIGN KEY (dept_id) references department(dept_id),\
    FOREIGN KEY (faculty_id) references faculty(faculty_id),\
    FOREIGN KEY (course_id) references courses(course_id))"
    stat7 = "CREATE TABLE student(\
    username varchar(30) PRIMARY KEY,\
    rollnum integer,\
    name varchar(30),\
    program varchar(30),\
    dept_id integer NOT NULL,\
    semester integer,\
    FOREIGN KEY (dept_id) references department(dept_id),\
    FOREIGN KEY (username) references login(username))"
    mycursor.execute(stat1)
    mycursor.execute(stat2)
    mycursor.execute(stat3)
    mycursor.execute(stat4)
    mycursor.execute(stat5)
    mycursor.execute(stat6)
    mycursor.execute(stat7)

def insertRows():
    stat1 = "INSERT INTO login VALUES('211111@iiitt.ac.in', 'pass', 1);\
    INSERT INTO login VALUES('ambikam@iiitt.ac.in', 'pass', 2);\
    INSERT INTO login VALUES('hodcse@iiitt.ac.in', 'pass', 3);"
    mycursor.execute(stat1)
createTables()
insertRows()
