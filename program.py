#University Management System
#-------------------------------------------------------------------------------Common Functions------------------------------------------------------------------------------

# Constants for file paths
STUDENTS_FILE = "students.txt"
COURSES_FILE = "courses.txt"
LECTURERS_FILE = "lecturers.txt"
ATTENDANCE_FILE = "attendance.txt"
GRADES_FILE = "grades.txt"
USERS_FILE = "users.txt"
RECEIPTS_FILE = "receipts.txt"

# Function to read data from a file that returns a list of lists
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Skip the header
            next(file)
            data = []
            for line in file:
                # read each line and split it into a list and append it to the data list
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

# Function to append data to a file
def append_file(file_path, data):
    try:
        with open(file_path, 'a') as file:
            file.writelines(data)
    except Exception as e:
        print(f"Error appending to {file_path}: {e}")

# Function to get student details and return it in a dictionary
def get_student_details(student_id):

    #iterating over each line in the students file
    for line in read_file(STUDENTS_FILE):
        if len(line) >= 6:
            s_id, name, email, enrolled_courses, total_fees, outstanding_fees = line

            # Check if the student ID matches
            if s_id == student_id:

                # Return the student details
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

# Function to update student fees after payment
def update_student_fees(student_id, payment_amount):
    students = read_file(STUDENTS_FILE)

    new_students = ["StudentID,Name,Email,EnrolledCourses,TotalFees,OutstandingFees\n"]
    updated = False
    
    for student in students:
        # Checking if the student ID matches
        if len(student) >= 6 and student[0] == student_id:
            outstanding = float(student[5]) - payment_amount
            
            # Update the outstanding fees
            new_line = f"{student[0]},{student[1]},{student[2]},{student[3]},{student[4]},{outstanding}\n"
            new_students.append(new_line)
            updated = True
        else:
            new_students.append(','.join(student) + '\n')
    
    if updated:
        write_file(STUDENTS_FILE, new_students)
        
        # Record receipt
        receipt_id = f"R{len(read_file(RECEIPTS_FILE)) + 1:04d}"
        date = get_date()
        receipt_entry = f"{receipt_id},{student_id},{payment_amount},{date}\n"
        append_file(RECEIPTS_FILE, [receipt_entry])
        
        return True
    return False

# Function to get list of students enrolled in a course and return them in a list
def get_enrolled_students(course_code):

    students = []
    for line in read_file(STUDENTS_FILE):
        if len(line) >= 6: 
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

# Function to get date
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

# Function to load users and return them in a dictionary
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

# Function to authenticate user and redirect them to their respective menu
def authenticate(email, password, users):
    if not email or not password:
        print("Email and password cannot be empty")
        return
    if email in users:
        if users[email]['password'] == password:
            role = users[email]['role']
            print(f"\nLogin successful! ")
            while True:
                if role == 'student':
                    student_menu(email)
                    break
                elif role == 'lecturer':
                    lecturer_menu(email)
                    break
                elif role == 'admin':
                    admin_menu(email)
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

# Function to display login menu
def login(users):
    print("\n---------- Login ----------")
    while True:
        email = input("Enter email: ").strip()

        # Email validation
        if not email:
            print("Email cannot be empty")
            continue
        if '@' not in email or '.' not in email:
            print("Please enter a valid email address")
            continue
        break
    
    password = input("Enter password: ").strip()
    authenticate(email, password, users)

#-------------------------------------------------------------LECTURER MENU--------------------------------------------------------------------------------------

# Function to get course details for multiple course codes
def get_courses(course_codes):
    if not course_codes:
        return []
      
    codes = course_codes.strip().split()

    all_courses = read_file(COURSES_FILE)
    
    courses_list = []
    for code in codes:
        for course in all_courses:
            if course[0] == code:
                courses_list.append(course)
                break

    # Returning as tuple for faster access and immutable
    courses = tuple(courses_list)
    return courses

# Function to select a module from lecturer's assigned courses
def select_module(lecturer_id):
    for line in read_file(LECTURERS_FILE):
        l_id, _, _, course_code = line
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

# Function to get all grades in a specific module
def get_module_grades(course_code):
    grades = []
    # Iterating through the grades file
    for line in read_file(GRADES_FILE):
        if len(line) < 4:
            continue
        student_id, module, marks, grade_letter = line
        # Checking if the module ID matches
        if module == course_code:
            grades.append({
                'student_id': student_id,
                'marks': marks,
                'grade_letter': grade_letter
            })
    return grades

# Function to calculate letter grade from numerical marks
def calculate_grade(marks):
    #nested if statements to assign letter grade
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

