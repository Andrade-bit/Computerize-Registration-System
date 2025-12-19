# from PyQt6.QtWidgets import QMessageBox, QFileDialog, QRadioButton, QCheckBox, QButtonGroup
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import QDate
# from staffregistrationmodel.registrationmodel import StaffRegistrationModel
# import os
#
#
# class RegistrationController:
#     def __init__(self, registration_dialog):
#         self.registration_dialog = registration_dialog
#         self.db_model = StaffRegistrationModel()
#
#         # Store the previous form data (basic student info)
#         self.student_data = registration_dialog.registration_data or {}
#
#         # Store selected files
#         self.selected_photo = None
#         self.selected_documents = []
#
#         # Store selected values
#         self.selected_grade = None
#         self.selected_strand = None
#         self.school_year = None
#
#         # Store radio button states
#         self.radio33_clicked = False
#         self.radio34_clicked = False
#
#         # Find all radio buttons and checkboxes
#         self.strand_radio_buttons = []
#         self.grade_checkboxes = []
#
#         # Create button groups
#         self.grade_button_group = QButtonGroup()
#         self.grade_button_group.setExclusive(True)
#
#         # Connect signals
#         self.setup_connections()
#
#         # Pre-fill data from previous form if available
#         if self.student_data:
#             self.prefill_data()
#
#     def setup_connections(self):
#         """Connect UI signals to handlers"""
#         # Find all radio buttons for STRAND
#         strand_names = [
#             ('radioButton_13', 'STEM'),
#             ('radioButton_14', 'HUMSS'),
#             ('radioButton_19', 'ABM'),
#             ('radioButton_20', 'GAS'),
#         ]
#
#         for radio_name, strand_value in strand_names:
#             if hasattr(self.registration_dialog, radio_name):
#                 radio = getattr(self.registration_dialog, radio_name)
#                 self.strand_radio_buttons.append((radio, strand_value))
#                 radio.toggled.connect(lambda checked, s=strand_value: self.handle_strand_selection(checked, s))
#
#         # Grade checkboxes
#         grade_names = [
#             ('checkBox_7', 'Grade 11'),
#             ('checkBox_6', 'Grade 12'),
#         ]
#
#         for checkbox_name, grade_value in grade_names:
#             if hasattr(self.registration_dialog, checkbox_name):
#                 checkbox = getattr(self.registration_dialog, checkbox_name)
#                 self.grade_checkboxes.append((checkbox, grade_value))
#                 self.grade_button_group.addButton(checkbox)
#                 checkbox.toggled.connect(lambda checked, g=grade_value: self.handle_grade_selection(checked, g))
#
#         # Connect radioButton_33
#         if hasattr(self.registration_dialog, 'radioButton_33'):
#             self.registration_dialog.radioButton_33.toggled.connect(
#                 lambda checked: self.handle_radio33_clicked(checked)
#             )
#
#         # Connect radioButton_34
#         if hasattr(self.registration_dialog, 'radioButton_34'):
#             self.registration_dialog.radioButton_34.toggled.connect(
#                 lambda checked: self.handle_radio34_clicked(checked)
#             )
#
#         # Connect dateEdit_4 for school year
#         if hasattr(self.registration_dialog, 'dateEdit_4'):
#             self.registration_dialog.dateEdit_4.dateChanged.connect(self.handle_school_year_changed)
#
#         # Photo upload button (pushButton_5)
#         if hasattr(self.registration_dialog, 'pushButton_5'):
#             self.registration_dialog.pushButton_5.clicked.connect(self.handle_photo_upload)
#
#         # Connect pushButton_6
#         if hasattr(self.registration_dialog, 'pushButton_6'):
#             self.registration_dialog.pushButton_6.clicked.connect(self.handle_button6_clicked)
#
#         # Connect pushButton_7
#         if hasattr(self.registration_dialog, 'pushButton_7'):
#             self.registration_dialog.pushButton_7.clicked.connect(self.handle_button7_clicked)
#
#         # Finish button (pushButton_3)
#         if hasattr(self.registration_dialog, 'pushButton_3'):
#             self.registration_dialog.pushButton_3.clicked.connect(self.handle_finish)
#
#     def handle_strand_selection(self, checked, strand_value):
#         """Handle strand radio button selection"""
#         if checked:
#             self.selected_strand = strand_value
#
#     def handle_grade_selection(self, checked, grade_value):
#         """Handle grade checkbox selection"""
#         if checked:
#             self.selected_grade = grade_value
#
#     def handle_radio33_clicked(self, checked):
#         """Handle radioButton_33 click"""
#         if checked:
#             self.radio33_clicked = True
#
#     def handle_radio34_clicked(self, checked):
#         """Handle radioButton_34 click"""
#         if checked:
#             self.radio34_clicked = True
#
#     def handle_school_year_changed(self, date):
#         """Handle school year date change"""
#         self.school_year = date.toString("yyyy-MM-dd")
#
#     def handle_photo_upload(self):
#         """Handle photo upload when pushButton_5 is clicked"""
#         file_path, _ = QFileDialog.getOpenFileName(
#             self.registration_dialog,
#             "Select Photo",
#             "",
#             "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
#         )
#
#         if file_path:
#             self.selected_photo = file_path
#             self.photo_filename = os.path.basename(file_path)
#
#     def handle_button6_clicked(self):
#         """Handle pushButton_6 click"""
#         print("pushButton_6 clicked")
#
#     def handle_button7_clicked(self):
#         """Handle pushButton_7 click"""
#         print("pushButton_7 clicked")
#
#     def validate_registration_fields(self):
#         """Validate registration form fields"""
#         errors = []
#
#         # Get position and department if they exist
#         position = ""
#         department = ""
#
#         if hasattr(self.registration_dialog, 'lineEdit_position'):
#             position = self.registration_dialog.lineEdit_position.text().strip()
#
#         if hasattr(self.registration_dialog, 'lineEdit_department'):
#             department = self.registration_dialog.lineEdit_department.text().strip()
#
#         # Check grade checkboxes
#         for checkbox, grade_value in self.grade_checkboxes:
#             if checkbox.isChecked():
#                 self.selected_grade = grade_value
#                 break
#
#         if not self.selected_grade:
#             errors.append("Grade is required - Please select Grade 11 or Grade 12")
#
#         # Validate strand
#         if not self.selected_strand:
#             errors.append("Strand is required - Please select a strand")
#
#         # Validate school year
#         if not self.school_year:
#             if hasattr(self.registration_dialog, 'dateEdit_4'):
#                 date = self.registration_dialog.dateEdit_4.date()
#                 if date.isValid():
#                     self.school_year = date.toString("yyyy-MM-dd")
#                 else:
#                     errors.append("School Year is required - Please select a valid date")
#
#         # Validate photo
#         if not self.selected_photo:
#             errors.append("Photo is required - Please upload a photo")
#
#         # Collect data
#         additional_data = {
#             'position': position,
#             'department': department,
#             'grade': self.selected_grade,
#             'strand': self.selected_strand,
#             'school_year': self.school_year,
#             'photo': self.photo_filename if hasattr(self, 'photo_filename') else None,
#         }
#
#         return errors, additional_data
#
#     def handle_finish(self):
#         """Handle finish button (pushButton_3) - UPDATE STUDENT WITH REGISTRATION DETAILS"""
#         print("\n" + "=" * 50)
#         print("🚀 FINISH BUTTON PRESSED - UPDATING STUDENT RECORD!")
#         print("=" * 50)
#
#         errors, additional_data = self.validate_registration_fields()
#
#         if errors:
#             error_msg = "Please fix the following errors:\n\n" + "\n".join(f"• {error}" for error in errors)
#             QMessageBox.critical(
#                 self.registration_dialog,
#                 "Validation Error",
#                 error_msg
#             )
#             return
#
#         try:
#             # Merge basic student data with additional registration data
#             complete_data = {**self.student_data, **additional_data}
#
#             print(f"\n📝 Student Data:")
#             print(f"   Student ID: {complete_data.get('student_id')}")
#             print(f"   Name: {complete_data.get('first_name')} {complete_data.get('last_name')}")
#             print(f"   Staff ID: {complete_data.get('staff_id')}")
#             print(f"   Emergency Number: {complete_data.get('emergency_number')}")
#             print(f"   Grade: {complete_data.get('grade')}")
#             print(f"   Strand: {complete_data.get('strand')}")
#
#             # Add radio button status
#             if self.radio33_clicked:
#                 complete_data['radio33_status'] = 'yes'
#             if self.radio34_clicked:
#                 complete_data['radio34_status'] = 'yes'
#
#             # UPDATE STUDENT RECORD WITH REGISTRATION DETAILS
#             print("\n📊 Updating student in database...")
#
#             # Get the student ID
#             student_id = complete_data.get('student_id')
#
#             if not student_id:
#                 print("❌ ERROR: No student ID found in data!")
#                 QMessageBox.critical(
#                     self.registration_dialog,
#                     "Error",
#                     "Student ID not found. Please start registration from the beginning."
#                 )
#                 return
#
#             # Update the student with registration details
#             success = self.db_model.update_student_with_staff(student_id, complete_data, None)
#
#             if success:
#                 print(f"✅✅✅ SUCCESS! Updated student ID: {student_id}")
#                 print(f"✅ Staff ID saved: {complete_data.get('staff_id')}")
#
#                 # Show success message
#                 QMessageBox.information(
#                     self.registration_dialog,
#                     "🎉 Registration Complete!",
#                     f"✅ Student registration completed successfully!\n\n"
#                     f"📋 Student Details:\n"
#                     f"• Name: {complete_data.get('first_name')} {complete_data.get('last_name')}\n"
#                     f"• Emergency Number: {complete_data.get('emergency_number')}\n"
#                     f"• Grade: {complete_data.get('grade')}\n"
#                     f"• Strand: {complete_data.get('strand')}\n"
#                     f"• Student ID: {student_id}\n"
#                     f"• Registered by Staff ID: {complete_data.get('staff_id')}"
#                 )
#
#                 # Close the registration window
#                 self.registration_dialog.close()
#             else:
#                 print("❌ FAILED to update student record!")
#                 QMessageBox.critical(
#                     self.registration_dialog,
#                     "Error",
#                     "Failed to update student information in database!"
#                 )
#
#         except Exception as e:
#             print(f"\n❌❌❌ ERROR: {e}")
#             import traceback
#             traceback.print_exc()
#
#             QMessageBox.critical(
#                 self.registration_dialog,
#                 "Database Error",
#                 f"Failed to save: {str(e)}"
#             )
#
#     def prefill_data(self):
#         """Pre-fill form with data from previous form"""
#         if hasattr(self.registration_dialog, 'label_staff_name'):
#             full_name = f"{self.student_data.get('first_name', '')} "
#             if self.student_data.get('middle_name'):
#                 full_name += f"{self.student_data.get('middle_name')} "
#             full_name += self.student_data.get('last_name', '')
#             self.registration_dialog.label_staff_name.setText(full_name)
#
#         if hasattr(self.registration_dialog, 'label_staff_email'):
#             self.registration_dialog.label_staff_email.setText(
#                 self.student_data.get('email', '')
#             )
#
#         # Show the student ID if it exists
#         if hasattr(self.registration_dialog, 'label_staff_id'):
#             self.registration_dialog.label_staff_id.setText(
#                 str(self.student_data.get('student_id', ''))
#             )
#
#     def cleanup(self):
#         """Cleanup resources"""
#         if hasattr(self, 'db_model'):
#             self.db_model.close()
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QRadioButton, QCheckBox, QButtonGroup
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QDate
from staffregistrationmodel.registrationmodel import StaffRegistrationModel
import os


