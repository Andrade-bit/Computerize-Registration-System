#admin
import pymysql


class adminmodel:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Connect to the database"""
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

    def get_all_staff(self):
        """Retrieve all staff from database - join staff and staff_credentials tables"""
        try:
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()
            query = """
                SELECT s.fullname as name, sc.username, sc.password 
                FROM staff s
                INNER JOIN staff_credentials sc ON s.staff_id = sc.staff_id
            """
            cursor.execute(query)
            staff_list = cursor.fetchall()
            cursor.close()

            print(f"✅ Retrieved {len(staff_list)} staff members from database")
            return staff_list

        except pymysql.MySQLError as e:
            print("❌ Database error:", e)
            return []