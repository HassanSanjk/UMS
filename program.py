#University Management System
#-------------------------------------------------------------------------------Common Functions------------------------------------------------------------------------------
STUDENTS_FILE = "students.txt"
COURSES_FILE = "courses.txt"
LECTURERS_FILE = "lecturers.txt"
ATTENDANCE_FILE = "attendance.txt"
GRADES_FILE = "grades.txt"
USERS_FILE = "users.txt"
RECEIPTS_FILE = "receipts.txt"

VALID_ROLES = ['student', 'lecturer', 'admin', 'accountant', 'registrar']
VALID_ATTENDANCE_STATUS = ['Present', 'Absent', 'Late']
CURRENT_SEMESTER = "2024/1"

# Function to read data from a file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            next(file)
            data = []
            for line in file:
                data.append(line.strip().split(","))
        return data
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
# Function to write data to a file
def write_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            file.writelines(data)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def append_file(file_path, data):
    try:
        with open(file_path, 'a') as file:
            file.writelines(data)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def get_student_details(student_id):
    """Get student details from students.txt with updated structure"""
    for line in read_file(STUDENTS_FILE):
        if len(line) >= 6:  # Updated to check for new file structure
            s_id, name, email, enrolled_courses, total_fees, outstanding_fees = line
            if s_id == student_id:
                return {
                    'id': s_id,
                    'name': name,
                    'email': email,
                    'enrolled_courses': enrolled_courses,
                    'total_fees': float(total_fees),
                    'outstanding_fees': float(outstanding_fees),
                    'status': 'Enrolled'
                }
    return None

def update_student_fees(student_id, payment_amount):
    """Update student fees in students.txt after payment"""
    students = read_file(STUDENTS_FILE)
    new_students = ["StudentID,Name,Email,EnrolledCourses,TotalFees,OutstandingFees\n"]
    updated = False
    
    for student in students:
        if len(student) >= 6 and student[0] == student_id:
            outstanding = float(student[5]) - payment_amount
            new_line = f"{student[0]},{student[1]},{student[2]},{student[3]},{student[4]},{outstanding}\n"
            new_students.append(new_line)
            updated = True
        else:
            new_students.append(','.join(student) + '\n')
    
    if updated:
        write_file(STUDENTS_FILE, new_students)
        
        # Record receipt
        receipt_id = f"R{len(read_file(RECEIPTS_FILE)) + 1:04d}"
        receipt_entry = f"{receipt_id},{student_id},{payment_amount},{CURRENT_SEMESTER}\n"
        append_file(RECEIPTS_FILE, [receipt_entry])
        
        return True
    return False

# Update the existing functions to work with new structure
def get_enrolled_students(course_code, semester):
    """Get list of students enrolled in a specific course with updated structure"""
    students = []
    for line in read_file(STUDENTS_FILE):
        if len(line) >= 6:  # Check for new file structure
            student_id, name, email, enrolled_courses, total_fees, outstanding_fees = line
            if course_code in enrolled_courses.split():
                students.append({
                    'id': student_id,
                    'name': name,
                    'email': email,
                    'total_fees': float(total_fees),
                    'outstanding_fees': float(outstanding_fees),
                    'status': 'Enrolled'
                })
    return students

# The rest of your functions (load_users, authenticate, login, etc.) remain the same
def load_users():
    """
    Load user data from users.txt
    Returns a dictionary with user email as key and dict of password and role as value
    """
    users = {}
    try:
        user_data = read_file(USERS_FILE)
        if not user_data:
            print("Warning: No users found in users.txt")
            return users
        for line in user_data:
            if len(line) >= 3:
                email, password, role = line
                if email and password and role:
                    users[email] = {
                        'password': password,
                        'role': role
                    }
            else:
                print(f"Warning: Invalid user data format found in users.txt")
    except Exception as e:
        print(f"Error loading users: {e}")
        exit()
    return users

def authenticate(email, password, users):
    """Authenticate user and redirect to appropriate menu"""
    if not email or not password:
        print("Email and password cannot be empty")
        return
    if email in users:
        if users[email]['password'] == password:
            role = users[email]['role']
            print(f"\nLogin successful! Welcome, {email}")
            while True:
                if role == 'student':
                    student_menu(email)
                    break
                elif role == 'lecturer':
                    lecturer_menu(email)
                    break
                elif role == 'admin':
                    admin_menu()
                    break
                elif role == 'accountant':
                    pass
                    break
                elif role == 'registrar':
                    print("Registrar menu not implemented yet")
                    break
                else:
                    print("Invalid role. Please contact administrator.")
                    break
        else:
            print("Incorrect password. Please try again.")
    else:
        print("User not found. Please try again.")

