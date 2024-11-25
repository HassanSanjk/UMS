#University Management System






#----------------------------------------------------------HASSAN ABDALLA--------------------------------------------------------------------------------------
'''Lecturer 
• View Assigned Modules: View the list of modules assigned to the lecturers. 
• Record Grades: Add or update student grades for a specific module. 
• View Student List: Display the list of students enrolled in each assigned module. 
• Track Attendance: Mark attendance for students. 
• View Student Grades: Access grades for students in each of the lecturer's modules. '''

def lecturer_menu(lecturer_id):
    while True:
        print("\n=== Lecturer Menu ===")
        print("1. View Assigned Modules")
        print("2. Record/Update Grades")
        print("3. View Student List")
        print("4. Track Attendance")
        print("5. View Student Grades")
        print("6. Logout")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            view_assigned_modules(lecturer_id)
        elif choice == "2":
            record_grades(lecturer_id)
        elif choice == "3":
            view_student_list(lecturer_id)
        elif choice == "4":
            track_attendance(lecturer_id)
        elif choice == "5":
            view_student_grades(lecturer_id)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def view_assigned_modules(lecturer_id):
    try:
        modules = []
        with open("lecturer_modules.txt", "r") as file:
            for line in file:
                l_id, course_code, semester = line.strip().split(",")
                if l_id == lecturer_id:
                    # Get course details from courses.txt
                    course_name = get_course_name(course_code)
                    modules.append(f"{course_code} - {course_name} ({semester})")
        
        if modules:
            print("\n=== Your Assigned Modules ===")
            for i, module in enumerate(modules, 1):
                print(f"{i}. {module}")
        else:
            print("No modules assigned yet.")
            
    except FileNotFoundError:
        print("Error: Data file not found.")

def record_grades(lecturer_id):
    # First select the module
    module = select_module(lecturer_id)
    if not module:
        return

    # Get student list for the module
    students = get_enrolled_students(module['course_code'], module['semester'])
    
    print("\n=== Record Grades ===")
    print(f"Module: {module['course_code']}")
    
    for student in students:
        while True:
            try:
                marks = float(input(f"\nEnter marks for {student['name']} ({student['id']}): "))
                if 0 <= marks <= 100:
                    grade_letter = calculate_grade(marks)  # Convert marks to letter grade
                    
                    # Update grades.txt
                    update_grade(student['id'], module['course_code'], 
                               module['semester'], marks, grade_letter)
                    break
                else:
                    print("Marks must be between 0 and 100")
            except ValueError:
                print("Please enter a valid number")

def calculate_grade(marks):
    if marks >= 90: return 'A+'
    elif marks >= 80: return 'A'
    elif marks >= 75: return 'A-'
    # ... continue for other grades
def track_attendance(lecturer_id):
    # Select module
    module = select_module(lecturer_id)
    if not module:
        return
        
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Get student list
    students = get_enrolled_students(module['course_code'], module['semester'])
    
    print("\n=== Mark Attendance ===")
    print(f"Date: {today}")
    print(f"Module: {module['course_code']}")
    
    for student in students:
        while True:
            status = input(f"{student['name']} ({student['id']})"
                         " [P]resent/[A]bsent/[L]ate: ").upper()
                         
            if status in ['P', 'A', 'L']:
                full_status = {'P': 'Present', 'A': 'Absent', 'L': 'Late'}[status]
                
                # Record in attendance.txt
                record_attendance(today, module['course_code'], 
                                student['id'], full_status, lecturer_id)
                break
            else:
                print("Invalid input. Please use P, A, or L.")

def view_student_list(lecturer_id):
    # Select module
    module = select_module(lecturer_id)
    if not module:
        return
        
    students = get_enrolled_students(module['course_code'], module['semester'])
    
    print(f"\n=== Student List for {module['course_code']} ===")
    print("ID\t\tName\t\tStatus")
    print("-" * 50)
    
    for student in students:
        print(f"{student['id']}\t{student['name']}\t{student['status']}")

def view_student_grades(lecturer_id):
    # Select module
    module = select_module(lecturer_id)
    if not module:
        return
        
    print(f"\n=== Grade Report for {module['course_code']} ===")
    print("ID\t\tName\t\tMarks\tGrade")
    print("-" * 50)
    
    grades = get_module_grades(module['course_code'], module['semester'])
    for grade in grades:
        student = get_student_details(grade['student_id'])
        print(f"{student['id']}\t{student['name']}\t"
              f"{grade['marks']}\t{grade['grade_letter']}")

