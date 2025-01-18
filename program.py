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

def get_date():
    # Get date input
    while True:
        date = input("\nEnter date (YYYY/MM/DD): ")
        valid_date = date.split('/')
        # Basic date format validation
        if len(valid_date) == 3:
            if valid_date[0].isdigit() and valid_date[1].isdigit() and valid_date[2].isdigit():
                # validating only dates between 2024 and 2030 with month in range 1-12 and date in range 1-31
                if 2024 <= int(valid_date[0]) <= 2030 and 1 <= int(valid_date[1]) <= 12 and 1 <= int(valid_date[2]) <= 31:
                    break
                else:
                    print("Invalid date range. Please enter a date between 2024 and 2030.")
                    continue
        print("Invalid date format. Please use YYYY/MM/DD")
    return date

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
                    admin_menu("admin@example.com")
                    break
                elif role == 'accountant':
                    accountant_menu()
                    pass
                    break
                elif role == 'registrar':
                    registrar_menu()
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

def get_courses(course_codes):
    #Get course details for multiple course codes
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
        print(f"\n===== Welcome {l_name.ljust(15)} =====")
        print("|    1. View Assigned Modules     |")
        print("|    2. Record/Update Grades      |")
        print("|    3. View Student List         |")
        print("|    4. Track Attendance          |")
        print("|    5. View Student Grades       |")
        print("|    6. Logout                    |")
        print("===================================\n")
        
        choice = input("Enter your choice: ")
        print("===============================\n")
        
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
            print(f"\n================== Assigned Modules for {l_name} ====================")
            print(f"Course Code".ljust(15) + "Course Name".ljust(25) + "Credit Hours".ljust(15) + "Semester")
            print("-" * 70)
            for course in courses:
                print(course[0].ljust(15) + course[1].ljust(25) + "    "+course[2].ljust(15) + course[3])
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
    
    print(f"\n=== Record Grades for {module['course_code']} ===\n")
    print("-"*55)
    print(f"Student ID".ljust(15) + "Name".ljust(25) + "Current Grade")
    print("-" * 55)
    
    current_grades = get_module_grades(module['course_code'], module['semester'])
    grades_dict = {grade['student_id']: grade['marks'] for grade in current_grades}
    
    for student in students:
        current_grade = grades_dict.get(student['id'], 'Not graded')
        print(student['id'].ljust(15) + student['name'].ljust(25) + current_grade)
    
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
    print(f"ID".ljust(10) + "Name".ljust(25)+"Email")
    print("-" * 60)
    
    for student in students:
        print(student['id'].ljust(10) + student['name'].ljust(25)+student['email'])
    print("-" * 60)
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
    
    date = get_date()
    
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
    print(f"ID".ljust(10)+"Name".ljust(25)+"Marks".ljust(10)+"Grade")
    print("-" * 70)
    
    for grade in grades:
        student = get_student_details(grade['student_id'])
        if student:
            print(student['id'].ljust(10)+student['name'].ljust(25)+grade['marks'].ljust(10)+grade['grade_letter'])
    
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
def record_tuition_fee():
    """Record a payment and update student fees."""
    student_id = input("Enter Student ID: ").strip()
    student = get_student_details(student_id)
    if not student:
        print("Error: Student ID not found.")
        return

    if student['outstanding_fees'] == 0:
        print("This student has no outstanding fees. No payment required.")
        return

    print(f"Outstanding Fees: {student['outstanding_fees']}")

    while True:
        try:
            payment = float(input("Enter payment amount: "))
            if payment <= 0:
                print("Error: Payment amount must be greater than 0.")
            elif payment > student['outstanding_fees']:
                print("Error: Payment amount exceeds outstanding fees. Please enter a valid amount.")
            else:
                break  # Valid payment entered
        except ValueError:
            print("Error: Please enter a valid number.")

    students = read_file(STUDENTS_FILE)
    updated_students = [students[0]]  # Keep header

    for record in students[1:]:
        if len(record) >= 6 and record[0].strip().lower() == student_id.strip().lower():
            outstanding_fees = float(record[5].strip()) - payment
            updated_students.append([
                record[0].strip(), record[1].strip(), record[2].strip(), record[3].strip(),
                record[4].strip(), f"{outstanding_fees:.2f}"
            ])

            receipt_id = f"R{len(read_file(RECEIPTS_FILE)) + 1:04d}"
            date = get_date()
            append_file(RECEIPTS_FILE, [receipt_id, student_id, f"{payment:.2f}", date])
        else:
            updated_students.append(record)

    write_file(STUDENTS_FILE, updated_students)
    print("Student record updated successfully.")