def login(users):
    print("\n----- Login -----")
    while True:
        email = input("Enter email: ").strip()
        if not email:
            print("Email cannot be empty")
            continue
        if '@' not in email or '.' not in email:
            print("Please enter a valid email address")
            continue
        break
        
    password = input("Enter password: ").strip()
    authenticate(email, password, users)


#----------------------------------------------------------HASSAN ABDALLA--------------------------------------------------------------------------------------
'''Lecturer 
• View Assigned Modules: View the list of modules assigned to the lecturers. 
• Record Grades: Add or update student grades for a specific module. 
• View Student List: Display the list of students enrolled in each assigned module. 
• Track Attendance: Mark attendance for students. 
• View Student Grades: Access grades for students in each of the lecturer's modules. '''
def get_courses(course_codes):
    """Get course details for multiple course codes"""
    if not course_codes:
        return []
        
    codes = course_codes.strip().split()
    courses = []
    all_courses = read_file(COURSES_FILE)
    
    for code in codes:
        for course in all_courses:
            if course[0] == code:
                courses.append(course)
                break
    
    return courses

def select_module(lecturer_id):
    """Select a module from lecturer's assigned courses"""
    for line in read_file(LECTURERS_FILE):
        l_id, l_name, l_email, course_code = line
        if l_id == lecturer_id:
            courses = get_courses(course_code)
            if not courses:
                print("\nNo modules assigned")
                input("Press Enter to continue...")
                return None
                
            print("\n=== Select Module ===")
            for i, course in enumerate(courses, 1):
                print(f"{i}. {course[0]} - {course[1]} (Semester {course[3]})")
                
            try:
                while True:
                    choice = input("\nEnter module number: ")
                    if choice.isdigit() and 1 <= int(choice) <= len(courses):
                        selected = courses[int(choice) - 1]
                        return {
                            'course_code': selected[0],
                            'course_name': selected[1],
                            'semester': selected[3]
                        }
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number")
                return None

def get_enrolled_students(course_code, semester):
    """Get list of students enrolled in a specific course"""
    students = []
    for line in read_file(STUDENTS_FILE):
        student_id, name, email, enrolled_courses, total_fees, outstanding_fees = line
        # Check if the course is in student's enrolled courses
        if course_code in enrolled_courses.split():
            students.append({
                'id': student_id,
                'name': name,
                'email': email,
                'status': 'Enrolled'
            })
    return students

def get_module_grades(course_code, semester):
    """Get all grades for a specific module"""
    grades = []
    for line in read_file(GRADES_FILE):
        student_id, module, marks, grade_letter = line
        if module == course_code:
            grades.append({
                'student_id': student_id,
                'marks': marks,
                'grade_letter': grade_letter
            })
    return grades

def calculate_grade(marks):
    """Calculate letter grade from numerical marks"""
    if marks >= 90:
        return 'A+'
    elif marks >= 85:
        return 'A'
    elif marks >= 80:
        return 'A-'
    elif marks >= 75:
        return 'B+'
    elif marks >= 70:
        return 'B'
    elif marks >= 65:
        return 'B-'
    elif marks >= 60:
        return 'C+'
    elif marks >= 55:
        return 'C'
    elif marks >= 50:
        return 'C-'
    elif marks >= 45:
        return 'D+'
    elif marks >= 40:
        return 'D'
    else:
        return 'F'

def update_grade(student_id, course_code, semester, marks, grade_letter):
    """Update or add new grade entry in grades.txt"""
    grades = read_file(GRADES_FILE)
    updated = False
    new_grades = []
    
    # Header for new file if it's empty
    if not grades:
        new_grades.append("StudentID,ModuleCode,Marks,Grade\n")
    
    for grade in grades:
        if grade[0] == student_id and grade[1] == course_code:
            new_grades.append(f"{student_id},{course_code},{marks},{grade_letter}\n")
            updated = True
        else:
            new_grades.append(','.join(grade) + '\n')
    
    if not updated:
        new_grades.append(f"{student_id},{course_code},{marks},{grade_letter}\n")
    
    write_file(GRADES_FILE, new_grades)
    print(f"\nGrade updated for student {student_id}")
    input("Press Enter to continue...")

def record_attendance(date, course_code, student_id, status, lecturer_id):
    """Record new attendance entry in attendance.txt"""
    attendance_entry = f"{course_code},{student_id},{date},{status}\n"
    
    # Read existing attendance to check for duplicates
    attendances = read_file(ATTENDANCE_FILE)
    for attendance in attendances:
        if (attendance[0] == course_code and 
            attendance[1] == student_id and 
            attendance[2] == date):
            print("\nAttendance already recorded for this date")
            input("Press Enter to continue...")
            return
    
    append_file(ATTENDANCE_FILE, [attendance_entry])
    print(f"\nAttendance recorded for student {student_id}")
    input("Press Enter to continue...")

