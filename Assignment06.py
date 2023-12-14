# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Joshh, 12/14/23, Completed Script
# ------------------------------------------------------------------------------------------ #
import json
from datetime import date
import os
import io as _io


class IO:
    """
    Class IO consists of functions that manage user input and output
    ChangeLog: (Who, When, What)
    Joshh, 12-14-2023 Created Class
    """
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')
    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user
        ChangeLog: (Who, When, What)
        Joshh, 12-14-23, Created function
        """
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user
        ChangeLog: (Who, When, What)
        Joshh, 12-14-23,Created function
        """
        choice = "0"
        try:
            choice = input("Enter menu selection: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__()) #exception obj

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays all course data in the list.
        ChangeLog: (Who, When, What)
        Joshh, 12-14-23,Created function
        """

        if not student_data:
            print()
            print("There is currently no data to display.")
            print("To enter data, choose menu option 1.")
        else:
            print()
            print("The current data is: \n")
            for student in student_data:
                print(f'{student["FirstName"]}, '
                      f'{student["LastName"]}, '
                      f'{student["CourseName"]}')
            print()

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the first name, last name,and course name from the user.
        ChangeLog: (Who, When, What)
        Joshh, 12-14-23,Created function
        """

        try:
            # Input the data
            student_first_name = input("What is the student's first name? ")
            if not student_first_name.isalpha():
                raise ValueError("Error: First name must be alphabetic")
            student_last_name = input("What is the student's last name? ")
            if not student_last_name.isalpha():
                raise ValueError("Error: Last name must be alphabetic")
            course_name = input("What is the course name? ")
            if not course_name:
                raise ValueError('Error: Course name cannot be blank')
            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print(f'You have registered '
                  f'{student["FirstName"]} '
                  f'{student["LastName"]} for the course '
                  f'{student["CourseName"]}.')

        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)

        return student_data

class FileProcessor:

    """
    class: FileProcessor is a collection of processing functions that work with Json files
    ChangeLog: (Who, When, What)
    Joshh, 12-14-2023, Created class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of dictionary rows
        ChangeLog: (Who, When, What)
        Joshh, 12-14-2023, Created function
        """
        try:
            if os.path.exists(file_name):
                file = open(file_name, "r")
            else:
                print("Existing file not found, creating new file. \n")
                file = open(file_name, 'w')
                file.write("[]")
                file.close()
                file = open(file_name, "r")
            list_of_dictionary_data = json.load(file)
            for student in list_of_dictionary_data:
                student_data.append(student)
                file.close()
        except FileNotFoundError:
            raise FileNotFoundError("Text file must exist before running this script!")
        except Exception:
            raise Exception("There was a non-specific error!")
        except Exception as e:
            IO.output_error_messages("There was an error opening the file!", e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of dictionary rows

    ChangeLog: (Who, When, What)
    Joshh, 12/14/2023,Created function
    """

        try:
            file = open(FILE_NAME, "w")
            json.dump(student_data, file, indent=4)
            file.close()

        except TypeError:
            raise TypeError("Please check that the data is a valid JSON format")
        except PermissionError:
            raise PermissionError("Please check the data file's read/write permission")
        except Exception as e:
            raise Exception("There was a non-specific error!")
        finally:
            if not file.closed:
                file.close()

#-----MAIN-----
#Variables and Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"
menu_choice: str
students: list = []

#Get data from existing file:

students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        try:
            IO.input_student_data(student_data=students)
        except Exception as e:
            IO.output_error_messages(e)
        continue


    elif menu_choice == "2":
        try:
            IO.output_student_courses(student_data=students)
        except Exception as e:
            IO.output_error_messages(e)
        continue

    elif menu_choice == "3":
        try:
            FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
            print(f"Data was saved to the {FILE_NAME} file.")
        except Exception as e:
            IO.output_error_messages(e)
        continue

    elif menu_choice == "4":
        break

print("Program Ended")