def view_outstanding_fees():
    """Display students with outstanding fees."""
    students = read_file(STUDENTS_FILE)
    if len(students) <= 1:
        print("No students found in the file.")
        return

    print("\n--- Students with Outstanding Fees ---")
    found = False
    for student in students[1:]:
        if len(student) >= 6 and float(student[5].strip()) > 0:
            print(f"Student ID: {student[0].strip()}, Name: {student[1].strip()}, Outstanding Fees: {student[5].strip()}")
            found = True

    if not found:
        print("No students with outstanding fees.")

def update_payment_record():
    """Update a specific payment record."""
    student_id = input("Enter Student ID: ").strip()
    student = get_student_details(student_id)
    if not student:
        print("Error: Student ID not found.")
        return

    try:
        new_outstanding = float(input("Enter new outstanding amount: "))
        if new_outstanding < 0 or new_outstanding > student['total_fees']:
            print("Error: Invalid outstanding amount.")
            return

        students = read_file(STUDENTS_FILE)
        updated_students = [students[0]]  # Keep header

        for record in students[1:]:
            if len(record) >= 6 and record[0].strip().lower() == student_id.strip().lower():
                updated_students.append([
                    record[0].strip(), record[1].strip(), record[2].strip(), record[3].strip(), record[4].strip(), f"{new_outstanding:.2f}"
                ])
            else:
                updated_students.append(record)

        write_file(STUDENTS_FILE, updated_students)
        print(f"Outstanding amount for {student['name']} updated successfully.")
    except ValueError:
        print("Error: Please enter a valid number.")

def issue_receipt():
    """Display the latest receipt for a student."""
    student_id = input("Enter Student ID: ").strip()
    receipts = read_file(RECEIPTS_FILE)
    if len(receipts) <= 1:
        print("No receipts found.")
        return

    latest_receipt = None
    for receipt in receipts:
        if len(receipt) >= 4 and receipt[1].strip().lower() == student_id.strip().lower():
            latest_receipt = receipt

    if latest_receipt:
        print(f"\n--- Latest Receipt ---\nReceipt ID: {latest_receipt[0]}, Student ID: {latest_receipt[1]}, Amount Paid: {latest_receipt[2]}, Date: {latest_receipt[3]}")
    else:
        print("No receipts found for this student.")

def view_financial_summary():
    """Display total paid and outstanding fees."""
    students = read_file(STUDENTS_FILE)
    if len(students) <= 1:
        print("No students found in the file.")
        return

    total_paid = 0
    total_outstanding = 0

    for student in students[1:]:
        if len(student) >= 6:
            total_fees = float(student[4].strip())
            outstanding_fees = float(student[5].strip())
            total_paid += total_fees - outstanding_fees
            total_outstanding += outstanding_fees

    print("\n--- Financial Summary ---")
    print(f"Total Paid: {total_paid:.2f}")
    print(f"Total Outstanding: {total_outstanding:.2f}")

# Main Menu
def accountant_menu():
    while True:
        print("\n" + "🌟" * 40)
        print(" " * 12 + "✨ MAIN MENU ✨")
        print("🌟" * 40)
        print("🔹 1️⃣  📋 Record Tuition Fee")
        print("🔹 2️⃣  💳 View Outstanding Fees")
        print("🔹 3️⃣  ✏️  Update Payment Record")
        print("🔹 4️⃣  🧾 Issue Receipt")
        print("🔹 5️⃣  📊 View Financial Summary")
        print("🔹 6️⃣  ❌ Exit")
        print("🌟" * 40)
        print("✅ Please select an option by entering its number ✅\n")

        choice = input("Enter your choice: ").strip()
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