# Function to update grade for a specific student
def update_grade(student_id, course_code, marks, grade_letter):
    grades = read_file(GRADES_FILE)
    updated = False
    new_grades = []
    
    # Header for new file if it's empty
    if not grades:
        new_grades.append("StudentID,ModuleCode,Marks,Grade\n")
    
    for grade in grades:
        if grade[0] == student_id and grade[1] == course_code:
            # Updating existing record
            new_grades.append(f"{student_id},{course_code},{marks:.1f},{grade_letter}\n")
            updated = True
        else:
            new_grades.append(','.join(grade) + '\n')
    
    if not updated:
        new_grades.append(f"{student_id},{course_code},{marks:.1f},{grade_letter}\n")
    
    write_file(GRADES_FILE, new_grades)
    print(f"\nGrade updated for student {student_id}")
    input("Press Enter to continue...")

# Function to record attendance
def record_attendance(date, course_code, student_id, status):

    attendance_entry = f"{course_code},{student_id},{date},{status}\n"
    
    # Reading attendance file to check for duplicates
    attendances = read_file(ATTENDANCE_FILE)
    for attendance in attendances:
        if (attendance[0] == course_code and 
            attendance[1] == student_id and 
            attendance[2] == date):
            print("\nAttendance already recorded for this date")
            input("Press Enter to continue...")
            return
    
    # Adding new attendance entry to the file
    append_file(ATTENDANCE_FILE, [attendance_entry])
    print(f"\nAttendance recorded for student {student_id}")


# Function to display the main lecturer menu
def lecturer_menu(email):
    # Iterating through lecturers file
    for line in read_file(LECTURERS_FILE):
        # Checking if email matches
        l_id, l_name, l_email, _ = line
        if l_email == email:
            break

    while True:
        # Displaying lecturer menu with personal details (Lecturer's Name)
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
        
        # Handling user's choice
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

# Function to view assigned modules for the lecturer
def view_assigned_modules(lecturer_id):
    for line in read_file(LECTURERS_FILE):
        l_id, l_name, _, course_code = line

        # Checking if lecturer ID matches
        if l_id == lecturer_id:
            courses = get_courses(course_code)
            
            # Displaying assigned modules with headers
            print(f"\n================ Assigned Modules for {l_name} ==================")
            print(f"Course Code".ljust(15) + "Course Name".ljust(25) + "Credit Hours".ljust(15) + "Semester")
            print("-" * 70)
            for course in courses:
                print(course[0].ljust(15) + course[1].ljust(25) + "    "+course[2].ljust(15) + course[3])
            print("-" * 70)
            input("Press Enter to continue...")
            return

# Function to record and update grades
def record_grades(lecturer_id):

    # Selecting module
    module = select_module(lecturer_id)
    if not module:
        return

    students = get_enrolled_students(module['course_code'])
    if not students:
        print("\nNo students enrolled in this module.")
        input("Press Enter to continue...")
        return
    
    # Displaying headers
    print(f"\n===== Record Grades for {module['course_code']} =====\n")
    print("-"*55)
    print(f"Student ID".ljust(15) + "Name".ljust(25) + "Current Grade")
    print("-" * 55)
    
    current_grades = get_module_grades(module['course_code'])
    grades_dict = {grade['student_id']: grade['marks'] for grade in current_grades}
    
    for student in students:

        # Displaying current grades for each student
        current_grade = grades_dict.get(student['id'], 'Not graded')
        print(student['id'].ljust(15) + student['name'].ljust(25) + current_grade)
    
    print("\nEnter new grades (0-100) or press Enter to skip:")
    for student in students:
        while True:
            grade_input = input(f"\nGrade for {student['name']} ({student['id']}): ").strip()
            
            if not grade_input:
                # If no input, skip to the next student
                break
            try:
                marks = float(grade_input)
                #Validating marks
                if 0 <= marks <= 100:
                    grade_letter = calculate_grade(marks)
                    
                    #Updating grade
                    update_grade(student['id'], module['course_code'], marks, grade_letter)
                    break
                else:
                    print("Marks must be between 0 and 100")
            except ValueError:
                print("Please enter a valid number")

# Function to view student list
def view_student_list(lecturer_id):
    
    # Selecting a module
    module = select_module(lecturer_id)
    if not module:
        return
    
    students = get_enrolled_students(module['course_code'])
    if not students:
        print("\nNo students enrolled in this module.")
        input("Press Enter to continue...")
        return
    
    # Displaying headers
    print(f"\n=== Student List for {module['course_code']} ===")
    print(f"ID".ljust(10) + "Name".ljust(25)+"Email")
    print("-" * 60)
    
    for student in students:

        # Displaying students' details
        print(student['id'].ljust(10) + student['name'].ljust(25)+student['email'])
    print("-" * 60)
    input("Press Enter to continue...")


