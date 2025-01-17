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
                   # admin_menu()
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
    print("ID\t\tName\t\tMarks\tGrade")
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

# Dictionary to store student data
students = {}

# User guide for the system
USER_GUIDE = """
Welcome to the Registrar System!

Features:
1. Register a new student.
2. View student information.
3. Update student details.
4. Manage course enrollment.
5. Generate student transcript.
6. Generate a report of all students.

Follow the on-screen instructions to use these features.
"""

# Function to register a new student
def register_student(student_id, first_name, last_name, course_enrolled):
    if student_id in students:
        return "Student ID already exists."
    students[student_id] = {
        "first_name": first_name,
        "last_name": last_name,
        "course_enrolled": course_enrolled,
        "transcript": []
    }
    return f"Student {first_name} {last_name} registered successfully."

# Function to view student information
def view_student(student_id):
    if student_id not in students:
        return "Student not found."
    student = students[student_id]
    return f"Student ID: {student_id}, Name: {student['first_name']} {student['last_name']}, Course: {student['course_enrolled']}"

# Function to update student information
def update_student(student_id, first_name=None, last_name=None, course_enrolled=None):
    if student_id not in students:
        return "Student not found."
    if first_name:
        students[student_id]["first_name"] = first_name
    if last_name:
        students[student_id]["last_name"] = last_name
    if course_enrolled:
        students[student_id]["course_enrolled"] = course_enrolled
    return f"Student {student_id} record updated successfully."

# Function to manage enrollment
def manage_enrollment(student_id, new_course):
    if student_id not in students:
        return "Student not found."
    if new_course == "":
        students[student_id]["course_enrolled"] = None
        return f"{students[student_id]['first_name']} {students[student_id]['last_name']} has been withdrawn from the course."
    students[student_id]["course_enrolled"] = new_course
    return f"{students[student_id]['first_name']} {students[student_id]['last_name']} has been enrolled in {new_course}."

# Function to issue a transcript
def issue_transcript(student_id):
    if student_id not in students:
        return "Student not found."
    student = students[student_id]
    transcript_entry = f"Transcript for {student['first_name']} {student['last_name']}: Enrolled in {student['course_enrolled']}."
    student["transcript"].append(transcript_entry)
    return transcript_entry

# Function to generate a report of all students
def generate_report():
    if not students:
        return "No students registered."
    report = "Student Report:\n"
    for student_id, student in students.items():
        report += f"Student ID: {student_id}, Name: {student['first_name']} {student['last_name']}, Course: {student['course_enrolled']}\n"
    return report

# Main function to run the system
def main():
    print("Welcome to the Registrar System!")
    guide_choice = input("Do you want to view the User Guide? (yes/no): ").strip().lower()
    if guide_choice == "yes":
        print(USER_GUIDE)
    
    while True:
        print("\nMenu:")
        print("1. Register a new student")
        print("2. View student information")
        print("3. Update student details")
        print("4. Manage course enrollment")
        print("5. Issue a transcript")
        print("6. Generate a report")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":  # Register a new student
            student_id = input("Enter student ID: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            course_enrolled = input("Enter the course to enroll in: ")
            print(register_student(student_id, first_name, last_name, course_enrolled))
        
        elif choice == "2":  # View student information
            student_id = input("Enter student ID: ")
            print(view_student(student_id))
        
        elif choice == "3":  # Update student details
            student_id = input("Enter student ID: ")
            first_name = input("Enter new first name (or press Enter to skip): ")
            last_name = input("Enter new last name (or press Enter to skip): ")
            course_enrolled = input("Enter new course (or press Enter to skip): ")
            print(update_student(student_id, first_name or None, last_name or None, course_enrolled or None))
        
        elif choice == "4":  # Manage course enrollment
            student_id = input("Enter student ID: ")
            new_course = input("Enter new course (or leave blank to withdraw): ")
            print(manage_enrollment(student_id, new_course))
        
        elif choice == "5":  # Issue a transcript
            student_id = input("Enter student ID: ")
            print(issue_transcript(student_id))
        
        elif choice == "6":  # Generate a report
            print(generate_report())
        
        elif choice == "7":  # Exit
            print("Exiting the system. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()



#--------------------------------------- Main program entry point--------------------------------------------------
users = load_users()
login(users)
