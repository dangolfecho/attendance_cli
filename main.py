import mysql.connector
con = mysql.connector.connect(host='localhost', user = 'root', passwd = 'root',
        database = 'giffy')
mycursor = con.cursor()

def accept():
    username = input("Enter the username")
    password = input("Enter the password")
    query = "SELECT password FROM userinfo WHERE username = "
    query += "'" + username + "';"
    mycursor.execute(query)
    res = mycursor.fetchone()
    if(password == res[0]):
        print("Login successful!")
    else:
        print("Incorrect password!")

def menu():
    print("Enter 1 to login")
    print("Enter 2 to exit")
    a = input()
    if(a == '1'):
        accept()

if __name__ == '__main__':
    print("Welcome to the Attendance Tracker")
    menu()