# Function to track attendance
def track_attendance(lecturer_id):

    # Selecting a module
    module = select_module(lecturer_id)
    if not module:
        return
        
    students = get_enrolled_students(module['course_code'])
    if not students:
        print("\nNo students enrolled in this module.")
        input("Press Enter to continue...")
        return
    
    date = get_date()
    
    # Displaying headers
    print(f"\n=== Mark Attendance for {module['course_code']} ===")
    print(f"Date: {date}")
    print("\nMark attendance: (P)resent, (A)bsent, (L)ate")
    
    for student in students:
        while True:

            # Taking attendance
            status = input(f"{student['name']} ({student['id']}): ").upper()

            # Validating input
            if status in ['P', 'A', 'L']:
                full_status = {'P': 'Present', 'A': 'Absent', 'L': 'Late'}[status]

                # Recording attendance
                record_attendance(date, module['course_code'], student['id'], full_status)
                break
            else:
                print("Invalid input. Please use P, A, or L.")
        print("-" * 60)
    print("Attendance updated for module:", module['course_code'])
    input("Press Enter to continue...")

# Function to view student grades
def view_student_grades(lecturer_id):

    # Selecting a module
    module = select_module(lecturer_id)
    if not module:
        return
        
    grades = get_module_grades(module['course_code'])
    if not grades:
        print("\nNo grades recorded for this module.")
        input("Press Enter to continue...")
        return
        
    # Displaying headers
    print(f"\n============== Grade Report for {module['course_code']} ================")
    print(f"ID".ljust(10)+"Name".ljust(25)+"Marks".ljust(10)+"Grade")
    print("-" * 55)
    
    for grade in grades:
        student = get_student_details(grade['student_id'])
        if student:

            # Displaying grades if student details are available
            print(student['id'].ljust(10)+student['name'].ljust(25)+grade['marks'].ljust(10)+grade['grade_letter'])
    
    # Calculate and display statistics from all marks
    marks = [float(grade['marks']) for grade in grades]
    
    if marks:
        avg = sum(marks) / len(marks)
        highest = max(marks)
        lowest = min(marks)
    else:
        avg = highest = lowest = 0
    
    print("-" * 55)
    print(f"Class Average: {avg:.2f}")
    print(f"Highest Mark: {highest}")
    print(f"Lowest Mark: {lowest}")
    print("-" * 55)
    input("Press Enter to continue...")

#---------------------------------------------------ACCOUNTANT MENU--------------------------------------------------------------------------------
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

#-------------------------------------------ADMINISTRATOR MENU----------------------------------------------------------------------------------

# Common File Handling Functions
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
    Appends a single record to a file with proper formatting.
    Args:
        file_name (str): The name of the file to append to.
        record (list): A list of values representing a single record.
    """
    try:
        with open(file_name, 'a') as file:
            file.write(', '.join(record) + '\n')  # Properly formatted with commas and line breaks
    except Exception as e:
        print(f"\nError: Could not append to {file_name}. Reason: {e}")


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
        print("6. Manage Lecturers")
        print("7. Generate Reports")
        print("8. Exit")
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
            view_all_data()
        elif choice == '6':
            manage_lecturers()
        elif choice == '7':
            generate_reports()  # Updated call
        elif choice == '8':
            print("\nExiting Administrator Menu...")
            break
        else:
            print("\nInvalid choice. Please try again.")


def add_student():
    """
    Adds a new student to the students.txt file and registers them in users.txt.
    Student ID is assigned automatically.
    """
    print("\n" + "-" * 40)
    print("         Add New Student Menu")
    print("-" * 40)

    # Input student details
    student_name = input("Enter Student Name: ").strip()
    student_email = input("Enter Student Email: ").strip()
    enrolled_courses = input("Enter Enrolled Courses (comma-separated): ").strip()
    total_fees = input("Enter Total Fees: ").strip()
    outstanding_fees = input("Enter Outstanding Fees: ").strip()

    # Ensure the files exist
    ensure_file_exists('students.txt', "Student ID,Student Name,Student Email,Enrolled Courses,Total Fees,Outstanding Fees")
    ensure_file_exists('users.txt', "Email,Password,Role")

    # Load existing students to determine the next Student ID
    students = load_file('students.txt')
    if len(students) > 1:
        last_id = students[-1][0]  # Get the last student ID
        next_id = "S" + str(int(last_id[1:]) + 1)  # Increment numeric part of the ID
    else:
        next_id = "S001"  # Default ID if the file is empty

    # Append the new student to students.txt
    append_to_file('students.txt', [next_id, student_name, student_email, enrolled_courses, total_fees, outstanding_fees])

    # Add the student to users.txt with a default password and "Student" role
    default_password = "password123"
    append_to_file('users.txt', [student_email, default_password, "Student"])

    # Confirmation message
    print("\n" + "-" * 40)
    print(f"Success: Student '{student_name}' has been added with ID '{next_id}' and registered as a user.")
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
    Adds a new course to the courses.txt file with an automatically assigned ID.
    """
    print("\n" + "-" * 40)
    print("         Add New Course Menu")
    print("-" * 40)

    # Input course details
    course_name = input("Enter Course Name: ").strip()
    credit_hours = input("Enter Credit Hours: ").strip()
    semester = input("Enter Semester: ").strip()

    # Ensure the file exists
    ensure_file_exists('courses.txt', "Module ID,Module Name,Credit Hours,Semester")

    # Load existing courses to determine the next Course ID
    courses = load_file('courses.txt')
    if len(courses) > 1:
        last_id = courses[-1][0]  # Get the last course ID
        numeric_part = int(last_id[2:]) + 1  # Increment numeric part of the ID
        next_id = f"CS{numeric_part:03d}"  # Format as CS001, CS002, etc.
    else:
        next_id = "CS001"  # Default ID if the file is empty

    # Append the new course to the file
    append_to_file('courses.txt', [next_id, course_name, credit_hours, semester])
    print("\n" + "-" * 40)
    print(f"Success: Course '{course_name}' has been added with ID '{next_id}'.")
    print("-" * 40)


