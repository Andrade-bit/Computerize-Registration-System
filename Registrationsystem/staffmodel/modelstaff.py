import mysql.connector
from mysql.connector import Error, pooling
import threading


class StudentModel:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StudentModel, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        """Initialize database connection pool - only once"""
        if not self._initialized:
            self.host = "127.0.0.1"
            self.database = "registration"
            self.user = "root"
            self.password = ""
            self.pool = None
            self._initialize_pool()
            self._initialized = True

    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="student_pool",
                pool_size=5,
                pool_reset_session=True,
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                autocommit=False,
                connection_timeout=30,
                buffered=True
            )
            print("Database connection pool initialized successfully")
        except Error as e:
            print(f"Error creating connection pool: {e}")
            # Create a single connection as fallback
            self.pool = None

    def _get_connection(self):
        """Get a database connection from pool or create new one"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if self.pool:
                    connection = self.pool.get_connection()
                    if connection.is_connected():
                        return connection
                else:
                    # Fallback to single connection
                    connection = mysql.connector.connect(
                        host=self.host,
                        database=self.database,
                        user=self.user,
                        password=self.password,
                        autocommit=False,
                        connection_timeout=30
                    )
                    if connection.is_connected():
                        return connection
            except Error as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise e
        return None

    def _execute_with_connection(self, operation, *args, **kwargs):
        """Execute database operation with proper connection handling"""
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            if not connection:
                return None if operation.get('fetch', False) else False

            cursor = connection.cursor(buffered=True)

            if 'params' in operation:
                cursor.execute(operation['query'], operation['params'])
            else:
                cursor.execute(operation['query'])

            if operation.get('commit', False):
                connection.commit()

            if operation.get('fetch', False):
                if operation.get('fetchone', False):
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
                return result
            elif operation.get('lastrowid', False):
                return cursor.lastrowid
            else:
                return cursor.rowcount

        except Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def check_student_exists_by_email(self, email):
        """Check if a student with the given email already exists"""
        try:
            operation = {
                'query': "SELECT COUNT(*) FROM student_info WHERE email = %s",
                'params': (email,),
                'fetch': True,
                'fetchone': True
            }
            result = self._execute_with_connection(operation)
            return result[0] > 0 if result else False
        except Error:
            return False

    def check_student_exists_by_mobile(self, mobile_number):
        """Check if a student with the given mobile number already exists"""
        try:
            operation = {
                'query': "SELECT COUNT(*) FROM student_info WHERE mobile_number = %s",
                'params': (mobile_number,),
                'fetch': True,
                'fetchone': True
            }
            result = self._execute_with_connection(operation)
            return result[0] > 0 if result else False
        except Error:
            return False

    def check_student_exists_by_name_and_birthdate(self, first_name, last_name, birth_date):
        """Check if a student with the same name and birth date already exists"""
        try:
            operation = {
                'query': """
                    SELECT COUNT(*) FROM student_info 
                    WHERE first_name = %s AND last_name = %s AND birth_date = %s
                """,
                'params': (first_name, last_name, birth_date),
                'fetch': True,
                'fetchone': True
            }
            result = self._execute_with_connection(operation)
            return result[0] > 0 if result else False
        except Error:
            return False

    def insert_student(self, student_data):
        """Insert a new student into the database"""
        try:
            # Check for duplicates in a single transaction
            email = student_data.get('email', '')
            mobile_number = student_data.get('mobile_number', '')
            first_name = student_data.get('first_name', '')
            last_name = student_data.get('last_name', '')
            birth_date = student_data.get('birth_date', '')

            # Use a single connection for all checks and insert
            connection = self._get_connection()
            if not connection:
                return False, None, "Failed to connect to database"

            cursor = connection.cursor(buffered=True)

            # Check duplicates
            duplicate_messages = []

            if email:
                cursor.execute("SELECT email FROM student_info WHERE email = %s", (email,))
                if cursor.fetchone():
                    duplicate_messages.append(f"Email '{email}'")

            if mobile_number:
                cursor.execute("SELECT mobile_number FROM student_info WHERE mobile_number = %s", (mobile_number,))
                if cursor.fetchone():
                    duplicate_messages.append(f"Mobile number '{mobile_number}'")

            if first_name and last_name and birth_date:
                cursor.execute(
                    "SELECT first_name FROM student_info WHERE first_name = %s AND last_name = %s AND birth_date = %s",
                    (first_name, last_name, birth_date)
                )
                if cursor.fetchone():
                    duplicate_messages.append(f"Name '{first_name} {last_name}' with birth date '{birth_date}'")

            if duplicate_messages:
                cursor.close()
                connection.close()
                return False, None, f"Student with {', '.join(duplicate_messages)} already exists!"

            # Insert the student with school_year
            query = """
                INSERT INTO student_info 
                (first_name, middle_name, last_name, sex, birth_date, school_year,
                mobile_number, email, street, subdivision, city, province, 
                grade, strand, studentdocu, photo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                student_data.get('first_name', ''),
                student_data.get('middle_name', ''),
                student_data.get('last_name', ''),
                student_data.get('sex', ''),
                student_data.get('birth_date', ''),
                student_data.get('school_year', None),
                student_data.get('mobile_number', ''),
                student_data.get('email', ''),
                student_data.get('street', ''),
                student_data.get('subdivision', ''),
                student_data.get('city', ''),
                student_data.get('province', ''),
                student_data.get('grade', ''),
                student_data.get('strand', ''),
                student_data.get('studentdocu', ''),
                student_data.get('photo', '')
            )

            cursor.execute(query, values)
            connection.commit()

            student_id = cursor.lastrowid

            cursor.close()
            connection.close()

            return True, student_id, "Student added successfully!"

        except Error as e:
            print(f"Insert error: {e}")
            if 'connection' in locals() and connection:
                connection.rollback()
                if connection.is_connected():
                    connection.close()
            return False, None, f"Database error: {str(e)}"

    def get_all_students(self):
        """Retrieve all students from the database"""
        try:
            operation = {
                'query': """
                    SELECT student_id, first_name, middle_name, last_name, sex, 
                           birth_date, school_year, mobile_number, email, street, 
                           subdivision, city, province, grade, strand, studentdocu, photo
                    FROM student_info
                    ORDER BY student_id DESC
                """,
                'fetch': True
            }
            result = self._execute_with_connection(operation)
            return result if result else []
        except Error as e:
            print(f"Get all students error: {e}")
            return []

    def delete_student(self, student_id):
        """Delete a student from the database"""
        try:
            operation = {
                'query': "DELETE FROM student_info WHERE student_id = %s",
                'params': (student_id,),
                'commit': True
            }
            self._execute_with_connection(operation)
            return True, "Student deleted successfully!"
        except Error as e:
            print(f"Delete error: {e}")
            return False, f"Database error: {str(e)}"