from PyQt6.QtWidgets import QMessageBox
from staffRegistration.registration import StaffRegistration
from staffregistrationmodel.registrationmodel import StaffRegistrationModel


class StaffController:
    def __init__(self, staff_pov_dialog):
        self.staff_pov = staff_pov_dialog
        self.staff_registration_window = None

        # Initialize database model
        self.db_model = StaffRegistrationModel()

        # Create table if it doesn't exist
        self.db_model.create_table_if_not_exists()

        # Connect all signals
        self.setup_connections()

    def setup_connections(self):
        # Connect sex checkboxes (make them exclusive)
        self.staff_pov.checkBox_3.toggled.connect(
            lambda checked: self.handle_sex_checkbox(checked, self.staff_pov.checkBox_5)
        )
        self.staff_pov.checkBox_5.toggled.connect(
            lambda checked: self.handle_sex_checkbox(checked, self.staff_pov.checkBox_3)
        )

        # Connect proceed button
        self.staff_pov.pushButton_2.clicked.connect(self.handle_proceed)

    def handle_sex_checkbox(self, checked, other_checkbox):
        """Make sex checkboxes exclusive"""
        if checked:
            other_checkbox.setChecked(False)

    def validate_fields(self):
        """Validate all required fields"""
        errors = []

        # Get all field values
        first_name = self.staff_pov.lineEdit.text().strip()
        middle_name = self.staff_pov.lineEdit_2.text().strip()  # Optional
        last_name = self.staff_pov.lineEdit_3.text().strip()
        staff_id_input = self.staff_pov.lineEdit_4.text().strip()  # STAFF ID INPUT
        birth_date = self.staff_pov.dateEdit.date().toString("yyyy-MM-dd")
        mobile = self.staff_pov.lineEdit_7.text().strip()
        emergency_number = self.staff_pov.lineEdit_9.text().strip()
        email = self.staff_pov.lineEdit_8.text().strip()
        street = self.staff_pov.lineEdit_19.text().strip()
        city = self.staff_pov.lineEdit_21.text().strip()
        subdivision = self.staff_pov.lineEdit_20.text().strip()
        province = self.staff_pov.lineEdit_22.text().strip()

        # Check required fields
        if not first_name:
            errors.append("First Name is required")
        if not last_name:
            errors.append("Last Name is required")
        if not staff_id_input:  # VALIDATE STAFF ID
            errors.append("Staff ID is required")
        elif not staff_id_input.isdigit():
            errors.append("Staff ID must be a number")
        if not (self.staff_pov.checkBox_3.isChecked() or self.staff_pov.checkBox_5.isChecked()):
            errors.append("Please select Sex (Male or Female)")
        if not mobile:
            errors.append("Mobile Number is required")
        elif not self.validate_mobile(mobile):
            errors.append("Invalid Mobile Number format")
        if not emergency_number:
            errors.append("Emergency Number is required")
        elif not self.validate_mobile(emergency_number):
            errors.append("Invalid Emergency Number format")
        if not email:
            errors.append("Email is required")
        elif not self.validate_email(email):
            errors.append("Invalid Email format")
        if not street:
            errors.append("Street is required")
        if not city:
            errors.append("City is required")
        if not province:
            errors.append("Province is required")

        # Check if student already exists in database
        if email and mobile and not errors:
            if self.db_model.check_staff_exists(email, mobile):
                errors.append("A student with this email or mobile number already exists")

        # Collect data - INCLUDING STAFF ID
        data = {
            'first_name': first_name,
            'middle_name': middle_name if middle_name else None,
            'last_name': last_name,
            'staff_id': int(staff_id_input) if staff_id_input.isdigit() else None,  # ADD STAFF ID
            'birth_date': birth_date,
            'sex': 'Male' if self.staff_pov.checkBox_3.isChecked() else 'Female' if self.staff_pov.checkBox_5.isChecked() else None,
            'mobile_number': mobile,
            'emergency_number': emergency_number,
            'email': email,
            'street': street,
            'city': city,
            'subdivision': subdivision if subdivision else None,
            'province': province,
            'full_address': f"{street}, {city}" + (f", {subdivision}" if subdivision else "") + f", {province}"
        }

        return errors, data

    def validate_mobile(self, mobile):
        """Simple mobile number validation"""
        mobile = mobile.replace(" ", "").replace("-", "")
        return mobile.isdigit() and 10 <= len(mobile) <= 15

    def validate_email(self, email):
        """Simple email validation"""
        return '@' in email and '.' in email and len(email) > 5

    def handle_proceed(self):
        """Handle proceed button click"""
        print("\n" + "=" * 60)
        print("📝 PROCEED BUTTON CLICKED - VALIDATING AND SAVING BASIC INFO")
        print("=" * 60)

        errors, data = self.validate_fields()

        if errors:
            error_msg = "Please fix the following errors:\n\n" + "\n".join(f"• {error}" for error in errors)
            QMessageBox.critical(self.staff_pov, "Validation Error", error_msg)
            return

        try:
            print("\n💾 Saving basic student info to database...")
            print(f"📋 Data to save:")
            for key, value in data.items():
                print(f"   {key}: {value}")

            # Save basic student info to database
            student_id = self.db_model.save_staff_info(data)

            if not student_id:
                raise Exception("Failed to save student info - save_staff_info returned None")

            # Add student_id to data
            data['student_id'] = student_id

            print(f"\n✅ Basic info saved! Student ID: {student_id}")
            print(f"📦 Complete data with student_id: {data}")

            # Show success message
            self.show_success_message(data)

            # Open registration form with the data
            self.open_registration_form(data)

        except Exception as e:
            print(f"\n❌ ERROR in handle_proceed: {e}")
            import traceback
            traceback.print_exc()

            QMessageBox.critical(
                self.staff_pov,
                "Database Error",
                f"Failed to save student information:\n{str(e)}\n\n"
                f"Please check your database connection!"
            )

    def show_success_message(self, data):
        """Show success message with collected data"""
        msg = QMessageBox(self.staff_pov)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Registration Successful")

        message_text = f"Student basic information saved successfully!\n\n"
        message_text += f"Student ID: {data['student_id']}\n"
        message_text += f"Name: {data['first_name']} "
        if data['middle_name']:
            message_text += f"{data['middle_name']} "
        message_text += f"{data['last_name']}\n"
        message_text += f"Staff ID: {data['staff_id']}\n"  # SHOW STAFF ID
        message_text += f"Birth Date: {data['birth_date']}\n"
        message_text += f"Sex: {data['sex']}\n"
        message_text += f"Mobile: {data['mobile_number']}\n"
        message_text += f"Emergency Number: {data['emergency_number']}\n"
        message_text += f"Email: {data['email']}\n"
        message_text += f"Address: {data['full_address']}"

        msg.setText(message_text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def open_registration_form(self, data):
        """Open the StaffRegistration panel with the collected data"""
        print(f"\n🚀 Opening registration form with data:")
        print(f"   Student ID: {data.get('student_id')}")
        print(f"   Name: {data.get('first_name')} {data.get('last_name')}")
        print(f"   Staff ID: {data.get('staff_id')}")
        print(f"   Emergency Number: {data.get('emergency_number')}")

        # Show message to proceed to school information
        msg = QMessageBox(self.staff_pov)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Proceed to School Information")
        msg.setText("✅ Basic information saved successfully!\n\n📋 Please proceed to complete the School Information.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

        # Open new registration window with data from first form
        self.staff_registration_window = StaffRegistration(registration_data=data)
        self.staff_registration_window.show()

    def cleanup(self):
        """Cleanup database connection"""
        if hasattr(self, 'db_model'):
            self.db_model.close()