def remove_course():
    """Removes a course from the courses.txt file using its ID."""
    course_id = input("Enter Course ID to Remove: ").strip()
    delete_record('courses.txt', lambda record: record[0] == course_id)

def manage_lecturers():
    """
    Manage lecturer records, allowing addition, removal, or updating of lecturers.
    Data is stored in lecturers.txt with the format:
    Lecturer ID, Lecturer Email, List of Modules
    """
    while True:
        print("\n" + "-" * 40)
        print("         Manage Lecturers Menu")
        print("-" * 40)
        print("1. Add Lecturer")
        print("2. Remove Lecturer")
        print("3. Update Lecturer Information")
        print("4. Back to Administrator Menu")
        print("-" * 40)

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_lecturer()
        elif choice == '2':
            remove_lecturer()
        elif choice == '3':
            update_lecturer()
        elif choice == '4':
            print("\nReturning to Administrator Menu...")
            break
        else:
            print("\nInvalid choice. Please try again.")


def add_lecturer():
    """
    Adds a new lecturer to the lecturers.txt file.
    Ensures Lecturer ID is unique before appending.
    """
    print("\n" + "-" * 40)
    print("         Add New Lecturer")
    print("-" * 40)

    lecturer_id = input("Enter Lecturer ID: ").strip()
    lecturer_email = input("Enter Lecturer Email: ").strip()
    modules = input("Enter List of Modules (comma-separated): ").strip()

    # Ensure the file exists
    ensure_file_exists('lecturers.txt', "Lecturer ID,Lecturer Email,List of Modules")

    # Check for duplicate Lecturer ID
    lecturers = load_file('lecturers.txt')
    for lecturer in lecturers:
        if lecturer[0] == lecturer_id:
            print("\n" + "-" * 40)
            print(f"Error: A lecturer with ID '{lecturer_id}' already exists.")
            print("-" * 40)
            return

    # Append the new lecturer
    append_to_file('lecturers.txt', [lecturer_id, lecturer_email, modules])
    print("\n" + "-" * 40)
    print(f"Success: Lecturer '{lecturer_id}' has been added.")
    print("-" * 40)
 
def remove_lecturer():
    """
    Removes a lecturer from the lecturers.txt file.
    """
    print("\n" + "-" * 40)
    print("         Remove Lecturer")
    print("-" * 40)

    lecturer_id = input("Enter Lecturer ID to Remove: ").strip()

    # Load lecturers and filter out the one to remove
    lecturers = load_file('lecturers.txt')
    updated_lecturers = [lecturer for lecturer in lecturers if lecturer[0] != lecturer_id]

    if len(updated_lecturers) == len(lecturers):
        print("\n" + "-" * 40)
        print(f"Error: Lecturer with ID '{lecturer_id}' does not exist.")
        print("-" * 40)
    else:
        save_to_file('lecturers.txt', updated_lecturers)
        print("\n" + "-" * 40)
        print(f"Success: Lecturer with ID '{lecturer_id}' has been removed.")
        print("-" * 40)



