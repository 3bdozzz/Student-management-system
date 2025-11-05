from dotenv import load_dotenv
import os
import mysql.connector
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

myCursor = db.cursor()

flat_list=[]
list1 =[]
list4 =[]
list5 = []
subjectsList = []
list6 = []
n=0

def get_name():
    while True:
        name = input("Enter name: ").lower().strip()
        if len(name) < 20:
            if name and all(i.isalpha() or i.isspace() for i in name):
                return name
            print("")
            print("\033[31mInvalid input\033[0m")
            print("")
        else:
            print("")
            print("\033[31mName cannot be longer than 20 characters\033[0m")
            print("")

def get_ID():
    while True:
            try:
                ID = int(input("Enter your Student ID: "))
                return ID
            except ValueError:
                print("")
                print("\033[31mInvalid input\033[0m")
                print("")

def get_Course():
    while True:
        Course = input("Enter course: ").lower().strip()
        if len(Course)<28:
            if Course and all(j.isalpha() or j.isspace() for j in Course):
                return Course
            print("")
            print("\033[31mInvalid input\033[0m")
            print("")
        else:
            print("")
            print("\033[31mCourse cannot be longer than 20 characters\033[0m")
            print("")

def get_age():
    while True:
        try:
            age = int(input("Enter age: "))
            while age < 17 or age > 50:
                print("")
                age = int(input("\033[31mEnter a valid age (17-50): \033[0m"))
                print("")
            return age
        except ValueError:
            print("")
            print("\033[31mInvalid input\033[0m")
            print("")

def get_GPA():
    while True:
        try:
            GPA = float(input("Enter GPA: "))
            while GPA < 0 or GPA > 4:
                print("")
                GPA = float(input("\033[31mEnter a valid GPA (0-4): \033[0m"))
                print("")
            return GPA
        except ValueError:
            print("")
            print("\033[31mInvalid input\033[0m")
            print("")

def addStudents():
    global list6
    print("Please enter the following details.")
    ID = get_ID()
    myCursor.execute('SELECT * FROM students WHERE Id = %s', (ID,))
    list1 = myCursor.fetchall()
    if len(list1) != 0:
        print("")
        print("\033[31mID is already taken. Please try again with a different ID.\033[0m")
        print("")
        return
    name = get_name()
    Course = get_Course()
    age = get_age()
    list6.append([ID,name])
    myCursor.execute("INSERT INTO Students (id, name, course, age) VALUES (%s, %s, %s, %s)",
                     (ID, name, Course, age))
    db.commit()
    for student in list1:
        myCursor.execute('SELECT GPA FROM intermediate')
        list10 = myCursor.fetchall()
    print("")
    print("\033[32mStudent added successfully\033[0m")
    print("")

def viewStudents():
    myCursor.execute('SELECT * FROM students ORDER BY Gpa DESC')
    list1 = myCursor.fetchall()


    if len(list1) == 0:
        print("")
        print("\033[38;5;214mNo students found!\033[0m")
        print("")
    else:

        print("\033[32mID \t\t\t\t\t\t Name \t\t\t\t\t\t Course \t\t\t\t\t\t Age \t     GPA\033[0m")
        print("\033[32m" + "-" * 101 + "\033[0m")
        for student in list1:
            myCursor.execute('SELECT AVG(GPA) FROM intermediate WHERE ID = %s', (student[0],))
            listCgpa = myCursor.fetchall()
            listCgpaFlat = []
            for tuple in listCgpa:
                for value in tuple:
                    if value != None:
                        value = round(value, 2)
                        listCgpaFlat.append(value)
                    else:
                        listCgpaFlat.append(value)

            print(f"{student[0]:<25}{student[1]:<28}{student[2]:<32}{student[3]:<12}{listCgpaFlat[0]}")
            print("")

