# # modelstudent.py
# import mysql.connector
# from mysql.connector import Error
#
#
# class StudentModel:
#     def __init__(self):
#         self.connection = None
#         self.connect_to_database()
#
#     def connect_to_database(self):
#         #Establish connection to MySQL database
#         try:
#             self.connection = mysql.connector.connect(
#                 host='127.0.0.1',
#                 database='registration',
#                 user='root',  # Change if your username is different
#                 password=''   # Add your password if you have one
#             )
#             if self.connection.is_connected():
#                 print("✅ Connected to MySQL database")
#         except Error as e:
#             print(f"❌ Error connecting to MySQL: {e}")
#             self.connection = None
#
#     def get_all_students(self):
#         #Retrieve all students from student_info table
#         if not self.connection or not self.connection.is_connected():
#             print("❌ No database connection")
#             return []
#
#         try:
#             cursor = self.connection.cursor(dictionary=True)
#             query = """
#                 SELECT
#                     first_name,
#                     middle_name,
#                     last_name,
#                     birth_date,
#                     sex,
#                     mobile_number,
#                     email,
#                     street,
#                     subdivision,
#                     city,
#                     province,
#                     grade,
#                     strand,
#                     studentdocu,
#                     photo,
#                     student_id
#                 FROM student_info
#                 ORDER BY student_id DESC
#             """
#             cursor.execute(query)
#             students = cursor.fetchall()
#             cursor.close()
#             print(f"✅ Retrieved {len(students)} students from database")
#             return students
#         except Error as e:
#             print(f"❌ Error fetching students: {e}")
#             return []
#
#     def close_connection(self):
#         #Close database connection
#         if self.connection and self.connection.is_connected():
#             self.connection.close()
#             print("✅ Database connection closed")
#
#     def __del__(self):
#         #Destructor to ensure connection is closed
#         self.close_connection()
# #model
# import mysql.connector
# from mysql.connector import Error
#
#
# class StudentModel:
#     def __init__(self):
#         self.connection = None
#         self.connect_to_database()
#
#     def connect_to_database(self):
#         """Establish connection to MySQL database"""
#         try:
#             self.connection = mysql.connector.connect(
#                 host='127.0.0.1',
#                 database='registration',
#                 user='root',
#                 password=''
#             )
#             if self.connection.is_connected():
#                 print("✅ Connected to MySQL database")
#         except Error as e:
#             print(f"❌ Error connecting to MySQL: {e}")
#             self.connection = None
#
#     def get_all_students(self):
#         """Retrieve all students from student_info table"""
#         if not self.connection or not self.connection.is_connected():
#             print("❌ No database connection")
#             return []
#
#         try:
#             cursor = self.connection.cursor(dictionary=True)
#             query = """
#                 SELECT
#                     student_id,
#                     first_name,
#                     middle_name,
#                     last_name,
#                     birth_date,
#                     sex,
#                     mobile_number,
#                     email,
#                     street,
#                     subdivision,
#                     city,
#                     province,
#                     grade,
#                     strand,
#                     photo,
#                     school_year,
#                     radio33_status,
#                     radio34_status
#                 FROM student_info
#                 ORDER BY student_id DESC
#             """
#             cursor.execute(query)
#             students = cursor.fetchall()
#             cursor.close()
#             print(f"✅ Retrieved {len(students)} students from database")
#             return students
#         except Error as e:
#             print(f"❌ Error fetching students: {e}")
#             return []
#
#     def close_connection(self):
#         """Close database connection"""
#         if self.connection and self.connection.is_connected():
#             self.connection.close()
#             print("✅ Database connection closed")
#
#     def __del__(self):
#         """Destructor to ensure connection is closed"""
#         self.close_connection()
# model.py - FIXED
# import mysql.connector
# from mysql.connector import Error
#
#
# class StudentModel:
#     def __init__(self):
#         self.connection = None
#         self.connect_to_database()
#
#     def connect_to_database(self):
#         """Establish connection to MySQL database"""
#         try:
#             self.connection = mysql.connector.connect(
#                 host='127.0.0.1',
#                 database='registration',
#                 user='root',
#                 password=''
#             )
#             if self.connection.is_connected():
#                 print("✅ Connected to MySQL database")
#         except Error as e:
#             print(f"❌ Error connecting to MySQL: {e}")
#             self.connection = None
#
#     def get_all_students(self):
#         """Retrieve ALL students from student_info table - INCLUDING emergency_number and staff_id"""
#         if not self.connection or not self.connection.is_connected():
#             print("❌ No database connection")
#             return []
#
#         try:
#             cursor = self.connection.cursor(dictionary=True)
#             query = """
#                 SELECT
#                     student_id,
#                     first_name,
#                     middle_name,
#                     last_name,
#                     birth_date,
#                     sex,
#                     mobile_number,
#                     emergency_number,  -- ADD THIS
#                     email,
#                     street,
#                     subdivision,
#                     city,
#                     province,
#                     grade,
#                     strand,
#                     photo,
#                     school_year,
#                     radio33_status,
#                     radio34_status,
#                     staff_id  -- ADD THIS
#                 FROM student_info
#                 ORDER BY student_id DESC
#             """
#             cursor.execute(query)
#             students = cursor.fetchall()
#             cursor.close()
#             print(f"✅ Retrieved {len(students)} students from database")
#
#             # Debug: Print first student to see what data we have
#             if students:
#                 print("🔍 First student data:")
#                 for key, value in students[0].items():
#                     print(f"   {key}: {value}")
#
#             return students
#         except Error as e:
#             print(f"❌ Error fetching students: {e}")
#             return []
#
#     def close_connection(self):
#         """Close database connection"""
#         if self.connection and self.connection.is_connected():
#             self.connection.close()
#             print("✅ Database connection closed")
#
#     def __del__(self):
#         """Destructor to ensure connection is closed"""
#         self.close_connection()
import mysql.connector
from mysql.connector import Error


class StudentModel:
    def __init__(self):
        self.connection = None
        self.connect_to_database()

    def connect_to_database(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                database='registration',
                user='root',
                password=''
            )
            if self.connection.is_connected():
                print("✅ Connected to MySQL database")
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            self.connection = None

    def get_all_students(self):
        """Retrieve all students from student_info table"""
        if not self.connection or not self.connection.is_connected():
            print("❌ No database connection")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    student_id,
                    first_name,
                    middle_name,
                    last_name,
                    birth_date,
                    sex,
                    mobile_number,
                    emergency_number,
                    email,
                    street,
                    subdivision,
                    city,
                    province,
                    grade,
                    strand,
                    photo,
                    school_year,
                    radio33_status,
                    radio34_status,
                    staff_id
                FROM student_info
                ORDER BY student_id DESC
            """
            cursor.execute(query)
            students = cursor.fetchall()
            cursor.close()
            print(f"✅ Retrieved {len(students)} students from database")
            return students
        except Error as e:
            print(f"❌ Error fetching students: {e}")
            return []

    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ Database connection closed")

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close_connection()