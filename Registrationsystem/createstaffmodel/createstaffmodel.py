
#createstaffmodel
import pymysql


class createstaffmodel:
    def __init__(self):
        self.connection = None

    def connect(self):
        #Connect to the database
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

    def username_exists(self, username):
        #Check if username already exists in staff_credentials table
        try:
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()
            query = "SELECT username FROM staff_credentials WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                print(f"⚠️ Username '{username}' already exists")
                return True  # Username exists
            return False  # Username is available

        except pymysql.MySQLError as e:
            print(f"❌ Error checking username: {e}")
            return True  # Return True to be safe and prevent creation

    def create_staff(self, fullname, username, password):
        #Insert staff into both staff and staff_credentials tables
        try:
            if self.connection is None:
                self.connect()

            # Double-check username doesn't exist before creating
            if self.username_exists(username):
                print(f"❌ Cannot create staff: Username '{username}' already exists")
                return False, None

            cursor = self.connection.cursor()

            # Step 1: Insert into staff table
            query_staff = "INSERT INTO staff (fullname) VALUES (%s)"
            cursor.execute(query_staff, (fullname,))
            self.connection.commit()

            # Get the last inserted staff_id
            staff_id = cursor.lastrowid

            # Step 2: Insert into staff_credentials table
            query_credentials = "INSERT INTO staff_credentials (staff_id, username, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_credentials, (staff_id, username, password, 'staff'))
            self.connection.commit()

            cursor.close()
            print(f"✅ Staff created successfully! staff_id: {staff_id}")
            return True, staff_id

        except pymysql.MySQLError as e:
            print("❌ Database error:", e)
            if self.connection:
                self.connection.rollback()

            # Check if error is due to duplicate username
            if "Duplicate entry" in str(e) or "unique" in str(e).lower():
                print(f"❌ Duplicate username error: '{username}'")

            return False, None

    def __del__(self):
        #Close database connection when model is destroyed
        if self.connection:
            self.connection.close()