#-----------------------------------------Omda-----------------------------------------------------------------------
def reset_user_password():
    """Allows the administrator to reset a user's password."""
    user_id = input("Enter User ID: ").strip()
    new_password = input("Enter New Password: ").strip()

    users = load_file('users.txt')
    user_found = False
    for user in users:
        if user[0] == user_id:
            user[1] = new_password
            user_found = True

    if user_found:
        save_to_file('users.txt', users)
        print("Password reset successfully!")
    else:
        print("User ID not found.")



def ensure_file_exists(file_name, header=None):
    """Ensures the specified file exists. Creates it with an optional header if not."""
    try:
        with open(file_name, 'r'):
            pass
    except FileNotFoundError:
        with open(file_name, 'w') as file:
            if header:
                file.write(header + '\n')

def load_file(file_name):
    """
    Reads data from a file and returns a list of records.
    Ensures the file exists before attempting to read.
    """
    try:
        with open(file_name, 'r') as file:
            return [line.strip().split(',') for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"\n----------------------------------------")
        print(f"Error: File '{file_name}' does not exist.")
        print("----------------------------------------")
        return []


def save_to_file(file_name, data):
    """
    Overwrites the specified file with new data.
    """
    try:
        with open(file_name, 'w') as file:
            for record in data:
                file.write(','.join(record) + '\n')
    except Exception as e:
        print(f"\n----------------------------------------")
        print(f"Error: Could not write to {file_name}. Reason: {e}")
        print("----------------------------------------")


def append_to_file(file_name, record):
    """
    Appends a single record to a file.
    """
    try:
        with open(file_name, 'a') as file:
            file.write(','.join(record) + '\n')
    except Exception as e:
        print(f"\n----------------------------------------")
        print(f"Error: Could not append to {file_name}. Reason: {e}")
        print("----------------------------------------")

def admin_menu(user_email):
    """
    Displays the Administrator menu.
    """
    while True:
        print("\n" + "-" * 40)
        print("         Administrator Menu")
        print("-" * 40)
        print(f"Logged in as: {user_email}")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Add Course")
        print("4. Remove Course")
        print("5. View All Data")
        print("6. Generate Reports")
        print("7. Exit")
        print("-" * 40)

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_student()
        elif choice == '2':
            remove_student()
        elif choice == '3':
            add_course()
        elif choice == '4':
            remove_course()
        elif choice == '5':
            file_name = input("Enter the file name to view: ").strip()
            view_all_data(file_name)
        elif choice == '6':
            report_menu()
        elif choice == '7':
            print("\nExiting Administrator Menu...")
            break
        else:
            print("\nInvalid choice. Please try again.")

def add_student():
    """
    Adds a new student to the students.txt file.
    """
    print("\n" + "-" * 40)
    print("         Add New Student Menu")
    print("-" * 40)
    
    student_id = input("Enter Student ID: ").strip()
    student_name = input("Enter Student Name: ").strip()
    student_email = input("Enter Student Email: ").strip()
    enrolled_courses = input("Enter Enrolled Courses (comma-separated): ").strip()
    total_fees = input("Enter Total Fees: ").strip()
    outstanding_fees = input("Enter Outstanding Fees: ").strip()

    ensure_file_exists('students.txt', "Student ID,Student Name,Student Email,Enrolled Courses,Total Fees,Outstanding Fees")

    students = load_file('students.txt')
    for student in students:
        if student[0] == student_id:
            print("\n" + "-" * 40)
            print(f"Error: Student with ID '{student_id}' already exists.")
            print("-" * 40)
            return

    append_to_file('students.txt', [student_id, student_name, student_email, enrolled_courses, total_fees, outstanding_fees])
    print("\n" + "-" * 40)
    print(f"Success: Student '{student_name}' has been added.")
    print("-" * 40)