def updateStudents():
    myCursor.execute('SELECT COUNT(*) FROM students')
    InOrNot = myCursor.fetchall()
    for tuple in InOrNot:
        for value in tuple:
            if value == 0:
                print("")
                print("\033[38;5;214mNo students found!\033[0m")
                print("")
                return
    ID = get_ID()
    myCursor.execute('SELECT * FROM students WHERE Id = %s', (ID,))
    list1 = myCursor.fetchall()
    flat_list.clear()
    for tuple in list1:
        for value in tuple:
            flat_list.append(value)
    else:
        print(flat_list)
        ID_found = False
        if flat_list[0] == ID:
                ID_found = True
                print("")
                print("Which of the following do you want to update")
                print("1. Name")
                print("2. Course")
                print("3. Age")
                print("4. GPA")
                while True:
                    try:
                        choice = int(input("Enter your choice (1-4): "))
                        if choice < 1 or choice > 4:
                            print("")
                            print("\033[31mInvalid choice.\033[0m")
                            print("")
                        else:
                            break
                    except ValueError:
                        print("")
                        print("\033[31mInvalid input.\033[0m")
                        print("")
                print("")
                print(f"You are currently updating {flat_list[0]}'s({flat_list[1]}) data")
                print("")
                if choice == 1:
                    name = get_name()
                    flat_list[1] = name
                    myCursor.execute("UPDATE students SET Name = %s WHERE Id = %s", (name, ID))
                    db.commit()
                elif choice == 2:
                    Course = get_Course()
                    flat_list[2] = Course
                    myCursor.execute('UPDATE students SET Course = %s WHERE Id = %s', (Course, ID))
                    db.commit()
                elif choice == 3:
                    age = get_age()
                    flat_list[3] = age
                    myCursor.execute('UPDATE students SET Age = %s WHERE Id = %s', (age, ID))
                    db.commit()
                elif choice == 4:
                    GPA = get_GPA()
                    flat_list[4] = GPA
                    myCursor.execute('UPDATE students SET Gpa = %s WHERE Id = %s', (GPA, ID))
                    db.commit()
                print("")
                print("\033[32mData updated successfully.\033[0m")
                print("")
                return

        if not ID_found:
            print("")
            print("\033[38;5;214mStudent not found!\033[0m")
            print("")

def deleteStudents():
    myCursor.execute('SELECT COUNT(*) FROM students')
    InOrNot = myCursor.fetchall()
    for tuple in InOrNot:
        for value in tuple:
            if value == 0:
                print("")
                print("\033[38;5;214mNo students found!\033[0m")
                print("")
                return
    else:
        allData = input("Do you want to delete all data?(y/n): ").lower()
        if allData == "y":
            myCursor.execute('DELETE FROM students')
            db.commit()
            myCursor.execute('DELETE FROM intermediate')
            db.commit()
            print("")
            print("\033[32mStudents deleted successfully\033[0m")
            print("")
        elif allData == "n":
            ID = get_ID()
            myCursor.execute('SELECT * FROM students WHERE Id = %s', (ID,))
            list1 = myCursor.fetchall()
            ID_found = False
            for student in list1:
                if student[0] == ID:
                    ID_found = True
                    while True:
                        YesNo = input(f"Are you sure you want to delete {student[1]} ({student[0]}) from the system (y/n): ").lower().strip()
                        print("")
                        if YesNo == "y" or YesNo == "n":
                            break
                        else:
                            print("\033[31mEnter a valid choice.\033[0m")
                            print("")
                    if YesNo == "y":
                        myCursor.execute('DELETE FROM students WHERE Id = %s', (ID,))
                        db.commit()
                        myCursor.execute('DELETE FROM intermediate WHERE Id = %s', (ID,))
                        db.commit()
                        print("\033[32mStudent deleted successfully\033[0m")
                        print("")
                    elif YesNo == "n":
                        break

            if not ID_found:
                print("")
                print("\033[38;5;214mStudent not found!\033[0m")
                print("")
        else:
            print("")
            print("\033[31mInvalid input\033[0m")
            print("")

def searchStudents():
    myCursor.execute('SELECT COUNT(*) FROM students')
    InOrNot = myCursor.fetchall()
    for tuple in InOrNot:
        for value in tuple:
            if value == 0:
                print("")
                print("\033[38;5;214mNo students found!\033[0m")
                print("")
                return
    else:
        print("")
        print("By which of the following would you like to search for a student/s")
        print("1. Name")
        print("2. Course")
        print("3. Specific ID")
        while True:
            try:
                choice2 = int(input("Enter your choice (1-3): "))
                if choice2 < 1 or choice2 > 3 :
                    print("")
                    print("\033[31mInvalid choice.\033[0m")
                    print("")
                break
            except ValueError:
                print("")
                print("\033[31mInvalid input.\033[0m")
                print("")

        if choice2 == 1:
            name_found=False
            name = get_name()
            myCursor.execute('SELECT * FROM students WHERE Name LIKE "%"%s"%"', (name,))
            list1 = myCursor.fetchall()
            print("\033[32mID \t\t\t\t\t\t Name \t\t\t\t\t\t Course \t\t\t\t\t\t Age \t     GPA\033[0m")
            print("\033[32m" + "-" * 100 + "\033[0m")
            for student in list1:
                if name in student[1]:
                    name_found = True
                    print(f"{student[0]:<25}{student[1]:<28}{student[2]:<32}{student[3]:<12}{student[4]}")
                    print("")
            if not name_found:
                print("")
                print(f"\033[38;5;214mNo one with the name of {name} was found\033[0m")
                print("")

        elif choice2 ==2:
            course_found = False
            Course = get_Course()
            myCursor.execute('SELECT * FROM students WHERE Course LIKE %s', (Course,))
            list1 = myCursor.fetchall()
            print("\033[32mID \t\t\t\t\t\t Name \t\t\t\t\t\t Course \t\t\t\t\t\t Age \t     GPA\033[0m")
            print("\033[32m" + "-" * 100 + "\033[0m")
            for student in list1:
                if student[2] == Course:
                    course_found = True
                    print(f"{student[0]:<25}{student[1]:<28}{student[2]:<32}{student[3]:<12}{student[4]}")
                    print("")
            if not course_found:
                print("")
                print("\033[38;5;214mNo one enrolled in that course.\033[0m")
                print("")

        elif choice2 == 3:
            ID = get_ID()
            myCursor.execute('SELECT * FROM students WHERE Id = %s', (ID,))
            list1 = myCursor.fetchall()
            ID_found = False
            for student in list1:
                if student[0] == ID:
                    ID_found = True
                    print("")
                    print("\033[32mID \t\t\t\t\t\t Name \t\t\t\t\t\t Course \t\t\t\t\t\t Age \t     GPA\033[0m")
                    print("\033[32m" + "-" * 100 + "\033[0m")
                    print(f"{student[0]:<25}{student[1]:<28}{student[2]:<32}{student[3]:<12}{student[4]}")
                    print("")
                    break
            if not ID_found:
                print("")
                print("\033[38;5;214mStudent not found!\033[0m")
                print("")