def update_lecturer():
    """
    Updates information for an existing lecturer in the lecturers.txt file.
    Allows changes to email or list of modules.
    """
    print("\n" + "-" * 40)
    print("         Update Lecturer")
    print("-" * 40)

    lecturer_id = input("Enter Lecturer ID to Update: ").strip()

    # Load lecturers
    lecturers = load_file('lecturers.txt')
    for lecturer in lecturers:
        if lecturer[0] == lecturer_id:
            print(f"\nFound Lecturer: {lecturer}")
            new_email = input("Enter New Lecturer Email (leave blank to keep unchanged): ").strip()
            new_modules = input("Enter New List of Modules (comma-separated, leave blank to keep unchanged): ").strip()

            # Update the lecturer's information
            if new_email:
                lecturer[1] = new_email
            if new_modules:
                lecturer[2] = new_modules

            # Save the updated list back to the file
            save_to_file('lecturers.txt', lecturers)
            print("\n" + "-" * 40)
            print(f"Success: Lecturer '{lecturer_id}' has been updated.")
            print("-" * 40)
            return

    print("\n" + "-" * 40)
    print(f"Error: Lecturer with ID '{lecturer_id}' not found.")
    print("-" * 40)

def view_all_data():
    """
    Displays the content of all relevant data files on the screen.
    """
    files = [
        "students.txt",
        "courses.txt",
        "lecturers.txt",
        "grades.txt",
        "attendance.txt",
        "users.txt",
        "receipts.txt"
    ]

    print("\n" + "-" * 40)
    print("         View All Data")
    print("-" * 40)

    for file_name in files:
        print(f"\n--- Data in {file_name} ---")
        try:
            with open(file_name, 'r') as file:
                data = [line.strip() for line in file.readlines()]
            
            if data:
                for line in data:
                    print(line)
            else:
                print("The file is empty.")
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist.")
        print("-" * 40)


# Report Functions

def generate_reports():
    """
    Displays a menu to generate specific reports:
    1. Total Students
    2. Total Active Courses
    3. Total Faculty
    """
    while True:
        print("\n" + "-" * 40)
        print("         Generate Reports Menu")
        print("-" * 40)
        print("1. Total Students Report")
        print("2. Total Active Courses Report")
        print("3. Total Faculty Report")
        print("4. Back to Administrator Menu")
        print("-" * 40)

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            total_students_report()
        elif choice == '2':
            total_active_courses_report()
        elif choice == '3':
            total_faculty_report()
        elif choice == '4':
            print("\nReturning to Administrator Menu...")
            break
        else:
            print("\nInvalid choice. Please try again.")


def total_students_report():
    """
    Generates and displays the total number of students.
    """
    students = load_file('students.txt')
    total_students = len(students[1:])  # Exclude header row
    print("\n" + "-" * 40)
    print("         Total Students Report")
    print("-" * 40)
    print(f"Total Students: {total_students}")
    print("-" * 40)

def total_active_courses_report():
    """
    Generates and displays the total number of active courses.
    """
    courses = load_file('courses.txt')
    total_courses = len(courses[1:])  # Exclude header row
    print("\n" + "-" * 40)
    print("      Total Active Courses Report")
    print("-" * 40)
    print(f"Total Active Courses: {total_courses}")
    print("-" * 40)

def total_faculty_report():
    """
    Generates and displays the total number of faculty members.
    """
    faculty = load_file('lecturers.txt')
    total_faculty = len(faculty[1:])  # Exclude header row
    print("\n" + "-" * 40)
    print("         Total Faculty Report")
    print("-" * 40)
    print(f"Total Faculty: {total_faculty}")
    print("-" * 40)



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



admin_menu("admin@example.com")

#----------------------------------------------------STUDENT MENU-------------------------------------------------------------------------------
# Constants for file paths and valid status values remain the same...

def view_available_modules(semester=None):
    """
    Display all available modules with filtering by semester if specified
    Returns list of available courses for reuse in other functions
    """
    courses = read_file(COURSES_FILE)
    if not courses:
        print("\nNo courses available.")
        return []
    
    filtered_courses = courses
    if semester:
        filtered_courses = [c for c in courses if c[3] == semester]
        
    print("\n========== Available Modules ==========")
    print(f"{'Course Code'.ljust(15)}{'Course Name'.ljust(35)}{'Credit Hours'.ljust(15)}{'Semester'}")
    print("=" * 75)
    
    for course in filtered_courses:
        print(f"{course[0].ljust(15)}{course[1].ljust(35)}{course[2].ljust(15)}{course[3]}")
    print("=" * 75)
    return filtered_courses

