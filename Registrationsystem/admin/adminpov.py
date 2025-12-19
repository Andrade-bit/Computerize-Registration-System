
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import sys
import os


class adminwindow(QDialog):
    def __init__(self):
        super().__init__()
        # Load UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "secondpov.ui")
        uic.loadUi(ui_path, self)

        # Initialize controller
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from admincontroller.adminpovcontroller import adminpovcontroller
        self.controller = adminpovcontroller()

        # Setup pages through controller
        self.student_table = self.controller.setup_student_review_table(self.stackedWidget)
        self.controller.setup_dashboard_page(self.stackedWidget)

        # Connect navigation buttons
        self.pushButton_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_6.clicked.connect(self.open_student_review)
        self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        # Connect Create Account buttons
        self.pushButton.clicked.connect(self.open_create_account)
        self.pushButton_2.clicked.connect(self.open_create_account)

        # Load staff data
        self.load_staff_data()

    def open_student_review(self):
        #Open student review window through controller
        self.student_review_window = self.controller.open_student_review_window(self)

    def open_create_account(self):

        self.create_acc_window = self.controller.open_create_account_window(self)

    def load_staff_data(self):

        staff_list = self.controller.get_staff_list()
        self.controller.populate_staff_table(self.tableWidget_2, staff_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = adminwindow()
    window.show()
    sys.exit(app.exec())