def alterSubjects():
        list5 = [0]
        list4.clear()
        flat_list.clear()
        myCursor.execute('SELECT COUNT(*) FROM students')
        InOrNot = myCursor.fetchall()
        for tuple in InOrNot:
            for value in tuple:
                if value == 0:
                    print("")
                    print("\033[38;5;214mNo students found!\033[0m")
                    print("")
                    return
        ID = get_ID()
        myCursor.execute('SELECT * FROM students WHERE Id = %s', (ID,))
        list1 = myCursor.fetchall()
        for tuple in list1:
            for value in tuple:
                flat_list.append(value)
        myCursor.execute('SELECT * FROM subjects')
        subjectsTableList = myCursor.fetchall()
        myCursor.execute('SElECT subject_ID FROM subjects')
        list3 = myCursor.fetchall()
        myCursor.execute('SELECT subject_ID FROM intermediate WHERE ID = %s', (ID,))
        list5 = myCursor.fetchall()
        for tuple in list5:
            for item in tuple:
                list4.append(item)
        addOrDelete = input("Do you want to add or delete subjects (a,d)? ").lower()
        if addOrDelete == "a":
            try:
                if flat_list[0] == ID:
                    print("\033[32mSubject_ID \t\t Subject_Name\033[0m")
                    print("\033[32m" + "-" * 35 + "\033[0m")
                    for item in subjectsTableList:
                        print(f"{item[0]:<17}{item[1]:<28}")
                    print("")
                    try:
                        subjects = int(input("Enter the subject ID to add: "))
                    except ValueError:
                        print("")
                        print("\033[91mInvalid input\033[0m")
                        print("")
                        return
                    if subjects > len(subjectsTableList) or subjects <= 0:
                        print("\033[91m\ninvalid option\n\033[0m")
                    elif subjects in list4:
                        print("\033[93m\nSubject already assigned\n\033[0m")
                    else:
                        GPA = get_GPA()
                        myCursor.execute('INSERT INTO intermediate VALUES (%s,%s,%s)', (ID,subjects,GPA))
                        db.commit()
                    while True:
                        list4.clear()
                        myCursor.execute('SELECT subject_ID FROM intermediate WHERE ID = %s', (ID,))
                        list5 = myCursor.fetchall()
                        for tuple in list5:
                            for item in tuple:
                                list4.append(item)
                        moreSubjects = input("Do you want to add more subjects? (y/n): ").lower()
                        if moreSubjects == "y":
                            try:
                                subjects = int(input("Enter the subject ID to add: "))
                            except ValueError:
                                print("")
                                print("\033[91mInvalid input\033[0m")
                                print("")
                                return
                            if subjects > len(subjectsTableList) or subjects < 0:
                                print("\033[91m\ninvalid option\n\033[0m")
                            elif subjects in list4:
                                print("\033[93m\nSubject already assigned\n\033[0m")
                            else:
                                GPA = get_GPA()
                                myCursor.execute('INSERT INTO intermediate VALUES (%s,%s,%s)', (ID,subjects,GPA))
                                db.commit()
                        elif moreSubjects == "n":
                            print("")
                            print("\033[92mSubjects added successfully\033[0m")
                            break
            except Exception:
                print("")
                print("\033[38;5;214mStudent not found!\033[0m")
                print("")
        elif addOrDelete == "d":
                if flat_list[0] == ID:
                    myCursor.execute('SELECT intermediate.subject_ID, subjects.subject_Name FROM intermediate INNER JOIN subjects ON intermediate.subject_ID = subjects.subject_ID WHERE ID = %s',(ID,))
                    list8 = myCursor.fetchall()
                    if len(list8) == 0:
                        print("")
                        print("\033[38;5;214mNo subjects assigned\033[0m")
                        print("")
                        return
                    else:
                        print("\033[32mSubject ID\t\tSubject Name\033[0m")
                        print("\033[32m" + "-" * 33 + "\033[0m")
                        for item in list8:
                            print(f"{item[0]:<16}{item[1]:<28}")
                        print("")
                        try:
                            subjects = int(input("Enter the subject ID to delete: "))
                        except ValueError:
                            print("")
                            print("\033[91mInvalid input\033[0m")
                            print("")
                            return
                        if subjects not in list4 or subjects <= 0:
                            print("\033[91m\ninvalid option\n\033[0m")
                        else:
                            myCursor.execute('DELETE FROM intermediate WHERE ID = %s AND subject_ID = %s', (ID,subjects))
                            db.commit()
                        while True:
                            list4.clear()
                            myCursor.execute('SELECT subject_ID FROM intermediate WHERE ID = %s', (ID,))
                            list5 = myCursor.fetchall()
                            for tuple in list5:
                                for item in tuple:
                                    list4.append(item)
                            moreSubjects = input("Do you want to delete more subjects? (y/n): ").lower()
                            if moreSubjects == "y":
                                try:
                                    subjects = int(input("Enter the subject ID to delete: "))
                                except ValueError:
                                    print("")
                                    print("\033[91mInvalid input\033[0m")
                                    print("")
                                    return
                                if subjects not in list4 or subjects < 0:
                                    print("\033[91m\ninvalid option\n\033[0m")
                                else:
                                    myCursor.execute('DELETE FROM intermediate WHERE ID = %s AND subject_ID = %s', (ID,subjects))
                                    db.commit()
                            elif moreSubjects == "n":
                                print("")
                                print("\033[92mSubjects deleted successfully\033[0m")
                                print("")
                                break

        else:
            print("")
            print("\033[31mInvalid input\033[0m")
            print("")
            return

