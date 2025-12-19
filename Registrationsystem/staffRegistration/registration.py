from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import sys
import os


class StaffRegistration(QDialog):
    def __init__(self, registration_data=None):
        super().__init__()
        # Get absolute path to registration.ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "registration.ui")
        uic.loadUi(ui_path, self)

        # Store registration data if provided (from previous form)
        self.registration_data = registration_data

        # Initialize the controller
        from staffregistrationcontroller.registrationcontroller import RegistrationController
        self.controller = RegistrationController(self)

        # Display previous form data if available
        if registration_data:
            self.display_registration_data(registration_data)

    def display_registration_data(self, data):
        """Display registration data from previous form"""
        # You can add labels to your UI to show this information
        print(f"Previous form data received: {data}")
        # Example usage if you add labels:
        # self.label_student_name.setText(f"{data['first_name']} {data['last_name']}")
        # self.label_student_email.setText(data['email'])

    def closeEvent(self, event):
        """Handle window close event"""
        if hasattr(self, 'controller'):
            self.controller.cleanup()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StaffRegistration()
    window.show()
    sys.exit(app.exec())