from datetime import datetime
import re
import uuid
from cryptography.fernet import Fernet
import getpass
import json
import logging
from colorama import Fore, Style, init

init()

#Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BootcampManager:
    def __init__(self):
        self.students = []
        self.users = []
        self.courses = ["Python Basics", "Data Science", "Web Development", "Machine Learning"]
        self.results = {}
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.announcements = []

        # Store the encryption key securely
        with open("secret.key", "wb") as key_file:
            key_file.write(self.key)

    def welcome_msg(self):
        print(Fore.CYAN + Style.BRIGHT + r"""
        ================================================================================
                 ____    ___    ___    ____      ____    _      __  __     _____   *
                | __ )  / _ \  /   \ |_    _|  /  ___|  / \   |   \/   | |  ___ |  *
                |  _ \ | | | || | | |  |  |   | |      / _ \  | | \/ | | |   __ |  *
                | |_) || |_| || | | |  |  |   | |     /  __ \ | |    | | |  |      *
                |____/  \___/  \___/   |__|    \_____| _/  \_\|_|    |_| |__|      *           
        ================================================================================
                            Welcome to BEP09 Tecvinson's
                            Bootcamp Manager Application!
        ================================================================================
        """ + Style.RESET_ALL)
        print(Fore.GREEN + "Let's get you started!" + Style.RESET_ALL)
    
    def is_valid_user_email(self):
        while True:
            email = input("Enter email: ").strip().lower()
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return email
            else:
                logging.error("Fore.RED + \n⚠️ Invalid email format. Please enter a valid email." + Style.RESET_ALL)


    def is_valid_role(self):
        while True:
            role = input("Enter role (Admin/Parent/Instructor/Student): ").strip().title()
            if role not in ["Admin", "Parent", "Instructor", "Student"]:
                logging.error("\n⚠️  Invalid role. Please enter a valid role.")
            else:
                return role
    
    def is_valid_username(self):
        while True:
            username = input("Enter username: ").strip()
            if len(username) > 1:
                return username
            else:
                logging.error(" \n⚠️  Invalid input. Name must be more than one character long.")

    def is_valid_password(self):
        while True:
            password = getpass.getpass("Enter password: ").strip()
            if len(password) > 7:
                return password
            else:
                logging.error("\n⚠️  Invalid password. Password must be more than seven characters long.")

                

    def register_user(self):
        print(Fore.CYAN + "\n--- User Registration ---" + Style.RESET_ALL)
        username = self.is_valid_username()
        email = self.is_valid_user_email()
        role = self.is_valid_role()
        password = self.is_valid_password()



        user = {
            "username": username,
            "email": email,
            "role": role,
            "password": self.encrypt_data(password)
        }

        self.users.append(user)
        logging.info(Fore.GREEN + f"""Registration successful🎉🌟 
                     {role} account created for {username}.""" + Style.RESET_ALL)

    def login_user(self):
        print(Fore.CYAN + "\n--- User Login ---" + Style.RESET_ALL)
        username = input(Fore.YELLOW + "Enter username: "+ Style.RESET_ALL).strip()
        password = getpass.getpass(Fore.YELLOW + "Enter password: ").strip()

        for user in self.users:
            
            if user["username"] == username and self.decrypt_data(user["password"]) == password:
                logging.info(Fore.GREEN + f"""Login successful!🎉🌟 
                             Welcome, {user['role']} {username}!👋""" + Style.RESET_ALL)
                return user["role"]
        logging.error(Fore.RED + "\n⚠️  Invalid username or password. Please enter the correct details." + Style.RESET_ALL)
        return None

    def encrypt_data(self, data):
        data_str = json.dumps(data).encode('utf-8')
        return self.cipher_suite.encrypt(data_str)

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return json.loads(decrypted_data)

    def is_valid_date_of_birth(self):
        dob = input("Enter your date of birth (YYYY-MM-DD): ").strip()
        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d")
            if birth_date > datetime.now() or birth_date < datetime.now().replace(year=datetime.now().year - 120):
                logging.error(Fore.RED +"\n⚠️  Invalid date of birth. Please enter your correct date of birth." + Style.RESET_ALL)
                return False
            #return True
        except ValueError:
            logging.error("\n⚠️  Invalid date format.")
            return False

    def generate_student_id(self, last_name):
        unique_id = str(uuid.uuid4())[:4]
        return f"{last_name}-{unique_id}"
    
    def is_valid_name(self, name):
        """Validate name (only alphabets allowed)."""
        if name.isalpha():
            return True
        logging.warning(f"\n⚠️  The name: {name} is invalid(Only alphabets are allowed).")
        return False

    def register_student(self):
        first_name = input("Enter your first name: ").strip().title()
        if not self.is_valid_name(first_name):
            logging.warning("\n⚠️  Invalid first name(Only alphabets are allowed).")
            return
        

        last_name = input("Enter your last name: ").strip().title()
        if not self.is_valid_name(last_name):
            logging.warning("\n⚠️  Invalid last name. Only alphabets are allowed.")
            return
        
        email = self.is_valid_user_email()
        dob = self.is_valid_date_of_birth()

        if not (first_name and last_name and email and dob):
            logging.error("\n⚠️ Error: Missing required information")
            return

        print("\nAvailable Courses:")
        for i, course in enumerate(self.courses, 1):
            print(f"{i}. {course}")

        selected_courses = input("\nEnter the courses you want to enroll in (comma-separated): ").strip().split(",")
        selected_courses = [course.strip().title() for course in selected_courses if course.strip().title() in self.courses]

        if not selected_courses:
            logging.error("\n⚠️ Error: No valid courses selected")
            return
        
        student_id = self.generate_student_id(last_name)
        student = {
            "studentID": student_id,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "dateOfBirth": dob,
            "selectedCourses": selected_courses,
            "feesPaid": False
        }

        self.students.append(self.encrypt_data(student))
        logging.info(f"""Registration successful🎉🌟
                      Student ID: {student_id}""")
    def validate_fee_payment(self, student_id):
        for i, encrypted_student in enumerate(self.students):
            student = self.decrypt_data(encrypted_student)
            if student["studentID"] == student_id:
                student["feesPaid"] = True
                self.students[i] = self.encrypt_data(student)
                print(f"Fees validated for student {student['firstName']} {student['lastName']}.")
                return
        logging.error("\n⚠️ Student not found")

    def enroll_student_in_course(self, student_id, selected_courses):
        selected_courses = [course.strip().title() for course in selected_courses if course.strip().title() in self.courses]
        if not selected_courses:
            logging.error("\n⚠️ No valid course selected. Please select a course.")
            return

        for i, encrypted_student in enumerate(self.students):
            student = self.decrypt_data(encrypted_student)
            if student["studentID"] == student_id:
                if student["feesPaid"]:
                    student["selectedCourses"] = selected_courses
                    self.students[i] = self.encrypt_data(student)
                    print(f"Enrollment successful for {student['firstName']} {student['lastName']}.")
                    return
                print(f"\n⚠️ Fees not paid for {student['firstName']} {student['lastName']}.")
                return
        print("\n⚠️ Error: Student not found")

    def view_student_information(self, student_id, role):
        for encrypted_student in self.students:
            student = self.decrypt_data(encrypted_student)
            if student["studentID"] == student_id:
                print(f"\nStudent ID: {student['studentID']}")
                print(f"Name: {student['firstName']} {student['lastName']}")
                print(f"Email: {student['email']}")
                print(f"Date of Birth: {student['dateOfBirth']}")
                print(f"Selected Courses: {', '.join(student['selectedCourses'])}")
                print(f"Fees Paid: {'Yes' if student['feesPaid'] else 'No'}")
                return
        logging.error("\n⚠️ Student not found")

    def score_student(self, student_id, course_name, score, remarks):
        for encrypted_student in self.students:
            student = self.decrypt_data(encrypted_student)
            if student["studentID"] == student_id:
                if course_name in student["selectedCourses"]:
                    if student_id not in self.results:
                        self.results[student_id] = {}
                    self.results[student_id][course_name] = {"score": score, "remarks": remarks}
                    print(f"Score {score} with remarks '{remarks}' assigned to {student['firstName']} {student['lastName']} for {course_name}.")
                else:
                    print(f"Error: Student not enrolled in {course_name}.")
                return
        logging.error("\n⚠️ Student not found")

    def view_student_results(self, student_id, role):
        student_id = input("Enter the student ID: ").strip()
        for encrypted_student in self.students:
            student = self.decrypt_data(encrypted_student)
            if student["studentID"] == student_id:
                if student_id in self.results:
                    print(f"\nResults for {student['firstName']} {student['lastName']}:")
                    for course_name, score in self.results[student_id].items():
                        print(f"{course_name}: {score}")
                else:
                    print(f"No results available for {student['firstName']} {student['lastName']}.")
                return
        logging.error("\n⚠️ Student not found")

    def generate_progress_report(self):
        student_id = input("Enter the student ID: ").strip()

        for encrypted_student in self.students:
            student = self.decrypt_data(encrypted_student)
            if student["studentID"] == student_id:
                print(f"\nProgress Report for {student['firstName']} {student['lastName']}:")
                print(f"\nStudent ID: {student['studentID']}")
                print(f"Email: {student['email']}")
                print(f"Date of Birth: {student['dateOfBirth']}")
                print(f"Selected Courses: {', '.join(student['selectedCourses'])}")
                print(f"Fees Paid: {'Yes' if student['feesPaid'] else 'No'}")

                if student_id in self.results:
                    print("Results:")
                    for course_name, result in self.results[student_id].items():
                        print(f"\n{course_name}: \nScore: {result['score']}, \nRemarks: {result['remarks']}")
                else:
                    logging.error("\n⚠️ No results available.")
                return
        logging.error("\n⚠️ Student not found")

    def create_announcement(self):
        print("\n--- Create Announcement ---")
        announcement = input("Enter the announcement message: ").strip()
        if not announcement:
            logging.warning("\n⚠️ Announcement cannot be empty.")
            return
        
        self.announcements.append(announcement)
        logging.info("Announcement created successfully!🎉")

    def view_announcements(self):
        print("\n--- Announcements ---")
        if not self.announcements:
            print("\n⚠️ No announcements available.")
            return
        
        for i, announcement in enumerate(self.announcements, 1):
            print(f"{i}. {announcement}")

    def handle_announcement_options(self, role):
        while True:
            print("\n--- Announcement Options ---")
            print("1. Create Announcement")
            print("2. View Announcements")
            print("3. Exit")

            option = input("Select an option: ").strip()

            if option == "1":
                if role == "Admin":
                    self.create_announcement()
                else:
                    print("Error: Only admins can create announcements.")
            elif option == "2":
                self.view_announcements()
            elif option == "3":
                break
            else:
                print("Error: Invalid option")


