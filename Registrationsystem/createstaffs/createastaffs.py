
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt
import sys
import os


class createacc(QDialog):
    def __init__(self):
        super().__init__()
        # Get absolute path to Finalsecond.ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "Finalsecond.ui")
        uic.loadUi(ui_path, self)

        # Initialize controller
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from createstaffcontroller.createstaffcontroller import createstaffcontroller
        self.controller = createstaffcontroller()

        # Set password field to show asterisks
        self.lineEdit_5.setEchoMode(QLineEdit.EchoMode.Password)

        # Connect buttons
        self.pushButton.clicked.connect(self.handle_create_staff)
        self.pushButton_2.clicked.connect(self.go_back_to_admin)

    def handle_create_staff(self):
        #Handle ENTER button click to create staff
        # Get fullname from lineEdit_3 only
        fullname = self.lineEdit_3.text().strip()
        username = self.lineEdit_4.text().strip()
        password = self.lineEdit_5.text().strip()

        # Debug: Print what we're getting
        print(f"DEBUG - Fullname: '{fullname}'")
        print(f"DEBUG - Username: '{username}'")
        print(f"DEBUG - Password: '{password}'")

        # Validation
        if not fullname:
            QMessageBox.warning(self, "Error", "Full name is required!")
            return

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and Password are required!")
            return

        # Minimum length validation
        if len(username) < 3:
            QMessageBox.warning(self, "Error", "Username must be at least 3 characters long!")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long!")
            return

        # Create staff through controller
        print(f"DEBUG - Calling controller.add_staff with fullname='{fullname}', username='{username}'")
        success, message = self.controller.add_staff(fullname, username, password)

        print(f"DEBUG - Result: success={success}, message='{message}'")

        if success:
            QMessageBox.information(self, "Success", message)
            # Clear all fields
            self.lineEdit_3.clear()  # Full name
            self.lineEdit_4.clear()  # Username
            self.lineEdit_5.clear()  # Password
            # Go back to admin window
            self.go_back_to_admin()
        else:
            QMessageBox.critical(self, "Error", message)
            # Highlight the username field if it's a duplicate username error
            if "already exists" in message:
                self.lineEdit_4.setFocus()
                self.lineEdit_4.selectAll()

    def go_back_to_admin(self):
        #Go back to admin window
        try:
            from admin.adminpov import adminwindow
            self.admin_window = adminwindow()
            self.admin_window.show()
            self.close()
        except Exception as e:
            print(f"Error opening admin window: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = createacc()
    window.show()
    sys.exit(app.exec())