def get_student_details(student_id):
    """Get student details from students.txt"""
    for line in read_file(STUDENTS_FILE):
        s_id, name, email, enrolled_courses, total_fees, outstanding_fees = line
        if s_id == student_id:
            return {
                'id': s_id,
                'name': name,
                'email': email,
                'status': 'Enrolled'
            }
    return None
def lecturer_menu(email):
    for line in read_file(LECTURERS_FILE):
        l_id, l_name, l_email, course_code = line
        if l_email == email:
            break

    while True:
        print(f"\n======= Welcome {l_name} ========")
        print("|   1. View Assigned Modules   |")
        print("|   2. Record/Update Grades    |")
        print("|   3. View Student List       |")
        print("|   4. Track Attendance        |")
        print("|   5. View Student Grades     |")
        print("|   6. Logout                  |")
        print("===============================\n")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_assigned_modules(l_id)
        elif choice == "2":
            record_grades(l_id)
        elif choice == "3":
            view_student_list(l_id)
        elif choice == "4":
            track_attendance(l_id)
        elif choice == "5":
            view_student_grades(l_id)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_assigned_modules(lecturer_id):
    for line in read_file(LECTURERS_FILE):
        l_id, l_name, l_email, course_code = line
        if l_id == lecturer_id:
            courses = get_courses(course_code)
            print(f"\n=== Assigned Modules for {l_name} ===")
            print("Course Code\tCourse Name\t\tCredit Hours\tSemester")
            print("-" * 70)
            for course in courses:
                print(f"{course[0]}\t\t{course[1]}\t\t{course[2]}\t\t{course[3]}")
            print("-" * 70)
            input("Press Enter to continue...")
            return

def record_grades(lecturer_id):
    module = select_module(lecturer_id)
    if not module:
        return

    students = get_enrolled_students(module['course_code'], module['semester'])
    if not students:
        print("\nNo students enrolled in this module.")
        input("Press Enter to continue...")
        return
    
    print(f"\n=== Record Grades for {module['course_code']} ===")
    print("Current grades:")
    print("\nStudent ID\tName\t\tCurrent Grade")
    print("-" * 50)
    
    current_grades = get_module_grades(module['course_code'], module['semester'])
    grades_dict = {grade['student_id']: grade['marks'] for grade in current_grades}
    
    for student in students:
        current_grade = grades_dict.get(student['id'], 'Not graded')
        print(f"{student['id']}\t{student['name']}\t\t{current_grade}")
    
    print("\nEnter new grades (0-100) or press Enter to skip:")
    for student in students:
        while True:
            grade_input = input(f"\nGrade for {student['name']} ({student['id']}): ").strip()
            if not grade_input:  # Skip this student
                break
            try:
                marks = float(grade_input)
                if 0 <= marks <= 100:
                    grade_letter = calculate_grade(marks)
                    update_grade(student['id'], module['course_code'], 
                               module['semester'], marks, grade_letter)
                    break
                else:
                    print("Marks must be between 0 and 100")
            except ValueError:
                print("Please enter a valid number")

def view_student_list(lecturer_id):
    module = select_module(lecturer_id)
    if not module:
        return
        
    students = get_enrolled_students(module['course_code'], module['semester'])
    if not students:
        print("\nNo students enrolled in this module.")
        input("Press Enter to continue...")
        return
    
    print(f"\n=== Student List for {module['course_code']} ===")
    print("ID\t\tName\t\t\tEmail")
    print("-" * 70)
    
    for student in students:
        print(f"{student['id']}\t{student['name']}\t\t{student['email']}")
    print("-" * 70)
    input("Press Enter to continue...")

def track_attendance(lecturer_id):
    module = select_module(lecturer_id)
    if not module:
        return
        
    students = get_enrolled_students(module['course_code'], module['semester'])
    if not students:
        print("\nNo students enrolled in this module.")
        input("Press Enter to continue...")
        return
    
    # Get date input
    while True:
        date = input("\nEnter date (YYYY/MM/DD): ")
        if len(date.split('/')) == 3:  # Basic date format validation
            break
        print("Invalid date format. Please use YYYY/MM/DD")
    
    print(f"\n=== Mark Attendance for {module['course_code']} ===")
    print(f"Date: {date}")
    print("\nMark attendance: (P)resent, (A)bsent, (L)ate")
    
    for student in students:
        while True:
            status = input(f"{student['name']} ({student['id']}): ").upper()
            if status in ['P', 'A', 'L']:
                full_status = {'P': 'Present', 'A': 'Absent', 'L': 'Late'}[status]
                record_attendance(date, module['course_code'], 
                                student['id'], full_status, lecturer_id)
                break
            else:
                print("Invalid input. Please use P, A, or L.")