def view_grades(student_id):
    """
    Display student's grades with additional statistics
    - Shows both percentage and letter grades
    - Calculates GPA and overall performance
    """
    grades = read_file(GRADES_FILE)
    student_grades = [g for g in grades if g[0] == student_id]
    
    if not student_grades:
        print("\nNo grades available.")
        return
    
    print("\n=============== Academic Record ===============")
    print(f"{'Module'.ljust(15)}{'Grade %'.ljust(15)}{'Letter'.ljust(15)}{'Status'}")
    print("=" * 50)
    
    total_percentage = 0
    passed_modules = 0
    
    for grade in student_grades:
        percentage = float(grade[2])
        letter_grade = grade[3]
        status = "Pass" if percentage >= 50 else "Fail"
        
        print(f"{grade[1].ljust(15)}{str(percentage).ljust(15)}{letter_grade.ljust(15)}{status}")
        
        total_percentage += percentage
        if status == "Pass":
            passed_modules += 1
    
    if student_grades:
        average = total_percentage / len(student_grades)
        print("\n============== Performance Summary ==============")
        print(f"Average Grade     : {average:.1f}%")
        print(f"Modules Passed    : {passed_modules}/{len(student_grades)}")
        print(f"Success Rate      : {(passed_modules/len(student_grades))*100:.1f}%")
        print("=" * 45)

def view_attendance(student_id):
    """
    Display student's attendance records with statistics
    """
    attendance = read_file(ATTENDANCE_FILE)
    student_attendance = [a for a in attendance if a[1] == student_id]
    
    if not student_attendance:
        print("\nNo attendance records found.")
        return
    
    course_attendance = {}
    for record in student_attendance:
        course = record[0]
        status = record[3]
        
        if course not in course_attendance:
            course_attendance[course] = {'total': 0, 'present': 0}
        
        course_attendance[course]['total'] += 1
        if status == 'Present':
            course_attendance[course]['present'] += 1
    
    print("\n=============== Attendance Summary ===============")
    print(f"{'Course'.ljust(15)}{'Present'.ljust(10)}{'Total'.ljust(10)}{'Percentage'}")
    print("=" * 50)
    
    for course, stats in course_attendance.items():
        percentage = (stats['present'] / stats['total']) * 100
        print(f"{course.ljust(15)}{str(stats['present']).ljust(10)}{str(stats['total']).ljust(10)}{f'{percentage:.1f}%'}")
    print("=" * 50)

def manage_profile(student_id):
    """
    Allow students to view and update their profile information
    """
    student = get_student_details(student_id)
    if not student:
        print("\nError: Student record not found.")
        return False
    
    print("\n============== Current Profile ==============")
    print(f"Student ID       : {student['id']}")
    print(f"Name            : {student['name']}")
    print(f"Email           : {student['email']}")
    print(f"Enrolled Courses: {student['enrolled_courses']}")
    print(f"Total Fees      : ${student['total_fees']:.2f}")
    print(f"Outstanding Fees : ${student['outstanding_fees']:.2f}")
    print("=" * 45)
    
    while True:
        print("\n============ Update Options ============")
        print("|    1. Update Name                  |")
        print("|    2. Update Email                 |")
        print("|    3. Return to Menu               |")
        print("======================================")
        
        choice = input("\nEnter choice: ").strip()
        if choice == "3":
            break
            
        # Rest of the profile management code remains the same...

# Program mappings
PROGRAM_MAPPINGS = {
    'CS': 'Computer Science',
    'ENG': 'Engineering',
    'BUS': 'Business Administration'
}

def get_student_program(student_id):
    """
    Get student's program from their ID
    Handles CS (Computer Science), ENG (Engineering), and BUS (Business) prefixes
    """
    students = read_file(STUDENTS_FILE)
    student = next((s for s in students if s[0] == student_id), None)
    if not student:
        return None
        
    # Extract program code from student ID
    if student_id.startswith('CS'):
        return 'CS'
    elif student_id.startswith('ENG'):
        return 'ENG'
    elif student_id.startswith('BUS'):
        return 'BUS'
    return None

def view_program_modules(program_code, semester=None):
    """
    Display modules available for a specific program
    Handles proper program names and filtering
    """
    courses = read_file(COURSES_FILE)
    if not courses:
        print("\nNo courses available.")
        return []
    
    # Filter courses by program code
    program_courses = [c for c in courses if c[0].startswith(program_code)]
    
    if semester:
        program_courses = [c for c in program_courses if c[3] == semester]
        
    if not program_courses:
        program_name = PROGRAM_MAPPINGS.get(program_code, program_code)
        print(f"\nNo modules available for {program_name}.")
        return []
    
    program_name = PROGRAM_MAPPINGS.get(program_code, program_code)
    print(f"\n========== {program_name} Modules ==========")
    print(f"{'Course Code'.ljust(15)}{'Course Name'.ljust(35)}{'Credit Hours'.ljust(15)}{'Semester'}")
    print("=" * 75)
    
    for course in program_courses:
        print(f"{course[0].ljust(15)}{course[1].ljust(35)}{course[2].ljust(15)}{course[3]}")
    print("=" * 75)
    
    return program_courses

