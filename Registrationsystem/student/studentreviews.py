# studentreviews.py
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import sys
import os


class studends(QDialog):
    def __init__(self):
        super().__init__()
        # Get absolute path to thirdayiee.ui
        self.setFixedSize(781, 431)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "thirdayiee.ui")
        uic.loadUi(ui_path, self)

        # Initialize the controller
        from studentcontroller.stdentreviewcontroller import StudentReviewController
        self.controller = StudentReviewController(self)

    def closeEvent(self, event):
       #Handle window close event to clean up resources
        if hasattr(self, 'controller'):
            self.controller.cleanup()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = studends()
    window.show()
    sys.exit(app.exec())