class RegistrationController:
    def __init__(self, registration_dialog):
        self.registration_dialog = registration_dialog
        self.db_model = StaffRegistrationModel()

        # Store the previous form data (basic student info)
        self.student_data = registration_dialog.registration_data or {}

        # Store selected files
        self.selected_photo = None
        self.selected_documents = []

        # Store selected values
        self.selected_grade = None
        self.selected_strand = None
        self.school_year = None

        # Store radio button states
        self.radio33_clicked = False
        self.radio34_clicked = False

        # Find all radio buttons and checkboxes
        self.strand_radio_buttons = []
        self.grade_checkboxes = []

        # Create button groups
        self.grade_button_group = QButtonGroup()
        self.grade_button_group.setExclusive(True)

        # Connect signals
        self.setup_connections()

        # Pre-fill data from previous form if available
        if self.student_data:
            self.prefill_data()

    def setup_connections(self):
        """Connect UI signals to handlers"""
        # Find all radio buttons for STRAND
        strand_names = [
            ('radioButton_13', 'STEM'),
            ('radioButton_14', 'HUMSS'),
            ('radioButton_19', 'ABM'),
            ('radioButton_20', 'GAS'),
        ]

        for radio_name, strand_value in strand_names:
            if hasattr(self.registration_dialog, radio_name):
                radio = getattr(self.registration_dialog, radio_name)
                self.strand_radio_buttons.append((radio, strand_value))
                radio.toggled.connect(lambda checked, s=strand_value: self.handle_strand_selection(checked, s))

        # Grade checkboxes
        grade_names = [
            ('checkBox_7', 'Grade 11'),
            ('checkBox_6', 'Grade 12'),
        ]

        for checkbox_name, grade_value in grade_names:
            if hasattr(self.registration_dialog, checkbox_name):
                checkbox = getattr(self.registration_dialog, checkbox_name)
                self.grade_checkboxes.append((checkbox, grade_value))
                self.grade_button_group.addButton(checkbox)
                checkbox.toggled.connect(lambda checked, g=grade_value: self.handle_grade_selection(checked, g))

        # Connect radioButton_33
        if hasattr(self.registration_dialog, 'radioButton_33'):
            self.registration_dialog.radioButton_33.toggled.connect(
                lambda checked: self.handle_radio33_clicked(checked)
            )

        # Connect radioButton_34
        if hasattr(self.registration_dialog, 'radioButton_34'):
            self.registration_dialog.radioButton_34.toggled.connect(
                lambda checked: self.handle_radio34_clicked(checked)
            )

        # Connect dateEdit_4 for school year
        if hasattr(self.registration_dialog, 'dateEdit_4'):
            self.registration_dialog.dateEdit_4.dateChanged.connect(self.handle_school_year_changed)

        # Photo upload button (pushButton_5)
        if hasattr(self.registration_dialog, 'pushButton_5'):
            self.registration_dialog.pushButton_5.clicked.connect(self.handle_photo_upload)

        # Connect pushButton_6
        if hasattr(self.registration_dialog, 'pushButton_6'):
            self.registration_dialog.pushButton_6.clicked.connect(self.handle_button6_clicked)

        # Connect pushButton_7
        if hasattr(self.registration_dialog, 'pushButton_7'):
            self.registration_dialog.pushButton_7.clicked.connect(self.handle_button7_clicked)

        # Finish button (pushButton_3)
        if hasattr(self.registration_dialog, 'pushButton_3'):
            self.registration_dialog.pushButton_3.clicked.connect(self.handle_finish)

    def handle_strand_selection(self, checked, strand_value):
        """Handle strand radio button selection"""
        if checked:
            self.selected_strand = strand_value

    def handle_grade_selection(self, checked, grade_value):
        """Handle grade checkbox selection"""
        if checked:
            self.selected_grade = grade_value

    def handle_radio33_clicked(self, checked):
        """Handle radioButton_33 click"""
        if checked:
            self.radio33_clicked = True

    def handle_radio34_clicked(self, checked):
        """Handle radioButton_34 click"""
        if checked:
            self.radio34_clicked = True

    def handle_school_year_changed(self, date):
        """Handle school year date change"""
        self.school_year = date.toString("yyyy-MM-dd")

    def show_upload_status(self, success, message=""):
        """Show upload status - success message or red button on failure"""
        if success:
            # Show success message
            QMessageBox.information(
                self.registration_dialog,
                "Upload Successful",
                f"✅ {message}"
            )
        else:
            # Turn button red on failure
            if hasattr(self.registration_dialog, 'pushButton_5'):
                self.registration_dialog.pushButton_5.setStyleSheet(
                    "background-color: #ff4444; color: white;"
                )

    def handle_photo_upload(self):
        """Handle photo upload when pushButton_5 is clicked"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.registration_dialog,
            "Select Photo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )

        if file_path:
            self.selected_photo = file_path
            self.photo_filename = os.path.basename(file_path)

            # Show success status
            self.show_upload_status(True, f"Photo uploaded successfully!\n\nFile: {self.photo_filename}")
        else:
            # Show failure status (turn button red)
            self.show_upload_status(False)

    def handle_button6_clicked(self):
        """Handle pushButton_6 click"""
        print("pushButton_6 clicked")

    def handle_button7_clicked(self):
        """Handle pushButton_7 click"""
        print("pushButton_7 clicked")

    def validate_registration_fields(self):
        """Validate registration form fields"""
        errors = []

        # Get position and department if they exist
        position = ""
        department = ""

        if hasattr(self.registration_dialog, 'lineEdit_position'):
            position = self.registration_dialog.lineEdit_position.text().strip()

        if hasattr(self.registration_dialog, 'lineEdit_department'):
            department = self.registration_dialog.lineEdit_department.text().strip()

        # Check grade checkboxes
        for checkbox, grade_value in self.grade_checkboxes:
            if checkbox.isChecked():
                self.selected_grade = grade_value
                break

        if not self.selected_grade:
            errors.append("Grade is required - Please select Grade 11 or Grade 12")

        # Validate strand
        if not self.selected_strand:
            errors.append("Strand is required - Please select a strand")

        # Validate school year
        if not self.school_year:
            if hasattr(self.registration_dialog, 'dateEdit_4'):
                date = self.registration_dialog.dateEdit_4.date()
                if date.isValid():
                    self.school_year = date.toString("yyyy-MM-dd")
                else:
                    errors.append("School Year is required - Please select a valid date")

        # Validate photo
        if not self.selected_photo:
            errors.append("Photo is required - Please upload a photo")

        # Collect data
        additional_data = {
            'position': position,
            'department': department,
            'grade': self.selected_grade,
            'strand': self.selected_strand,
            'school_year': self.school_year,
            'photo': self.photo_filename if hasattr(self, 'photo_filename') else None,
        }

        return errors, additional_data

    def handle_finish(self):
        """Handle finish button (pushButton_3) - UPDATE STUDENT WITH REGISTRATION DETAILS"""
        print("\n" + "=" * 50)
        print("🚀 FINISH BUTTON PRESSED - UPDATING STUDENT RECORD!")
        print("=" * 50)

        errors, additional_data = self.validate_registration_fields()

        if errors:
            error_msg = "Please fix the following errors:\n\n" + "\n".join(f"• {error}" for error in errors)
            QMessageBox.critical(
                self.registration_dialog,
                "Validation Error",
                error_msg
            )
            return

        try:
            # Merge basic student data with additional registration data
            complete_data = {**self.student_data, **additional_data}

            print(f"\n📝 Student Data:")
            print(f"   Student ID: {complete_data.get('student_id')}")
            print(f"   Name: {complete_data.get('first_name')} {complete_data.get('last_name')}")
            print(f"   Staff ID: {complete_data.get('staff_id')}")
            print(f"   Emergency Number: {complete_data.get('emergency_number')}")
            print(f"   Grade: {complete_data.get('grade')}")
            print(f"   Strand: {complete_data.get('strand')}")

            # Add radio button status
            if self.radio33_clicked:
                complete_data['radio33_status'] = 'yes'
            if self.radio34_clicked:
                complete_data['radio34_status'] = 'yes'

            # UPDATE STUDENT RECORD WITH REGISTRATION DETAILS
            print("\n📊 Updating student in database...")

            # Get the student ID
            student_id = complete_data.get('student_id')

            if not student_id:
                print("❌ ERROR: No student ID found in data!")
                QMessageBox.critical(
                    self.registration_dialog,
                    "Error",
                    "Student ID not found. Please start registration from the beginning."
                )
                return

            # Update the student with registration details
            success = self.db_model.update_student_with_staff(student_id, complete_data, None)

            if success:
                print(f"✅✅✅ SUCCESS! Updated student ID: {student_id}")
                print(f"✅ Staff ID saved: {complete_data.get('staff_id')}")

                # Show success message
                QMessageBox.information(
                    self.registration_dialog,
                    "🎉 Registration Complete!",
                    f"✅ Student registration completed successfully!\n\n"
                    f"📋 Student Details:\n"
                    f"• Name: {complete_data.get('first_name')} {complete_data.get('last_name')}\n"
                    f"• Emergency Number: {complete_data.get('emergency_number')}\n"
                    f"• Grade: {complete_data.get('grade')}\n"
                    f"• Strand: {complete_data.get('strand')}\n"
                    f"• Student ID: {student_id}\n"
                    f"• Registered by Staff ID: {complete_data.get('staff_id')}"
                )

                # Close the registration window
                self.registration_dialog.close()
            else:
                print("❌ FAILED to update student record!")
                QMessageBox.critical(
                    self.registration_dialog,
                    "Error",
                    "Failed to update student information in database!"
                )

        except Exception as e:
            print(f"\n❌❌❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

            QMessageBox.critical(
                self.registration_dialog,
                "Database Error",
                f"Failed to save: {str(e)}"
            )

    def prefill_data(self):
        """Pre-fill form with data from previous form"""
        if hasattr(self.registration_dialog, 'label_staff_name'):
            full_name = f"{self.student_data.get('first_name', '')} "
            if self.student_data.get('middle_name'):
                full_name += f"{self.student_data.get('middle_name')} "
            full_name += self.student_data.get('last_name', '')
            self.registration_dialog.label_staff_name.setText(full_name)

        if hasattr(self.registration_dialog, 'label_staff_email'):
            self.registration_dialog.label_staff_email.setText(
                self.student_data.get('email', '')
            )

        # Show the student ID if it exists
        if hasattr(self.registration_dialog, 'label_staff_id'):
            self.registration_dialog.label_staff_id.setText(
                str(self.student_data.get('student_id', ''))
            )

    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'db_model'):
            self.db_model.close()