def enroll_in_module(student_id):
    """
    Allow student to enroll in available modules for their program
    Now with proper program name display and validation
    """
    # Get student's program
    program_code = get_student_program(student_id)
    if not program_code:
        print("\nError: Could not determine your program.")
        return False
    
    program_name = PROGRAM_MAPPINGS.get(program_code, program_code)
    print(f"\n===== {program_name} Module Enrollment =====")
        
    # Get available courses for the program
    available_courses = view_program_modules(program_code)
    if not available_courses:
        return False
        
    student = get_student_details(student_id)
    if not student:
        print("\nError: Student record not found.")
        return False
        
    # Get current enrollments
    enrolled_courses = student['enrolled_courses'].split(';') if student['enrolled_courses'] else []
    
    print("\n============= Enrollment Process =============")
    while True:
        course_id = input("\nEnter Module ID to enroll (or 'x' to cancel): ").strip().upper()
        if course_id.lower() == 'x':
            return False
            
        # Validate course selection
        selected_course = next((c for c in available_courses if c[0] == course_id), None)
        if not selected_course:
            print("Invalid Module ID. Please try again.")
            continue
            
        if course_id in enrolled_courses:
            print("You are already enrolled in this module.")
            continue
            
        break
    
    # Update student's enrolled courses
    enrolled_courses.append(course_id)
    students = read_file(STUDENTS_FILE)
    updated_students = ["StudentID,Name,Email,EnrolledCourses,TotalFees,OutstandingFees\n"]
    
    for student_record in students:
        if student_record[0] == student_id:
            # Update enrollment and adjust fees
            credit_hours = float(selected_course[2])
            fee_per_credit = 100  # Assuming $100 per credit hour
            additional_fee = credit_hours * fee_per_credit
            
            new_total = float(student_record[4]) + additional_fee
            new_outstanding = float(student_record[5]) + additional_fee
            
            new_line = (f"{student_record[0]},{student_record[1]},{student_record[2]},"
                       f"{';'.join(enrolled_courses)},{new_total},{new_outstanding}\n")
            updated_students.append(new_line)
        else:
            updated_students.append(','.join(student_record) + '\n')
    
    write_file(STUDENTS_FILE, updated_students)
    
    print("\n=========== Enrollment Successful ===========")
    print(f"Program        : {program_name}")
    print(f"Module         : {selected_course[1]}")
    print(f"Credit Hours   : {selected_course[2]}")
    print(f"Additional Fee : ${additional_fee:.2f}")
    print("===========================================")
    
    return True

def manage_profile(student_id):
    """
    Display and manage student profile with program information
    """
    student = get_student_details(student_id)
    if not student:
        print("\nError: Student record not found.")
        return False
    
    program_code = get_student_program(student_id)
    program_name = PROGRAM_MAPPINGS.get(program_code, program_code)
    
    print("\n============== Current Profile ==============")
    print(f"Student ID       : {student['id']}")
    print(f"Program         : {program_name}")
    print(f"Name            : {student['name']}")
    print(f"Email           : {student['email']}")
    print(f"Enrolled Courses: {student['enrolled_courses']}")
    print(f"Total Fees      : ${student['total_fees']:.2f}")
    print(f"Outstanding Fees : ${student['outstanding_fees']:.2f}")
    print("=" * 45)
    
    # Rest of manage_profile function remains the same...