# MAIN MENU FUNCTION

def main():
    manager = BootcampManager()
    manager.welcome_msg()
    while True:
        
        print(Style.BRIGHT + "\n\tSignUp --- (Enter: 1)"+ Style.RESET_ALL)
        print(Style.BRIGHT + "\tLogin --- (Enter: 2)"+ Style.RESET_ALL)
        print(Style.BRIGHT + "\tExit --- (Enter: 3)"+ Style.RESET_ALL)
        
        choice = input(Fore.CYAN +"\nEnter your choice: "+ Style.RESET_ALL).strip()
        
        if choice == '1':
            manager.register_user()
        elif choice == '2':
            role = manager.login_user()
            if role:
                while True:
                    print("\n--- BEP09 Bootcamp Management System ---")
                    
                    if role == "Admin":
                        print("1. Register Student📝")
                        print("2. Validate Fee Payment💰")
                        print("3. Enroll Student in Course🎓")
                        print("4. View Student Information📋")
                        print("5. Score Student🧮")
                        print("6. View Student Results📊")
                        print("7. Generate Progress Report📈")
                        print("8. Handle Announcements📢")
                        print("9. Logout❌")
                    elif role == "Instructor":
                        print("1. Score Student🧮")
                        print("2. View Student Results📊")
                        print("3. Generate Progress Report📈")
                        print("4. View Announcements📢")
                        print("5. Logout❌")
                    elif role == "Parent":
                        print("1. View Student Information📋")
                        print("2. View Student Results📊")
                        print("3. Generate Progress Report📈")
                        print("4. View Announcements📢")
                        print("5. Logout❌")
                    elif role == "Student":
                        print("1. View Your Information📋")
                        print("2. View Your Results📊")
                        print("3. Generate Progress Report📈")
                        print("4. View Announcements📢")
                        print("5. Logout❌")

                    sub_choice = input(Fore.CYAN +"Enter your choice: "+ Style.RESET_ALL).strip()
                    if role == "Admin":
                        if sub_choice == '1':
                            manager.register_student()
                        elif sub_choice == '2':
                            student_id = input("Enter the student ID: ").strip()
                            manager.validate_fee_payment(student_id)
                        elif sub_choice == '3':
                            student_id = input("Enter the student ID: ").strip()
                            selected_courses = input("Enter the courses to enroll in (comma-separated): ").strip().split(",")
                            manager.enroll_student_in_course(student_id, selected_courses)
                        elif sub_choice == '4':
                            student_id = input("Enter the student ID: ").strip()
                            manager.view_student_information(student_id, role)
                        elif sub_choice == '5':
                            student_id = input("Enter the student ID: ").strip()
                            course_name = input("Enter the course name: ").strip().title()
                            score = input("Enter the score: ").strip()
                            remarks = input("Enter your remarks: ").strip()
                            manager.score_student(student_id, course_name, score, remarks)
                        elif sub_choice == '6':
                            manager.view_student_results(student_id, role)
                        elif sub_choice == '7':
                            manager.generate_progress_report()
                        elif sub_choice == '8':
                            manager.handle_announcement_options(role)
                        elif sub_choice == '9':
                            print("Logging out...")
                            break
                    elif role == "Instructor":
                        if sub_choice == '1':
                            student_id = input("Enter the student ID: ").strip()
                            course_name = input("Enter the course name: ").strip().title()
                            score = input("Enter the score: ").strip()
                            remarks = input("Enter your remarks: ").strip()
                            manager.score_student(student_id, course_name, score, remarks)
                        elif sub_choice == '2':
                            manager.view_student_results(student_id, role)
                        elif sub_choice == '3':
                            manager.generate_progress_report()
                        elif sub_choice == '4':
                            manager.view_announcements()
                        elif sub_choice == '5':
                            print("Logging out...")
                            break
                    elif role in [ "Student", "Parent" ]:
                        if sub_choice == '1':
                            student_id = input("Enter your student ID: ").strip()
                            manager.view_student_information(student_id, role)
                        elif sub_choice == '2':
                            student_id = input("Enter your student ID: ").strip()
                            manager.view_student_results(student_id, role)
                        elif sub_choice == '3':
                            manager.generate_progress_report()
                        elif sub_choice == '4':
                            manager.view_announcements()
                        elif sub_choice == '5':
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting Bootcamp Manager...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()