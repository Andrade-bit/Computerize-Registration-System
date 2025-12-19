import mysql.connector
from mysql.connector import Error


class StaffRegistrationModel:
    def __init__(self):
        """Initialize database connection"""
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
                print(f"✅ Connected to database: registration")
                return True
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False

    def create_table_if_not_exists(self):
        """Create student_info table if it doesn't exist"""
        try:
            cursor = self.connection.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS student_info (
                student_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) DEFAULT NULL,
                middle_name VARCHAR(255) DEFAULT NULL,
                last_name VARCHAR(255) DEFAULT NULL,
                sex VARCHAR(50) DEFAULT NULL,
                birth_date DATE DEFAULT NULL,
                mobile_number VARCHAR(255) DEFAULT NULL,
                emergency_number VARCHAR(255) DEFAULT NULL,
                email VARCHAR(255) DEFAULT NULL,
                street VARCHAR(255) DEFAULT NULL,
                subdivision VARCHAR(255) DEFAULT NULL,
                city VARCHAR(255) DEFAULT NULL,
                province VARCHAR(255) DEFAULT NULL,
                grade VARCHAR(255) DEFAULT NULL,
                strand VARCHAR(255) DEFAULT NULL,
                photo VARCHAR(255) DEFAULT NULL,
                school_year DATE DEFAULT NULL,
                radio33_status VARCHAR(10) DEFAULT NULL,
                radio34_status VARCHAR(10) DEFAULT NULL,
                staff_id INT(11) DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """

            cursor.execute(create_table_query)
            self.connection.commit()
            print("✅ Table 'student_info' checked/created successfully")
            cursor.close()
            return True

        except Error as e:
            print(f"❌ Error creating table: {e}")
            return False

    def save_staff_info(self, data):
        """Save student information to database - INCLUDES staff_id"""
        try:
            if not self.connection or not self.connection.is_connected():
                print("❌ Database connection lost! Reconnecting...")
                self.connect_to_database()

            cursor = self.connection.cursor()

            # INSERT query with staff_id field
            insert_query = """
            INSERT INTO student_info 
            (first_name, middle_name, last_name, sex, birth_date, 
             mobile_number, emergency_number, email, street, subdivision, city, province,
             staff_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                data.get('first_name'),
                data.get('middle_name'),
                data.get('last_name'),
                data.get('sex'),
                data.get('birth_date'),
                data.get('mobile_number'),
                data.get('emergency_number'),
                data.get('email'),
                data.get('street'),
                data.get('subdivision'),
                data.get('city'),
                data.get('province'),
                data.get('staff_id')  # ADD STAFF ID TO INSERT
            )

            cursor.execute(insert_query, values)
            self.connection.commit()

            student_id = cursor.lastrowid
            cursor.close()

            print(f"✅ Created new student with ID: {student_id}")
            print(f"✅ Staff ID saved: {data.get('staff_id')}")
            return student_id

        except Error as e:
            print(f"❌ Error saving student info: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_student_with_staff(self, student_id, data, logged_in_staff_id):
        """Update existing student with registration details"""
        try:
            if not self.connection or not self.connection.is_connected():
                print("❌ Database connection lost! Reconnecting...")
                self.connect_to_database()

            cursor = self.connection.cursor()

            update_query = """
            UPDATE student_info 
            SET grade = %s,
                strand = %s,
                photo = %s,
                school_year = %s,
                radio33_status = %s,
                radio34_status = %s
            WHERE student_id = %s
            """

            values = (
                data.get('grade'),
                data.get('strand'),
                data.get('photo'),
                data.get('school_year'),
                data.get('radio33_status'),
                data.get('radio34_status'),
                student_id
            )

            print(f"\n🔍 Updating student registration details...")
            print(f"   Student ID: {student_id}")
            print(f"   Grade: {data.get('grade')}")
            print(f"   Strand: {data.get('strand')}")
            print(f"   Staff ID in record: {data.get('staff_id')}")

            cursor.execute(update_query, values)
            self.connection.commit()

            rows_affected = cursor.rowcount
            cursor.close()

            if rows_affected > 0:
                print(f"✅ Student ID {student_id} updated successfully!")
                print(f"✅ Staff ID already saved from first form: {data.get('staff_id')}")
                return True
            else:
                print(f"⚠️ No student found with ID {student_id}")
                return False

        except Exception as e:
            print(f"❌ Error updating student: {e}")
            if self.connection:
                self.connection.rollback()
            import traceback
            traceback.print_exc()
            return False

    def check_staff_exists(self, email, mobile):
        """Check if student already exists"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_to_database()

            cursor = self.connection.cursor()

            check_query = """
            SELECT student_id FROM student_info 
            WHERE email = %s OR mobile_number = %s
            """

            cursor.execute(check_query, (email, mobile))
            result = cursor.fetchone()
            cursor.close()

            return result is not None

        except Error as e:
            print(f"❌ Error checking student existence: {e}")
            return False

    def get_staff_by_id(self, staff_id):
        """Retrieve student information by student_id"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            select_query = """
            SELECT * FROM student_info WHERE student_id = %s
            """

            cursor.execute(select_query, (staff_id,))
            result = cursor.fetchone()
            cursor.close()

            return result

        except Error as e:
            print(f"❌ Error retrieving student: {e}")
            return None

    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ Database connection closed")