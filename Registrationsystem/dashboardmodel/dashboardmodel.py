# modeldashboard.py
import mysql.connector
from mysql.connector import Error


class DashboardModel:
    def __init__(self):
        #Initialize database connection parameters
        self.host = "127.0.0.1"
        self.database = "registration"
        self.user = "root"
        self.password = ""
        self.connection = None

    def connect(self):
    #Establish connection to the database
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_total_students(self):
        #Get total number of registered students
        try:
            if not self.connect():
                return 0

            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM student_info"
            cursor.execute(query)
            result = cursor.fetchone()

            cursor.close()
            self.disconnect()

            return result[0] if result else 0

        except Error as e:
            print(f"Error getting total students: {e}")
            return 0
        finally:
            self.disconnect()

    def get_students_by_grade(self):
        #Get count of students by grade
        try:
            if not self.connect():
                return {}

            cursor = self.connection.cursor()
            query = """
                SELECT grade, COUNT(*) as count 
                FROM student_info 
                GROUP BY grade
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.disconnect()

            grade_data = {}
            for grade, count in results:
                grade_data[grade] = count

            return grade_data

        except Error as e:
            print(f"Error getting students by grade: {e}")
            return {}
        finally:
            self.disconnect()

    def get_students_by_sex(self):
       #Get count of students by sex
        try:
            if not self.connect():
                return {}

            cursor = self.connection.cursor()
            query = """
                SELECT sex, COUNT(*) as count 
                FROM student_info 
                GROUP BY sex
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.disconnect()

            sex_data = {}
            for sex, count in results:
                sex_data[sex] = count

            return sex_data

        except Error as e:
            print(f"Error getting students by sex: {e}")
            return {}
        finally:
            self.disconnect()

    def get_students_by_strand(self):
        #Get count of students by strand
        try:
            if not self.connect():
                return {}

            cursor = self.connection.cursor()
            query = """
                SELECT strand, COUNT(*) as count 
                FROM student_info 
                GROUP BY strand
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.disconnect()

            strand_data = {}
            for strand, count in results:
                strand_data[strand] = count

            return strand_data

        except Error as e:
            print(f"Error getting students by strand: {e}")
            return {}
        finally:
            self.disconnect()

    def get_students_with_documents(self):
        #Get count of students with complete documents
        try:
            if not self.connect():
                return {'complete': 0, 'incomplete': 0}

            cursor = self.connection.cursor()

            # Count students with both documents
            query_complete = """
                SELECT COUNT(*) FROM student_info 
                WHERE studentdocu LIKE '%Good Moral: Yes%' 
                AND studentdocu LIKE '%Student Form: Yes%'
            """
            cursor.execute(query_complete)
            complete = cursor.fetchone()[0]

            # Count students with incomplete documents
            query_incomplete = """
                SELECT COUNT(*) FROM student_info 
                WHERE studentdocu NOT LIKE '%Good Moral: Yes%' 
                OR studentdocu NOT LIKE '%Student Form: Yes%'
            """
            cursor.execute(query_incomplete)
            incomplete = cursor.fetchone()[0]

            cursor.close()
            self.disconnect()

            return {'complete': complete, 'incomplete': incomplete}

        except Error as e:
            print(f"Error getting document statistics: {e}")
            return {'complete': 0, 'incomplete': 0}
        finally:
            self.disconnect()