def get_enrolled_students(course_code, semester):
    students = []
    try:
        with open("enrollments.txt", "r") as file:
            for line in file:
                s_id, c_code, sem, status = line.strip().split(",")
                if c_code == course_code and sem == semester:
                    student_details = get_student_details(s_id)
                    students.append(student_details)
    except FileNotFoundError:
        print("Error: Enrollment data not found")
    return students

def get_student_details(student_id):
    # Read from students.txt and return student info
    pass

def update_grade(student_id, course_code, semester, marks, grade_letter):
    # Update or add new grade entry in grades.txt
    pass

def record_attendance(date, course_code, student_id, status, lecturer_id):
    # Record new attendance entry in attendance.txt
    pass


#------------------------------------------------MOHAMMED EISSA--------------------------------------------------

# File Paths
STUDENTS_FILE = "students.txt"
PAYMENTS_FILE = "payments.txt"


# Function to read data from a file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Creating a new file.")
        open(file_path, 'w').close()  # Create the file if it doesn't exist
        print(f"{file_path} created. Please populate it with data as needed.")
        return []


# Function to write data to a file
def write_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            file.writelines(data)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")


# Function to check if input is a valid numeric value
def is_valid_number(value):
    return value.isdigit()


# Function to check if a student exists in the students file
def student_exists(student_id):
    students = read_file(STUDENTS_FILE)
    return any(student.startswith(student_id) for student in students)


# Function to record tuition fees with duplicate check
def record_tuition_fee():
    student_id = input("Enter Student ID: ")
    if not student_exists(student_id):
        print("Error: Student ID not found in students file.")
        return

    # Read the existing payment records
    payments = read_file(PAYMENTS_FILE)

    # Check for existing payment record for the student
    for record in payments:
        if record.startswith(student_id):
            print("Error: Payment record for this student already exists.")
            return

    # If no duplicate found, proceed to record the payment
    amount_paid = input("Enter Amount Paid: ")
    if not is_valid_number(amount_paid):
        print("Error: Amount must be a numeric value.")
        return

    payment_record = f"{student_id},{amount_paid}\n"
    payments.append(payment_record)
    write_file(PAYMENTS_FILE, payments)
    print("Tuition fee recorded successfully.")


# Function to view outstanding fees
def view_outstanding_fees():
    students = read_file(STUDENTS_FILE)
    payments = read_file(PAYMENTS_FILE)

    paid_students = {line.split(",")[0] for line in payments}
    outstanding = [line for line in students if line.split(",")[0] not in paid_students]

    if outstanding:
        print("Outstanding Fees for Students:")
        for student in outstanding:
            print(student.strip())
    else:
        print("No outstanding fees.")


# Function to update payment records
def update_payment_record():
    student_id = input("Enter Student ID to update payment: ")
    if not student_exists(student_id):
        print("Error: Student ID not found in students file.")
        return

    new_amount = input("Enter New Amount Paid: ")
    if not is_valid_number(new_amount):
        print("Error: Amount must be a numeric value.")
        return

    data = read_file(PAYMENTS_FILE)
    updated = False
    for i, record in enumerate(data):
        if record.startswith(student_id):
            data[i] = f"{student_id},{new_amount}\n"
            updated = True
            break

    if updated:
        write_file(PAYMENTS_FILE, data)
        print("Payment record updated successfully.")
    else:
        print("Student ID not found in payment records.")


# Function to issue receipts
def issue_receipt():
    student_id = input("Enter Student ID: ")
    payments = read_file(PAYMENTS_FILE)

    for record in payments:
        if record.startswith(student_id):
            amount = record.split(",")[1].strip()
            print(f"Receipt for Student ID: {student_id}")
            print(f"Amount Paid: {amount}")
            return

    print("No payment record found for the given Student ID.")


# Function to view financial summary
def view_financial_summary():
    payments = read_file(PAYMENTS_FILE)
    try:
        total_collected = sum(float(record.split(",")[1]) for record in payments)
    except ValueError:
        print("Error: Invalid data format in payments file.")
        return

    outstanding_count = len(read_file(STUDENTS_FILE)) - len(payments)

    print("Financial Summary:")
    print(f"Total Fees Collected: {total_collected}")
    print(f"Number of Students with Outstanding Fees: {outstanding_count}")


# Main Menu System
def main_menu():
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


# Run the main menu
main_menu()

#-----------------------------------------Omda-----------------------------------------------------------------------