def student_menu(email):
    """
    Main menu for student functionality
    """
    students = read_file(STUDENTS_FILE)
    student = next((s for s in students if s[2] == email), None)
    
    if not student:
        print("Error: Student record not found.")
        return
    
    student_id = student[0]
    student_name = student[1]
    
    while True:
        print(f"\n===== Welcome {student_name.ljust(15)} =====")
        print("|    1. View Available Modules        |")
        print("|    2. Enroll in Module              |")
        print("|    3. View Grades                   |")
        print("|    4. View Attendance               |")
        print("|    5. Manage Profile                |")
        print("|    6. Logout                        |")
        print("=======================================")
        
        choice = input("\nEnter your choice: ")
        print("===============================")
        
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
            print("\nLogging out... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
#---------------------------------------------------REGISTRAR MENU-----------------------------------------------------------------------------------

# Function to register a new student
def register_student():
    print("\n--- Register New Student ---")
    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    email = input("Enter Student Email: ")
    password = input("Enter Password: ")
    enrolled_courses = input("Enter Enrolled Courses (comma-separated): ")
    total_fees = input("Enter Total Fees: ")
    outstanding_fees = total_fees  # At registration, outstanding fees equals total fees

    # Append to students.txt
    new_student = f"{student_id},{name},{email},{enrolled_courses},{total_fees},{outstanding_fees}\n"
    append_file(STUDENTS_FILE, [new_student])

    # Append to users.txt for authentication
    new_user = f"{email},{password},student\n"
    append_file(USERS_FILE, [new_user])

    print("Student registered successfully!")

# Function to update student records
def update_student():
    print("\n--- Update Student Records ---")
    student_id = input("Enter Student ID to update: ")
    students = read_file(STUDENTS_FILE)

    updated_students = ["StudentID,Name,Email,EnrolledCourses,TotalFees,OutstandingFees\n"]
    updated = False

    for student in students:
        if student[0] == student_id:
            print(f"Current Details: {student}")
            email = input(f"Enter New Email (or press Enter to keep {student[2]}): ") or student[2]
            enrolled_courses = input(f"Enter New Program/Courses (or press Enter to keep {student[3]}): ") or student[3]
            updated_student = f"{student_id},{student[1]},{email},{enrolled_courses},{student[4]},{student[5]}\n"
            updated_students.append(updated_student)
            updated = True
        else:
            updated_students.append(','.join(student) + '\n')

    if updated:
        write_file(STUDENTS_FILE, updated_students)
        print("Student record updated successfully!")
    else:
        print("Student not found.")

# Function to manage enrollments
def manage_enrollments():
    print("\n--- Manage Enrollments ---")
    students = read_file(STUDENTS_FILE)
    courses = read_file(COURSES_FILE)

    print("Available Courses:")
    for course in courses:
        print(f"{course[0]}: {course[1]} ({course[2]} Credits, Semester {course[3]})")

    student_id = input("Enter Student ID: ")

    updated_students = ["StudentID,Name,Email,EnrolledCourses,TotalFees,OutstandingFees\n"]
    updated = False

    for student in students:
        if student[0] == student_id:
            print(f"Current Enrolled Courses: {student[3]}")
            print("Enter course codes to enroll, separated by commas.")
            new_courses = input("Updated Courses: ")

            # Validate course codes
            valid_courses = [course[0] for course in courses]
            new_courses_list = new_courses.split(',')
            invalid_courses = [course for course in new_courses_list if course not in valid_courses]

            if invalid_courses:
                print(f"Invalid course codes: {', '.join(invalid_courses)}")
            else:
                student[3] = new_courses
                updated_students.append(','.join(student) + '\n')
                updated = True
        else:
            updated_students.append(','.join(student) + '\n')

    if updated:
        write_file(STUDENTS_FILE, updated_students)
        print("Enrollments updated successfully!")
    else:
        print("Student not found.")

# Function to issue transcripts
def issue_transcript():
    print("\n--- Issue Transcript ---")
    student_id = input("Enter Student ID: ")
    grades = read_file(GRADES_FILE)

    print(f"\nTranscript for Student ID: {student_id}")
    print("Module Grade Percentage Grade Letter")
    for grade in grades:
        if grade[0] == student_id:
            print(f"{grade[1]} {grade[2]}% {grade[3]}")

# Function to view student information
def view_student_info():
    print("\n--- View Student Information ---")
    email = input("Enter Student Email: ")
    password = input("Enter Password: ")
    
    # Verify user credentials
    users = read_file(USERS_FILE)
    user_valid = any(user[0] == email and user[1] == password for user in users)

    if not user_valid:
        print("Invalid credentials. Access denied.")
        return

    students = read_file(STUDENTS_FILE)

    for student in students:
        if student[2] == email:
            print(f"\nStudent Information:\nID: {student[0]}\nName: {student[1]}\nEmail: {student[2]}\nCourses: {student[3]}\nTotal Fees: {student[4]}\nOutstanding Fees: {student[5]}")
            return

    print("Student not found.")

# Registrar menu
def registrar_menu():
    while True:
        print("\n--- Registrar Menu ---")
        print("1. Register New Student")
        print("2. Update Student Records")
        print("3. Manage Enrollments")
        print("4. Issue Transcript")
        print("5. View Student Information")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_student()
        elif choice == '2':
            update_student()
        elif choice == '3':
            manage_enrollments()
        elif choice == '4':
            issue_transcript()
        elif choice == '5':
            view_student_info()
        elif choice == '6':
            print("Exiting Registrar Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

#--------------------------------------- Main program entry point--------------------------------------------------

print("Welcome to the University Management System (UMS)")
# Load user data
users = load_users()
# calling Login function
print("Please login to continue:")

while True:
    login(users)
    print("Do you want to login again? (yes/no)")
    choice = input().lower()
    if not choice == "yes":
        break
print("Goodbye!")
