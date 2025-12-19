import pymysql


class DatabaseModel:
    def __init__(self):
        self.connection = None

    def connect(self):
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
                print("Connection failed:", e)
                self.connection = None
        return self.connection

    def verify_login(self, username, password):
        try:
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()

            # First, try to find in staff_credentials
            query_staff = "SELECT * FROM staff_credentials WHERE username = %s AND password = %s"
            cursor.execute(query_staff, (username, password))
            staff_result = cursor.fetchone()

            if staff_result:
                print(f"✅ Staff login successful! Welcome {staff_result['username']}")
                cursor.close()
                return True, staff_result

            # If not found in staff, check admin_credentials
            query_admin = "SELECT * FROM admin_credentials WHERE user = %s AND pass = %s"
            cursor.execute(query_admin, (username, password))
            admin_result = cursor.fetchone()

            if admin_result:
                # Add 'role' field to match staff structure
                admin_result['role'] = 'admin'
                admin_result['username'] = admin_result['user']  # Standardize field name
                print(f" Admin login successful! Welcome {admin_result['user']}")
                cursor.close()
                return True, admin_result

            # If not found in either table
            print("Invalid username or password")
            cursor.close()
            return False, None

        except pymysql.MySQLError as e:
            print("Database error:", e)
            return False, None