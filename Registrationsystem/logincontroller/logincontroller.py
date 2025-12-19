#controller
from loginmodel.loginmodel import DatabaseModel
from PyQt6.QtWidgets import QPushButton, QLineEdit


class logincontroller:
    def __init__(self, view):
        self.view = view
        self.model = DatabaseModel()
        self.model.connect()
        self.password_visible = False
        self.setup_password_toggle()

    def setup_password_toggle(self):
        #Add a show/hide password button to lineEdit_2
        # Create simple button with eye icon
        self.toggle_button = QPushButton("👁", self.view.lineEdit_2)
        self.toggle_button.setFixedSize(30, 23)

        # Simple style
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 3px;
            }
        """)

        # Position at right edge
        self.toggle_button.move(
            self.view.lineEdit_2.width() - 35,
            4
        )

        # Connect click
        self.toggle_button.clicked.connect(self.toggle_password_visibility)

    def toggle_password_visibility(self):
        #Toggle between showing and hiding password
        if self.password_visible:
            # Hide password - closed eye
            self.view.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_button.setText("👁")
            self.password_visible = False
        else:
            # Show password - open eye with slash
            self.view.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_button.setText("👁‍🗨")
            self.password_visible = True

    def logins(self, username, password):
        #Handle login authentication
        success, user_data = self.model.verify_login(username, password)
        return success, user_data