def remove_student():
    """
    Removes a student from the students.txt file.
    """
    print("\n" + "-" * 40)
    print("         Remove Student Menu")
    print("-" * 40)
    
    student_id = input("Enter the Student ID to Remove: ").strip()
    students = load_file('students.txt')
    updated_students = [student for student in students if student[0] != student_id]

    if len(updated_students) == len(students):
        print("\n" + "-" * 40)
        print(f"Error: Student with ID '{student_id}' does not exist.")
        print("-" * 40)
    else:
        save_to_file('students.txt', updated_students)
        print("\n" + "-" * 40)
        print(f"Success: Student with ID '{student_id}' has been removed.")
        print("-" * 40)

def add_course():
    """
    Adds a new course to the courses.txt file.
    """
    print("\n" + "-" * 40)
    print("         Add New Course Menu")
    print("-" * 40)
    
    course_id = input("Enter Module ID (e.g., CS101): ").strip()
    course_name = input("Enter Course Name: ").strip()
    credit_hours = input("Enter Credit Hours: ").strip()
    semester = input("Enter Semester: ").strip()

    ensure_file_exists('courses.txt', "Module ID,Module Name,Credit Hours,Semester")

    courses = load_file('courses.txt')
    for course in courses:
        if course[0] == course_id:
            print("\n" + "-" * 40)
            print(f"Error: Course with ID '{course_id}' already exists.")
            print("-" * 40)
            return

    append_to_file('courses.txt', [course_id, course_name, credit_hours, semester])
    print("\n" + "-" * 40)
    print(f"Success: Course '{course_name}' has been added.")
    print("-" * 40)

def remove_course():
    """Removes a course from the courses.txt file using its ID."""
    course_id = input("Enter Course ID to Remove: ").strip()
    delete_record('courses.txt', lambda record: record[0] == course_id)

def view_all_data(file_name):
    """
    Displays all the data from a specified file.
    If the file does not exist, shows an error message.
    """
    try:
        with open(file_name, 'r') as file:
            data = [line.strip() for line in file.readlines()]
        
        if not data:
            print("\n" + "-" * 40)
            print(f"Notice: The file '{file_name}' is empty.")
            print("-" * 40)
            return
        
        print("\n" + "-" * 40)
        print(f"       Data in '{file_name}'")
        print("-" * 40)
        for line in data:
            print(line)
        print("-" * 40)
    except FileNotFoundError:
        print("\n" + "-" * 40)
        print(f"Error: The file '{file_name}' does not exist.")
        print("-" * 40)


def report_menu():
    """
    Displays the report menu for administrators, allowing selection of a specific report to generate and save to a file.
    """
    while True:
        print("\n--- Generate Reports Menu ---")
        print("1. Course Enrollment Report")
        print("2. Student Performance Report")
        print("3. Fees Collection Report")
        print("4. Outstanding Fees Report")
        print("5. Back to Administrator Menu")

        choice = input("Enter the report number to generate: ").strip()
        if choice == '1':
            course_enrollment_report()
        elif choice == '2':
            student_performance_report()
        elif choice == '3':
            fees_collection_report()
        elif choice == '4':
            outstanding_fees_report()
        elif choice == '5':
            print("Returning to Administrator Menu...")
            break
        else:
            print("Invalid choice. Please try again.")




# Report Functions

def course_enrollment_report():
    """
    Generates and saves a report showing the number of students enrolled in each course.
    Report File: course_enrollment_report.txt
    """
    students = load_file('students.txt')
    courses = load_file('courses.txt')

    # Create a dictionary to track enrollments for each course
    enrollment_count = {}
    for student in students[1:]:  # Skip header row
        enrolled_courses = student[3].split(',')  # List of courses student is enrolled in
        for course in enrolled_courses:
            course = course.strip()
            if course:  # Ignore empty course entries
                enrollment_count[course] = enrollment_count.get(course, 0) + 1

    # Generate the report
    report_lines = ["--- Course Enrollment Report ---"]
    for course in courses[1:]:  # Skip header row
        course_id = course[0]
        course_name = course[1]
        enrolled = enrollment_count.get(course_id, 0)
        report_lines.append(f"Course: {course_name} ({course_id}), Enrolled Students: {enrolled}")

    # Save the report to a file
    save_to_file('course_enrollment_report.txt', [[line] for line in report_lines])
    print("Course Enrollment Report generated and saved to 'course_enrollment_report.txt'")