def view_student_grades(lecturer_id):
    module = select_module(lecturer_id)
    if not module:
        return
        
    grades = get_module_grades(module['course_code'], module['semester'])
    if not grades:
        print("\nNo grades recorded for this module.")
        input("Press Enter to continue...")
        return
        
    print(f"\n=== Grade Report for {module['course_code']} ===")
    print("ID\t\tName\t\t\tMarks\tGrade")
    print("-" * 70)
    
    for grade in grades:
        student = get_student_details(grade['student_id'])
        if student:
            print(f"{student['id']}\t{student['name']}\t\t{grade['marks']}\t{grade['grade_letter']}")
    
    # Calculate and display statistics
    marks = [float(grade['marks']) for grade in grades]
    avg = sum(marks) / len(marks) if marks else 0
    highest = max(marks) if marks else 0
    lowest = min(marks) if marks else 0
    
    print("-" * 70)
    print(f"Class Average: {avg:.2f}")
    print(f"Highest Mark: {highest}")
    print(f"Lowest Mark: {lowest}")
    print("-" * 70)
    input("Press Enter to continue...")

#------------------------------------------------MOHAMMED EISSA--------------------------------------------------
'''
# Function to check if a student exists
def student_exists(student_id):
    fees = read_file(FEES_FILE)
    return any(parse_line(line, "fees")["student_id"] == student_id for line in fees)

# Function to get outstanding fees
def get_outstanding_fees(student_id):
    fees = read_file(FEES_FILE)
    for line in fees:
        data = parse_line(line, "fees")
        if data["student_id"] == student_id:
            return data["outstanding"]
    return None

# Function to validate numeric input
def get_valid_number(prompt, max_value=None):
    while True:
        value = input(prompt)
        if not value.replace('.', '', 1).isdigit():
            print("Error: Please enter a valid numeric value.")
        else:
            value = float(value)
            if value <= 0:
                print("Error: Value must be greater than 0.")
            elif max_value and value > max_value:
                print(f"Error: Value cannot exceed {max_value}.")
            else:
                return value

# Function to update all related files after payment
def update_related_files(student_id, amount_paid):
    try:
        # Update fees.txt
        fees = read_file(FEES_FILE)
        updated_fees = []
        for line in fees:
            data = parse_line(line, "fees")
            if data["student_id"] == student_id:
                data["paid"] += amount_paid
                data["outstanding"] -= amount_paid
                line = (
                    f"Student ID: {data['student_id']} | Name: {data['name']} | "
                    f"Paid: {data['paid']} | Total: {data['total']} | Outstanding: {data['outstanding']}"
                )
            updated_fees.append(line)
        write_file(FEES_FILE, updated_fees)

        # Update receipts.txt
        receipts = read_file(RECEIPTS_FILE)
        receipt_id = f"R{len(receipts) + 1:03}"
        receipt_record = f"Receipt ID: {receipt_id} | Student ID: {student_id} | Paid: {amount_paid} "
        receipts.append(receipt_record)
        write_file(RECEIPTS_FILE, receipts)

        print("All related files updated successfully.")
    except Exception as e:
        print(f"Error updating files: {e}")

# Function to record tuition fees
def record_tuition_fee():
    student_id = input("Enter Student ID: ")
    if not student_exists(student_id):
        print("Error: Student ID not found.")
        return

    outstanding_fees = get_outstanding_fees(student_id)
    if outstanding_fees == 0:
        print("No outstanding fees for this student.")
        return

    print(f"Outstanding Fees for Student ID {student_id}: {outstanding_fees}")
    amount_paid = get_valid_number(f"Enter Amount Paid (max: {outstanding_fees}): ", max_value=outstanding_fees)

    update_related_files(student_id, amount_paid)
    print("Tuition fee recorded successfully.")

# Function to view outstanding fees
def view_outstanding_fees():
    fees = read_file(FEES_FILE)
    outstanding = [
        line for line in fees if float(parse_line(line, "fees")["outstanding"]) > 0
    ]

    if outstanding:
        print("Outstanding Fees for Students:")
        for line in outstanding:
            data = parse_line(line, "fees")
            print(
                f"Student ID: {data['student_id']} - Name: {data['name']} - Outstanding: {data['outstanding']}"
            )
    else:
        print("No outstanding fees.")

# Function to update payment records
def update_payment_record():
    student_id = input("Enter Student ID: ")
    if not student_exists(student_id):
        print("Error: Student ID not found.")
        return

    new_amount = get_valid_number("Enter New Amount Paid: ")
    fees = read_file(FEES_FILE)
    updated_fees = []
    for line in fees:
        data = parse_line(line, "fees")
        if data["student_id"] == student_id:
            data["paid"] = new_amount
            data["outstanding"] = data["total"] - new_amount
            line = (
                f"Student ID: {data['student_id']} | Name: {data['name']} | "
                f"Paid: {data['paid']} | Total: {data['total']} | Outstanding: {data['outstanding']}"
            )
        updated_fees.append(line)
    write_file(FEES_FILE, updated_fees)
    print("Payment record updated successfully.")

# Function to issue receipts
def issue_receipt():
    student_id = input("Enter Student ID: ")
    receipts = read_file(RECEIPTS_FILE)

    # Filter receipts for the given student ID
    student_receipts = [
        parse_line(line, "receipts")
        for line in receipts
        if parse_line(line, "receipts")["student_id"] == student_id
    ]

    if not student_receipts:
        print("No receipt found for the given Student ID.")
        return

    # Get the latest receipt by position (last entry for the student)
    latest_receipt = student_receipts[-1]

    print(
        f"Receipt ID: {latest_receipt['receipt_id']} | Student ID: {latest_receipt['student_id']} | "
        f"Paid: {latest_receipt['paid']} "
    )

# Function to view financial summary
def view_financial_summary():
    fees = read_file(FEES_FILE)
    try:
        total_collected = sum(parse_line(line, "fees")["paid"] for line in fees)
        total_outstanding = sum(parse_line(line, "fees")["outstanding"] for line in fees)
    except ValueError:
        print("Error: Invalid data format.")
        return

    print("Financial Summary:")
    print(f"Total Fees Collected: {total_collected}")
    print(f"Total Outstanding Fees: {total_outstanding}")

# Main Menu
def accountant_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Record Tuition Fee")
        print("2. View Outstanding Fees")
        print("3. Update Payment Record")
        print("4. Issue Receipt")
        print("5. View Financial Summary")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            record_tuition_fee()
        elif choice == "2":
            view_outstanding_fees()
        elif choice == "3":
            update_payment_record()
        elif choice == "4":
            issue_receipt()
        elif choice == "5":
            view_financial_summary()
        elif choice == "6":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
'''

