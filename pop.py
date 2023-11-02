import mysql.connector
con = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'root',
        database = 'student')
mycursor = con.cursor()

def createTables():
    stat1 = "CREATE TABLE login(\
    username varchar(50) PRIMARY KEY,\
    password varchar(50),\
    type integer)"
    stat2 = "CREATE TABLE department(\
    dept_id INTEGER PRIMARY KEY,\
    dept_name varchar(50))"
    stat3 = "CREATE TABLE courses(\
    course_id varchar(50) PRIMARY KEY,\
    title varchar(50),\
    dept_id INTEGER NOT NULL,\
    FOREIGN KEY (dept_id) references department(dept_id),\
    credits integer,\
    type integer)"
    stat4 = "CREATE TABLE faculty(\
    username varchar(50) PRIMARY KEY,\
    faculty_id INTEGER NOT NULL,\
    faculty_name varchar(50),\
    dept_id INTEGER NOT NULL,\
    designation varchar(50),\
    FOREIGN KEY (dept_id) references department(dept_id))"
    stat5 = "CREATE TABLE teaches(\
    faculty_id INTEGER NOT NULL,\
    course_id VARCHAR(50) NOT NULL,\
    program VARCHAR(50),\
    dept_id INTEGER NOT NULL,\
    semester INTEGER,\
    FOREIGN KEY (dept_id) references department(dept_id),\
    FOREIGN KEY (course_id) references courses(course_id))"
    stat6 = "CREATE TABLE timetable(\
    program varchar(50),\
    dept_id integer NOT NULL,\
    semester integer,\
    day varchar(50),\
    slot integer,\
    faculty_id INTEGER NOT NULL,\
    course_id varchar(50) NOT NULL,\
    FOREIGN KEY (dept_id) references department(dept_id),\
    FOREIGN KEY (course_id) references courses(course_id))"
    stat7 = "CREATE TABLE student(\
    username varchar(50) PRIMARY KEY,\
    rollnum integer,\
    name varchar(50),\
    program varchar(50),\
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

createTables()

con.commit()

con.close()
