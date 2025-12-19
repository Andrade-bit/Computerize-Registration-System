
#createstaffcontroller
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from createstaffmodel.createstaffmodel import createstaffmodel


class createstaffcontroller:
    def __init__(self):
        print("🎮 Initializing createstaffcontroller...")
        self.model = createstaffmodel()
        print("✓ Controller initialized\n")

    def check_username_exists(self, username):
#Check if username already exists
        if not username:
            return False
        return self.model.username_exists(username)

    def add_staff(self, fullname, username, password):
     #Add new staff through model
        print(f"\n{'=' * 60}")
        print("🔄 Controller: Processing staff creation...")
        print(f"{'=' * 60}")
        print(f"   Full Name: {fullname}")
        print(f"   Username: {username}")
        print(f"   Password: {'*' * len(password)}")

        # Validation
        if not fullname or not username or not password:
            error_msg = "All fields are required!"
            print(f"❌ Validation failed: {error_msg}")
            return False, error_msg

        # Check minimum lengths
        if len(username) < 3:
            error_msg = "Username must be at least 3 characters long!"
            print(f"❌ Validation failed: {error_msg}")
            return False, error_msg

        if len(password) < 6:
            error_msg = "Password must be at least 6 characters long!"
            print(f"❌ Validation failed: {error_msg}")
            return False, error_msg

        print("✓ Validation passed")

        # Check if username exists
        print(f"🔍 Checking if username '{username}' exists...")
        if self.model.username_exists(username):
            error_msg = f"Username '{username}' already exists! Please choose a different username."
            print(f"❌ {error_msg}")
            return False, error_msg

        # Create staff
        print("💾 Creating staff in database...")
        success, staff_id = self.model.create_staff(fullname, username, password)

        if success:
            success_msg = f"Staff '{fullname}' created successfully!\n\nStaff ID: {staff_id}\nUsername: {username}"
            print(f"✅ SUCCESS!")
            print(f"{'=' * 60}\n")
            return True, success_msg
        else:
            error_msg = "Failed to create staff account. Please check database connection."
            print(f"❌ FAILED: {error_msg}")
            print(f"{'=' * 60}\n")
            return False, error_msg