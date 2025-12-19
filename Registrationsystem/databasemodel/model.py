import pymysql


class StudentDatabaseModel:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Connect to the MySQL database"""
        if self.connection is None:
            try:
                self.connection = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="registration",
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("✅ Connected to database successfully!")
            except pymysql.MySQLError as e:
                print("❌ Connection failed:", e)
                self.connection = None
        return self.connection

    def get_all_students(self):
        """Retrieve all student records from student_info table"""
        try:
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                SELECT student_id, first_name, middle_name, last_name, sex, 
                       birth_date, mobile_number, email, street, subdivision,
                       city, province, grade, strand, studentdocu, photo,
                       staff_id, school_year
                FROM student_info
                ORDER BY student_id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            print(f"✅ Retrieved {len(results)} student records")
            return results

        except pymysql.MySQLError as e:
            print(f"❌ Error fetching student data: {e}")
            return []

    def get_student_by_id(self, student_id):
        """Retrieve a specific student by ID"""
        try:
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                SELECT student_id, first_name, middle_name, last_name, sex, 
                       birth_date, mobile_number, email, street, subdivision,
                       city, province, grade, strand, studentdocu, photo,
                       staff_id, school_year
                FROM student_info 
                WHERE student_id = %s
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                print(f"✅ Found student with ID: {student_id}")
                return result
            else:
                print(f"⚠️ No student found with ID: {student_id}")
                return None

        except pymysql.MySQLError as e:
            print(f"❌ Error fetching student by ID: {e}")
            return None

    def search_students(self, search_term, field="first_name"):
        """Search students by a specific field"""
        try:
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()
            query = f"""
                SELECT student_id, first_name, middle_name, last_name, sex, 
                       birth_date, mobile_number, email, street, subdivision,
                       city, province, grade, strand, studentdocu, photo,
                       staff_id, school_year
                FROM student_info
                WHERE {field} LIKE %s
                ORDER BY student_id
            """
            cursor.execute(query, (f"%{search_term}%",))
            results = cursor.fetchall()
            cursor.close()

            print(f"✅ Search found {len(results)} results")
            return results

        except pymysql.MySQLError as e:
            print(f"❌ Error searching students: {e}")
            return []

    def get_column_names(self):
        """Get column names for the table headers"""
        return [
            "Student ID", "First Name", "Middle Name", "Last Name", "Sex",
            "Birth Date", "Mobile Number", "Email", "Street", "Subdivision",
            "City", "Province", "Grade", "Strand", "Student Docu", "Photo",
            "Staff ID", "School Year"
        ]

    def __del__(self):
        """Close database connection when model is destroyed"""
        if self.connection:
            self.connection.close()
            print("🔒 Database connection closed")