def viewSubjects():
    global list8
    myCursor.execute('SELECT COUNT(*) FROM students')
    InOrNot = myCursor.fetchall()
    for tuple in InOrNot:
        for value in tuple:
            if value == 0:
                print("")
                print("\033[38;5;214mNo students found!\033[0m")
                print("")
                return
    ID = get_ID()
    myCursor.execute('SELECT COUNT(*) FROM intermediate WHERE ID = %s', (ID,))
    list7 = myCursor.fetchall()
    for tuple in list7:
        for value in tuple:
            if value == 0:
                print("")
                print(f"\033[38;5;214mThe student with the ID of {ID} didn't add any subjects yet\033[0m")
                print("")
                return
    myCursor.execute('SELECT intermediate.subject_ID, subjects.subject_Name, intermediate.GPA FROM intermediate INNER JOIN subjects ON intermediate.subject_ID = subjects.subject_ID WHERE ID = %s', (ID,))
    list8 = myCursor.fetchall()
    myCursor.execute('SELECT Name FROM students WHERE ID = %s', (ID,))
    list9 = myCursor.fetchall()
    print("\033[32mSubject_ID \t\t Subject_Name \t\t\t\t  GPA\033[0m")
    print("\033[32m" + "-" * 55 + "\033[0m")
    for item in list8:
        print(f"{item[0]:<17}{item[1]:<29}{item[2]:<}")
    print("")
    for tuple in list9:
        for name in tuple:
            print(f"\033[92mThe student {name} is enrolled in the subjects shown above\033[0m")
    print("")

"""key = "Abood2006"
print(f"Password is {key}")
while True:
    password = input("Enter password: ")
    if password == key:
        print("\nYou now have access to our student management system\n")"""

while True:
    print("1. Add students")
    print("2. View students")
    print("3. Update students' data")
    print("4. Delete student")
    print("5. Search student")
    print("6. Alter subjects")
    print("7. View subjects")
    print("8. Exit")
    while True:
        try:
            choice = int(input("choose an operation: "))
            break
        except ValueError:
            print("")
            print("\033[31mEnter a valid choice!!\033[0m")
            print("")
    if choice < 1 or choice > 8:
        print("")
        print("\033[31mEnter a valid choice!\033[0m")
        print("")
    elif choice == 1:
        addStudents()
    elif choice == 2:
        viewStudents()
    elif choice == 3:
        updateStudents()
    elif choice == 4:
        deleteStudents()
    elif choice == 5:
        searchStudents()
    elif choice == 6:
        alterSubjects()
    elif choice == 7:
        viewSubjects()
    elif choice == 8:
        print("")
        print("\033[32mThanks for using our student management system.\033[0m")
        break