def student_performance_report():
    """
    Generates and saves a performance report for each course with grade statistics.
    Report File: student_performance_report.txt
    """
    grades = load_file('grades.txt')

    # Create a dictionary to store grades per course
    course_grades = {}
    for entry in grades[1:]:  # Skip header row
        course = entry[1]
        if entry[2].replace('.', '', 1).isdigit():  # Validate grade is numeric
            grade = float(entry[2])
            course_grades.setdefault(course, []).append(grade)

    # Generate the report
    report_lines = ["--- Student Performance Report ---"]
    for course, grade_list in course_grades.items():
        if grade_list:  # Ensure the course has grades
            average_grade = sum(grade_list) / len(grade_list)
            highest_grade = max(grade_list)
            lowest_grade = min(grade_list)
            report_lines.append(f"Course: {course}")
            report_lines.append(f"  Average Grade: {average_grade:.2f}%")
            report_lines.append(f"  Highest Grade: {highest_grade:.2f}%")
            report_lines.append(f"  Lowest Grade: {lowest_grade:.2f}%")

    # Save the report to a file
    save_to_file('student_performance_report.txt', [[line] for line in report_lines])
    print("Student Performance Report generated and saved to 'student_performance_report.txt'")



def fees_collection_report():
    """
    Generates and saves a report summarizing total fees collected and outstanding fees.
    Report File: fees_collection_report.txt
    """
    students = load_file('students.txt')

    total_collected = 0
    total_outstanding = 0
    fully_paid_count = 0

    # Calculate totals while skipping invalid rows
    for student in students[1:]:  # Skip header row
        if (student[4].replace('.', '', 1).isdigit() and student[5].replace('.', '', 1).isdigit()):
            total_fees = float(student[4])
            outstanding_fees = float(student[5])
            total_collected += (total_fees - outstanding_fees)
            total_outstanding += outstanding_fees
            if outstanding_fees == 0:
                fully_paid_count += 1

    # Generate the report
    report_lines = [
        "--- Fees Collection Report ---",
        f"Total Fees Collected: MYR{total_collected:.2f}",
        f"Total Outstanding Fees: MYR{total_outstanding:.2f}",
        f"Students Fully Paid: {fully_paid_count}"
    ]

    # Save the report to a file
    save_to_file('fees_collection_report.txt', [[line] for line in report_lines])
    print("Fees Collection Report generated and saved to 'fees_collection_report.txt'")


def outstanding_fees_report():
    """
    Generates and saves a list of students with outstanding fees.
    Report File: outstanding_fees_report.txt
    """
    students = load_file('students.txt')

    # Sort students by outstanding fees in descending order
    students_with_fees = sorted(
        [
            student for student in students[1:]  # Skip header row
            if student[5].replace('.', '', 1).isdigit() and float(student[5]) > 0
        ],
        key=lambda x: float(x[5]),
        reverse=True
    )

    # Generate the report
    report_lines = ["--- Outstanding Fees Report ---"]
    for student in students_with_fees:
        student_id = student[0]
        student_name = student[1]
        outstanding_fees = float(student[5])
        report_lines.append(f"Student ID: {student_id}, Name: {student_name}, Outstanding Fees: MYR{outstanding_fees:.2f}")

    # Save the report to a file
    save_to_file('outstanding_fees_report.txt', [[line] for line in report_lines])
    print("Outstanding Fees Report generated and saved to 'outstanding_fees_report.txt'")




def delete_record(file_name, match_function):
    """Deletes records matching a condition in the file."""
    data = load_file(file_name)
    updated_data = [record for record in data if not match_function(record)]
    if len(data) == len(updated_data):
        print("No matching records found.")
    else:
        save_to_file(file_name, updated_data)
        print("Record(s) deleted successfully!")




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
# # Dictionary to store student data
students = {}

