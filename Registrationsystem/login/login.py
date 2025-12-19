from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit
import sys
import os
from loginmodel.loginmodel import DatabaseModel
from logincontroller.logincontroller import logincontroller
from staff.staffpov import StaffPOV
from admin.adminpov import adminwindow


class login(QDialog):
    def __init__(self):
        super().__init__()
        # Get the directory where login.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "loginnew1.ui")
        uic.loadUi(ui_path, self)

        # Set password field to show asterisks
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)

        self.db = DatabaseModel()
        self.controller = logincontroller(self)  # Fixed: Pass self as view parameter

        if self.db.connect():
            print("✅ Database connected!")
        else:
            print("❌ Failed to connect to database.")

        # Connect the Enter button to login function
        self.Enterbut.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username == "USER" or username.strip() == "":
            QMessageBox.warning(self, "Error", "Please enter a username")
            return

        if password == "PASSWORD" or password.strip() == "":
            QMessageBox.warning(self, "Error", "Please enter a password")
            return

        # Verify login through controller
        success, user_data = self.controller.logins(username, password)

        if success:
            role = user_data['role']
            QMessageBox.information(self, "Success", f"Welcome {user_data['username']}!")

            try:
                if role == 'admin':
                    print(f" Opening admin window for {user_data['username']}")
                    self.admin_window = adminwindow()
                    self.admin_window.show()
                elif role == 'staff':
                    print(f" Opening staff window for {user_data['username']}")
                    self.staff_window = StaffPOV()
                    self.staff_window.show()
                else:
                    QMessageBox.warning(self, "Error", "Unknown role!")
                    return

                # Close login window after successful login
                self.close()

            except Exception as e:
                print(f" Error opening window: {e}")
                QMessageBox.critical(self, "Error", f"Failed to open window: {str(e)}")
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password!")
            self.lineEdit_2.clear()  # Clear password field


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = login()
    window.show()
    sys.exit(app.exec())