#-----------------------------------------Omda-----------------------------------------------------------------------

# Utility Functions for File Handling

def load_file(file_name):
    """
    Reads data from a file and returns a list of records.
    If the file does not exist, it returns an empty list.
    """
    try:
        with open(file_name, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]
    except FileNotFoundError:
        # If file is not found, return an empty list.
        return []

def save_to_file(file_name, data):
    """
    Overwrites the specified file with the provided data.
    Each record in 'data' is a list that will be joined using commas.
    """
    with open(file_name, 'w') as file:
        for record in data:
            file.write(','.join(record) + '\n')

def append_to_file(file_name, record):
    """
    Appends a single record (list) to the specified file.
    """
    with open(file_name, 'a') as file:
        file.write(','.join(record) + '\n')

# Administrator Role Functions

def add_course():
    """
    Adds a new course to the courses.txt file.
    Checks for duplicate course codes before adding.
    """
    course_code = input("Enter Course Code: ").strip()
    course_name = input("Enter Course Name: ").strip()
    credits = input("Enter Course Credits: ").strip()
    
    courses = load_file('courses.txt')  # Load existing courses
    for course in courses:
        if course[0] == course_code:  # Check for duplicate course codes
            print("Course already exists!")
            return
    append_to_file('courses.txt', [course_code, course_name, credits])  # Add new course
    print("Course added successfully!")

def remove_course():
    """
    Removes a course from the courses.txt file.
    If the course code does not exist, notifies the user.
    """
    course_code = input("Enter Course Code to Remove: ").strip()
    courses = load_file('courses.txt')  # Load existing courses
    courses_updated = [course for course in courses if course[0] != course_code]
    
    if len(courses) == len(courses_updated):  # If no changes were made
        print("Course not found!")
    else:
        save_to_file('courses.txt', courses_updated)  # Save updated course list
        print("Course removed successfully!")

def add_student():
    """
    Adds a new student to the students.txt file.
    Checks for duplicate student IDs before adding.
    """
    student_id = input("Enter Student ID: ").strip()
    student_name = input("Enter Student Name: ").strip()
    department = input("Enter Department: ").strip()
    
    students = load_file('students.txt')  # Load existing students
    for student in students:
        if student[0] == student_id:  # Check for duplicate student IDs
            print("Student already exists!")
            return
    append_to_file('students.txt', [student_id, student_name, department])  # Add new student
    print("Student added successfully!")

def remove_student():
    """
    Removes a student from the students.txt file.
    If the student ID does not exist, notifies the user.
    """
    student_id = input("Enter Student ID to Remove: ").strip()
    students = load_file('students.txt')  # Load existing students
    students_updated = [student for student in students if student[0] != student_id]
    
    if len(students) == len(students_updated):  # If no changes were made
        print("Student not found!")
    else:
        save_to_file('students.txt', students_updated)  # Save updated student list
        print("Student removed successfully!")

