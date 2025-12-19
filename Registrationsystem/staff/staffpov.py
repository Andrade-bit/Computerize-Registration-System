# from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication, QDialog
# import sys
# import os
#
#
# class staffpov(QDialog):
#     def __init__(self):
#         super().__init__()
#         # Get absolute path to FOURTH.ui
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         ui_path = os.path.join(current_dir, "FOURTH.ui")
#         uic.loadUi(ui_path, self)
#
#
# if __name__ == "__main__":
#     from staffpovcontroller.controllerstaff import StaffController
#
#     app = QApplication(sys.argv)
#     window = staffpov()
#
#     # Initialize the controller with the view
#     controller = StaffController(window)
#
#     window.show()
#     sys.exit(app.exec())

##########################
# from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication, QDialog
# import sys
# import os
#
#
# class staffpov(QDialog):
#     def __init__(self):
#         super().__init__()
#         # Get absolute path to FOURTH.ui
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         ui_path = os.path.join(current_dir, "FOURTH.ui")
#         uic.loadUi(ui_path, self)
#
#         # Initialize the controller HERE so it works from login too!
#         from staffpovcontroller.controllerstaff import StaffController
#         self.controller = StaffController(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = staffpov()
#     window.show()
#     sys.exit(app.exec())

####################
# #staffpov
# from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication, QDialog
# import sys
# import os
#
#
# class staffpov(QDialog):
#     def __init__(self):
#         super().__init__()
#         # Get absolute path to FOURTH.ui
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         ui_path = os.path.join(current_dir, "FOURTH.ui")
#         uic.loadUi(ui_path, self)
#
#         # Initialize the controller HERE so it works from login too!
#         from staffcontroller.controllerstaff import StaffController
#         self.controller = StaffController(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = staffpov()
#     window.show()
#     sys.exit(app.exec())
# #staffpov
# from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication, QDialog
# import sys
# import os
#
#
# class staffpov(QDialog):
#     def __init__(self):
#         super().__init__()
#         # Get absolute path to FOURTH.ui
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         ui_path = os.path.join(current_dir, "FOURTH.ui")
#         uic.loadUi(ui_path, self)
#
#         # Initialize the controller HERE so it works from login too!
#         from staffcontroller.controllerstaff import StaffController
#         self.controller = StaffController(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = staffpov()
#     window.show()
#     sys.exit(app.exec())
#
# # staff/staffpov.py
# from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication, QDialog
# import sys
# import os
#
#
# class StaffPOV(QDialog):
#     def __init__(self):
#         super().__init__()
#         # Get absolute path to FOURTH.ui
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         ui_path = os.path.join(current_dir, "FOURTH.ui")
#         uic.loadUi(ui_path, self)
#
#         # Initialize the controller HERE so it works from login too!
#         from staffcontroller.controllerstaff import StaffController
#         self.controller = StaffController(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = StaffPOV()
#     window.show()
#     sys.exit(app.exec())
# # staff/staffpov.py
# from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication, QDialog
# import sys
# import os
#
#
# class StaffPOV(QDialog):
#     def __init__(self):
#         super().__init__()
#         # Get absolute path to FOURTH.ui
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         ui_path = os.path.join(current_dir, "FOURTH.ui")
#         uic.loadUi(ui_path, self)
#
#         # Initialize the controller HERE so it works from login too!
#         from staffcontroller.controllerstaff import StaffController
#         self.controller = StaffController(self)
#
#         self.pushButton_2.clicked.connect(self.controller.open_registration_form)
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = StaffPOV()
#     window.show()
#     sys.exit(app.exec())
# staff/staffpov.py
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import sys
import os


class StaffPOV(QDialog):
    def __init__(self):
        super().__init__()
        # Get absolute path to FOURTH.ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "FOURTH.ui")

        if not os.path.exists(ui_path):
            print(f"❌ UI file not found: {ui_path}")
            raise FileNotFoundError(f"UI file not found: {ui_path}")

        uic.loadUi(ui_path, self)
        print(f"✅ Loaded UI from: {ui_path}")

        # Initialize the controller
        from staffcontroller.controllerstaff import StaffController
        self.controller = StaffController(self)

    def closeEvent(self, event):
        """Handle window close event"""
        if hasattr(self, 'controller'):
            self.controller.cleanup()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StaffPOV()
    window.show()
    sys.exit(app.exec())