# Function to register a new student
def register_student(student_id, first_name, last_name, course_enrolled):
    """Registers a new student by adding their details to the students dictionary."""
    if student_id in students:
        return f"Error: A student with ID {student_id} already exists."
    students[student_id] = {
        "first_name": first_name,
        "last_name": last_name,
        "course_enrolled": course_enrolled,
        "transcript": []
    }
    return f"Student {first_name} {last_name} registered successfully with ID {student_id}."

# Function to view student information
def view_student(student_id):
    """Displays the details of a student based on their ID."""
    if student_id not in students:
        return f"Error: Student with ID {student_id} not found."
    student = students[student_id]
    return (f"Student ID: {student_id}\n"
            f"Name: {student['first_name']} {student['last_name']}\n"
            f"Course Enrolled: {student['course_enrolled']}")

# Function to update student information
def update_student(student_id, first_name=None, last_name=None, course_enrolled=None):
    """Updates the personal details or enrolled course of an existing student."""
    if student_id not in students:
        return f"Error: Student with ID {student_id} not found."
    if first_name:
        students[student_id]["first_name"] = first_name
    if last_name:
        students[student_id]["last_name"] = last_name
    if course_enrolled:
        students[student_id]["course_enrolled"] = course_enrolled
    return f"Student {student_id}'s record updated successfully."

# Function to manage course enrollment
def manage_enrollment(student_id, new_course):
    """Manages a student's enrollment by enrolling in or withdrawing from a course."""
    if student_id not in students:
        return f"Error: Student with ID {student_id} not found."
    if new_course.strip() == "":
        students[student_id]["course_enrolled"] = None
        return f"{students[student_id]['first_name']} {students[student_id]['last_name']} has been withdrawn from all courses."
    students[student_id]["course_enrolled"] = new_course
    return f"{students[student_id]['first_name']} {students[student_id]['last_name']} has been enrolled in the course: {new_course}."

# Function to issue a transcript
def issue_transcript(student_id):
    """Generates a transcript entry for the student and appends it to their record."""
    if student_id not in students:
        return f"Error: Student with ID {student_id} not found."
    student = students[student_id]
    transcript_entry = f"Transcript: {student['first_name']} {student['last_name']} is enrolled in {student['course_enrolled']}."
    student["transcript"].append(transcript_entry)
    return transcript_entry

# Function to generate a report of all students
def generate_report():
    """Creates a report listing all students and their details."""
    if not students:
        return "No students registered in the system."
    report = "Student Report:\n"
    for student_id, student in students.items():
        report += (f"Student ID: {student_id}, "
                   f"Name: {student['first_name']} {student['last_name']}, "
                   f"Course: {student['course_enrolled']}\n")
    return report

# Main function to run the system
def registrar_menu():
    print("Welcome to the Registrar system!")
    
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
            student_id = input("Enter student ID: ").strip()
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            course_enrolled = input("Enter the course to enroll in: ").strip()
            print(register_student(student_id, first_name, last_name, course_enrolled))
        
        elif choice == "2":  # View student information
            student_id = input("Enter student ID: ").strip()
            print(view_student(student_id))
        
        elif choice == "3":  # Update student details
            student_id = input("Enter student ID: ").strip()
            first_name = input("Enter new first name (or press Enter to skip): ").strip()
            last_name = input("Enter new last name (or press Enter to skip): ").strip()
            course_enrolled = input("Enter new course (or press Enter to skip): ").strip()
            print(update_student(student_id, first_name or None, last_name or None, course_enrolled or None))
        
        elif choice == "4":  # Manage course enrollment
            student_id = input("Enter student ID: ").strip()
            new_course = input("Enter new course (or leave blank to withdraw): ").strip()
            print(manage_enrollment(student_id, new_course))
        
        elif choice == "5":  # Issue a transcript
            student_id = input("Enter student ID: ").strip()
            print(issue_transcript(student_id))
        
        elif choice == "6":  # Generate a report
            print(generate_report())
        
        elif choice == "7":  # Exit
            print("Exiting the system. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

#--------------------------------------- Main program entry point--------------------------------------------------
users = load_users()
login(users)