def manage_lecturers():
    """
    Manages lecturers by adding or removing their details.
    Prompts the user to choose an action.
    """
    action = input("Enter 'add' to add a lecturer or 'remove' to remove: ").strip().lower()
    if action == 'add':
        lecturer_id = input("Enter Lecturer ID: ").strip()
        lecturer_name = input("Enter Lecturer Name: ").strip()
        department = input("Enter Department: ").strip()
        
        lecturers = load_file('lecturers.txt')  # Load existing lecturers
        for lecturer in lecturers:
            if lecturer[0] == lecturer_id:  # Check for duplicate lecturer IDs
                print("Lecturer already exists!")
                return
        append_to_file('lecturers.txt', [lecturer_id, lecturer_name, department])  # Add new lecturer
        print("Lecturer added successfully!")
    elif action == 'remove':
        lecturer_id = input("Enter Lecturer ID to Remove: ").strip()
        lecturers = load_file('lecturers.txt')  # Load existing lecturers
        lecturers_updated = [lecturer for lecturer in lecturers if lecturer[0] != lecturer_id]
        
        if len(lecturers) == len(lecturers_updated):  # If no changes were made
            print("Lecturer not found!")
        else:
            save_to_file('lecturers.txt', lecturers_updated)  # Save updated lecturer list
            print("Lecturer removed successfully!")
    else:
        print("Invalid action! Please choose 'add' or 'remove'.")

def view_all_data():
    """
    Displays all data (students, courses, and lecturers) for administrative review.
    """
    print("\n--- Students ---")
    students = load_file('students.txt')
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Department: {student[2]}")
    
    print("\n--- Courses ---")
    courses = load_file('courses.txt')
    for course in courses:
        print(f"Code: {course[0]}, Name: {course[1]}, Credits: {course[2]}")
    
    print("\n--- Lecturers ---")
    lecturers = load_file('lecturers.txt')
    for lecturer in lecturers:
        print(f"ID: {lecturer[0]}, Name: {lecturer[1]}, Department: {lecturer[2]}")

def generate_reports():
    """
    Generates and displays a summary of students, courses, and lecturers.
    """
    students = load_file('students.txt')
    courses = load_file('courses.txt')
    lecturers = load_file('lecturers.txt')
    
    print("\n--- Reports ---")
    print(f"Total Students: {len(students)}")
    print(f"Total Courses: {len(courses)}")
    print(f"Total Lecturers: {len(lecturers)}")

# Menu for Administrator Role
def admin_menu():
    """
    Displays the Administrator Menu and handles menu navigation.
    """
    while True:
        print("\nAdministrator Menu:")
        print("1. Add Course")
        print("2. Remove Course")
        print("3. Add Student")
        print("4. Remove Student")
        print("5. Manage Lecturers")
        print("6. View All Data")
        print("7. Generate Reports")
        print("8. Exit")

        choice = input("Select an option: ").strip()
        if choice == '1':
            add_course()
        elif choice == '2':
            remove_course()
        elif choice == '3':
            add_student()
        elif choice == '4':
            remove_student()
        elif choice == '5':
            manage_lecturers()
        elif choice == '6':
            view_all_data()
        elif choice == '7':
            generate_reports()
        elif choice == '8':
            print("Exiting Administrator Menu...")
            break
        else:
            print("Invalid option! Please try again.")

#----------------------------------------------------KHALED------------------------------------------------------------------------

# STUDENTS_FILE = "students.txt"
# COURSES_FILE = "courses.txt"
# GRADES_FILE = "grades.txt"
# ATTENDANCE_FILE = "attendance.txt"


# ------------------------------
# Student Functions
# ------------------------------

# 1. View Available Modules
def view_available_modules():
    courses = read_file(COURSES_FILE)
    if not courses:
        print("No courses available.")
        return
    print("Available Modules:")
    print("Module ID | Module Name | Credit Hours | Semester")
    for course in courses:
        print(" | ".join(course))


