
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
import sys
from databasecontroller.controller import StudentDatabaseController


class MainWindow(QDialog):  # Changed from QMainWindow to QDialog
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load the UI file
        uic.loadUi('FOURTH.ui', self)

        # Initialize the database controller with tableWidget_2
        self.db_controller = StudentDatabaseController(self.tableWidget_2)

        # Load all data when window opens
        self.load_database_data()

        # Connect signals (if you have these buttons/widgets in your UI)
        # Uncomment and modify based on your UI elements:

        # If you have a refresh button:
        # self.pushButton_refresh.clicked.connect(self.refresh_table)

        # If you have a search box:
        # self.lineEdit_search.textChanged.connect(self.search_students)

        # If you want to handle row selection:
        # self.tableWidget_2.itemSelectionChanged.connect(self.on_row_selected)

    def load_database_data(self):
        """Load all student data into tableWidget_2"""
        success = self.db_controller.load_all_data()
        if success:
            print("✅ Database loaded successfully into tableWidget_2")
        else:
            QMessageBox.warning(self, "Database Error",
                                "Failed to load student data from database")

    def refresh_table(self):
        """Refresh the table data"""
        self.db_controller.refresh_data()

    def search_students(self):
        """Search students based on input"""
        search_term = self.lineEdit_search.text()
        # You can change 'first_name' to search by other fields:
        # Options: 'student_id', 'last_name', 'email', 'grade', 'strand', etc.
        self.db_controller.search_data(search_term, field="first_name")

    def on_row_selected(self):
        """Handle when a row is selected in the table"""
        student_id = self.db_controller.get_selected_student_id()
        if student_id != -1:
            print(f"Selected student ID: {student_id}")

            # Get full student data if needed
            student_data = self.db_controller.get_selected_student_data()
            if student_data:
                print(f"Student name: {student_data['first_name']} {student_data['last_name']}")

    def closeEvent(self, event):
        """Handle window close event"""
        self.db_controller.close_connection()
        print("🔒 Application closed, database connection terminated")
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()