# 2. Enroll in a Module
def enroll_in_module(student_id):
    courses = read_file(COURSES_FILE)
    students = read_file(STUDENTS_FILE)
    
    # Find the student
    student = next((s for s in students if s[0] == student_id), None)
    if not student:
        print(f"Student with ID {student_id} not found.")
        return

    print("Available Modules for Enrollment:")
    for i, course in enumerate(courses, start=1):
        print(f"{i}. {course[1]} (Module ID: {course[0]})")

    choice = input("Enter the number of the module to enroll in: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(courses):
        print("Invalid choice.")
        return
    
    selected_course = courses[int(choice) - 1][0]  # Get Module ID
    enrolled_courses = student[3].split(';') if student[3] else []

    if selected_course in enrolled_courses:
        print("You are already enrolled in this module.")
        return
    
    enrolled_courses.append(selected_course)
    student[3] = ';'.join(enrolled_courses)

    # Update the student record
    updated_students = [','.join(s) + '\n' for s in students]
    write_file(STUDENTS_FILE, updated_students)
    print(f"Successfully enrolled in {selected_course}.")


# 3. View Grades
def view_grades(student_id):
    grades = read_file(GRADES_FILE)
    student_grades = [g for g in grades if g[0] == student_id]
    
    if not student_grades:
        print("No grades available.")
        return

    print("Your Grades:")
    print("Module | Grade Percentage")
    for grade in student_grades:
        print(f"{grade[1]} | {grade[2]}%")


# 4. View Attendance
def view_attendance(student_id):
    attendance = read_file(ATTENDANCE_FILE)
    student_attendance = [a for a in attendance if a[1] == student_id]

    if not student_attendance:
        print("No attendance records found.")
        return

    print("Your Attendance:")
    print("Course Code | Date | Status")
    for record in student_attendance:
        print(" | ".join(record[0:4]))


# 5. Manage Personal Profile
def manage_profile(student_id):
    students = read_file(STUDENTS_FILE)
    
    # Find the student
    student = next((s for s in students if s[0] == student_id), None)
    if not student:
        print(f"Student with ID {student_id} not found.")
        return
    
    print("Your Profile:")
    print(f"ID: {student[0]}")
    print(f"Name: {student[1]}")
    print(f"Email: {student[2]}")
    print(f"Enrolled Courses: {student[3]}")
    
    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Email")
    print("3. Cancel")
    
    choice = input("Enter your choice: ")
    if choice == "1":
        new_name = input("Enter new name: ")
        student[1] = new_name
    elif choice == "2":
        new_email = input("Enter new email: ")
        student[2] = new_email
    else:
        print("Cancelled.")
        return
    
    # Update the student record
    updated_students = [','.join(s) + '\n' for s in students]
    write_file(STUDENTS_FILE, updated_students)
    print("Profile updated successfully.")


# ------------------------------
# Menu for Student Functions
# ------------------------------

def student_menu(email):
    for line in read_file(STUDENTS_FILE):
        student_id, s_name, s_email, courses, total_fees, outstanding_fees = line
        if s_email == email:
            break

    while True:
        print("\nStudent Menu:")
        print("1. View Available Modules")
        print("2. Enroll in a Module")
        print("3. View Grades")
        print("4. View Attendance")
        print("5. Manage Personal Profile")
        print("6. Logout")

        choice = input("Enter your choice: ")
        if choice == "1":
            view_available_modules()
        elif choice == "2":
            enroll_in_module(student_id)
        elif choice == "3":
            view_grades(student_id)
        elif choice == "4":
            view_attendance(student_id)
        elif choice == "5":
            manage_profile(student_id)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")




#---------------------------------------------------HUSSEIN-----------------------------------------------------------------------------------
'''
# Registrar & Documentation System with Enrollment Management

class Student:
   

    def __init__(self, student_id, first_name, last_name, course_enrolled):
        """
        Initializes a new student with the provided details.
        """
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.course_enrolled = course_enrolled
        self.transcript = []

    def update_record(self, first_name=None, last_name=None, course_enrolled=None):
    
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if course_enrolled:
            self.course_enrolled = course_enrolled

    def issue_transcript(self):
       
        self.transcript.append(f"Transcript for {self.first_name} {self.last_name}: Enrolled in {self.course_enrolled}.")
        return self.transcript[-1]

    def view_student_info(self):
        
        return f"Student ID: {self.student_id}, Name: {self.first_name} {self.last_name}, Course: {self.course_enrolled}"

    def manage_enrollment(self, new_course):
       
        if new_course == "":
            self.course_enrolled = None
            return f"{self.first_name} {self.last_name} has been removed from the course."
        else:
            self.course_enrolled = new_course
            return f"{self.first_name} {self.last_name} has been enrolled in {new_course}."


class Registrar:
  

    def __init__(self):
        """
        Initializes the registrar system with an empty student record database.
        """
        self.students = {}
    
    def register_student(self, student_id, first_name, last_name, course_enrolled):
        """
        Registers a new student in the system.
        
        Parameters:
        - student_id: Unique ID for the student.
        - first_name: The first name of the student.
        - last_name: The last name of the student.
        - course_enrolled: The course the student is enrolled in.
        """
        if student_id not in self.students:
            student = Student(student_id, first_name, last_name, course_enrolled)
            self.students[student_id] = student
            return f"Student {first_name} {last_name} registered successfully."
        return "Student ID already exists."
    
    def update_student_info(self, student_id, first_name=None, last_name=None, course_enrolled=None):
      
        student = self.students.get(student_id)
        if student:
            student.update_record(first_name, last_name, course_enrolled)
            return f"Student {student_id} record updated."
        return "Student not found."

    def view_student(self, student_id):
       
        student = self.students.get(student_id)
        if student:
            return student.view_student_info()
        return "Student not found."

    def issue_student_transcript(self, student_id):
       
        student = self.students.get(student_id)
        if student:
            return student.issue_transcript()
        return "Student not found."

    def generate_report(self):
    
        report = "Student Report:\n"
        for student in self.students.values():
            report += f"{student.view_student_info()}\n"
        return report

    def manage_enrollment(self, student_id, new_course):
       
        student = self.students.get(student_id)
        if student:
            return student.manage_enrollment(new_course)
        return "Student not found."


# System Documentation and User Guide
USER_GUIDE = """
System Documentation & User Guide

1. **Registrar System Overview**:
   - The Registrar System is designed to manage student records, including registration, enrollment, transcript issuance, and more.
   - Students can register for courses, update their information, view their enrollment status, and generate transcripts.
   - The system allows for enrollment management, meaning students can switch courses or withdraw from courses.

2. **Features**:
   - **Student Registration**: Registers new students with unique student IDs, names, and course enrollments.
   - **View Student Information**: Displays the student's registration details, including name and enrolled course.
   - **Enrollment Management**: Allows students to switch between courses or withdraw from a course entirely.
   - **Transcript Issuance**: Generates transcripts containing the student's enrolled course details.
   - **Student Information Update**: Updates student information, including name and course.
   - **Report Generation**: Generates a report of all students in the system with their details.

3. **User Guide**:
   - **Step 1**: When prompted, provide your student ID, first name, last name, and course for registration.
   - **Step 2**: You can choose to view your registration details after successfully registering.
   - **Step 3**: You can manage your enrollment by either enrolling in a new course or withdrawing from your current course.
   - **Step 4**: Update your personal or course information if needed.
   - **Step 5**: Generate a transcript of your enrollment details.
   - **Step 6**: If required, generate a report containing the details of all students in the system.

4. **System Requirements**:
   - The system runs in a standard Python environment with no external dependencies.
   - No database or file system is required as the system operates entirely in-memory.

5. **Usage Example**:
   - The system prompts users for their ID, name, course details, and allows for interaction with different functionalities like updating details, enrolling in courses, or generating transcripts.
"""

# Example Usage:
if __name__ == "__main__":
    registrar = Registrar()

    # Option to view the User Guide
    guide_choice = input("Do you want to view the User Guide? (yes/no): ")
    if guide_choice.lower() == 'yes':
        print(USER_GUIDE)

    # Input your details here dynamically
    print("Welcome! Please provide the following information:")
    
    # Take user input for registration
    student_id = input("Enter your student ID: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    course_enrolled = input("Enter the course you want to register for: ")

    # Register the student with the provided ID
    print(registrar.register_student(student_id, first_name, last_name, course_enrolled))
    
    # Option to view student information
    view_choice = input("\nDo you want to view your registration details? (yes/no): ")
    if view_choice.lower() == 'yes':
        print("\nYour registration details are:")
        print(registrar.view_student(student_id))

    # Option to manage enrollment (enroll in a new course or withdraw)
    manage_enrollment_choice = input("\nDo you want to manage your enrollment? (yes/no): ")
    if manage_enrollment_choice.lower() == 'yes':
        new_course = input("Enter the new course you want to enroll in (leave empty to withdraw): ")
        print(registrar.manage_enrollment(student_id, new_course))

    # Option to update student information
    update_choice = input("\nDo you want to update your details? (yes/no): ")
    if update_choice.lower() == 'yes':
        new_first_name = input("Enter your new first name (leave empty to skip): ")
        new_last_name = input("Enter your new last name (leave empty to skip): ")
        new_course = input("Enter your new course (leave empty to skip): ")
        
        # Update student info - If input is empty, pass None to indicate no update
        print(registrar.update_student_info(student_id, 
                                            new_first_name if new_first_name else None, 
                                            new_last_name if new_last_name else None, 
                                            new_course if new_course else None))

        # View updated information
        print("\nYour updated registration details are:")
        print(registrar.view_student(student_id))

    # Option to issue a transcript
    issue_transcript_choice = input("\nDo you want to issue a transcript? (yes/no): ")
    if issue_transcript_choice.lower() == 'yes':
        print("\nYour Transcript:")
        print(registrar.issue_student_transcript(student_id))

    # Option to generate a report of all students
    report_choice = input("\nDo you want to generate a report of all students? (yes/no): ")
    if report_choice.lower() == 'yes':
        print("\nGenerated Report:")
        print(registrar.generate_report())
'''
#--------------------------------------- Main program entry point--------------------------------------------------
users = load_users()
login(users)
