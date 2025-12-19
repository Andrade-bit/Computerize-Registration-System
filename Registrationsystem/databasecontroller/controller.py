from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from databasemodel.model import StudentDatabaseModel


class StudentDatabaseController:
    def __init__(self, table_widget):
        """
        Initialize controller with table widget

        Args:
            table_widget: The QTableWidget (tableWidget_2) to display data
        """
        self.table_widget = table_widget
        self.model = StudentDatabaseModel()
        self.setup_table()

    def setup_table(self):
        """Configure the table widget headers and properties"""
        try:
            column_names = self.model.get_column_names()
            self.table_widget.setColumnCount(len(column_names))
            self.table_widget.setHorizontalHeaderLabels(column_names)

            # Set table properties for better appearance
            header = self.table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

            # Enable alternating row colors
            self.table_widget.setAlternatingRowColors(True)

            # Select entire rows
            self.table_widget.setSelectionBehavior(
                self.table_widget.SelectionBehavior.SelectRows
            )

            # Make table read-only
            self.table_widget.setEditTriggers(
                self.table_widget.EditTrigger.NoEditTriggers
            )

            print("✅ Table setup completed")

        except Exception as e:
            print(f"❌ Error setting up table: {e}")

    def load_all_data(self):
        """Load all student data from database to tableWidget_2"""
        try:
            # Connect to database
            if not self.model.connect():
                print("❌ Failed to connect to database")
                return False

            # Get all students
            students = self.model.get_all_students()

            if not students:
                print("⚠️ No student records found")
                self.table_widget.setRowCount(0)
                return False

            # Populate the table
            self.populate_table(students)
            print(f"✅ Loaded {len(students)} students into tableWidget_2")
            return True

        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False

    def populate_table(self, data):
        """
        Populate table widget with data

        Args:
            data: List of student records (dictionaries)
        """
        try:
            # Clear existing rows
            self.table_widget.setRowCount(0)

            # Column names in order
            columns = [
                'student_id', 'first_name', 'middle_name', 'last_name', 'sex',
                'birth_date', 'mobile_number', 'email', 'street', 'subdivision',
                'city', 'province', 'grade', 'strand', 'studentdocu', 'photo',
                'staff_id', 'school_year'
            ]

            # Insert data row by row
            for row_num, row_data in enumerate(data):
                self.table_widget.insertRow(row_num)

                # Fill each column
                for col_num, col_name in enumerate(columns):
                    cell_data = row_data.get(col_name, "")

                    # Convert None to empty string
                    display_data = "" if cell_data is None else str(cell_data)

                    # Create table item
                    item = QTableWidgetItem(display_data)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    # Set item in table
                    self.table_widget.setItem(row_num, col_num, item)

            # Adjust column widths
            self.table_widget.resizeColumnsToContents()
            print(f"✅ Populated table with {len(data)} rows")

        except Exception as e:
            print(f"❌ Error populating table: {e}")

    def search_data(self, search_term, field="first_name"):
        """
        Search for students and update table

        Args:
            search_term: The text to search for
            field: The field to search in (default: "first_name")
                   Options: 'student_id', 'first_name', 'last_name', 'email', 
                           'grade', 'strand', 'city', 'province', etc.
        """
        try:
            if not search_term or search_term.strip() == "":
                # If search is empty, load all data
                self.load_all_data()
                return

            results = self.model.search_students(search_term, field)
            self.populate_table(results)
            print(f"✅ Search completed: {len(results)} results for '{search_term}'")

        except Exception as e:
            print(f"❌ Error searching data: {e}")

    def refresh_data(self):
        """Refresh the table data"""
        print("🔄 Refreshing data...")
        self.load_all_data()

    def clear_table(self):
        """Clear all data from the table"""
        self.table_widget.setRowCount(0)
        print("🗑️ Table cleared")

    def get_selected_student_id(self):
        """
        Get the student ID from selected row

        Returns:
            int: Student ID or -1 if no selection
        """
        try:
            selected_items = self.table_widget.selectedItems()
            if selected_items:
                row = selected_items[0].row()
                student_id_item = self.table_widget.item(row, 0)
                if student_id_item:
                    student_id = int(student_id_item.text())
                    print(f"✅ Selected student ID: {student_id}")
                    return student_id
            print("⚠️ No student selected")
            return -1
        except Exception as e:
            print(f"❌ Error getting selected student: {e}")
            return -1

    def get_selected_student_data(self):
        """
        Get all data from selected row

        Returns:
            dict: Student data dictionary or None
        """
        try:
            student_id = self.get_selected_student_id()
            if student_id != -1:
                return self.model.get_student_by_id(student_id)
            return None
        except Exception as e:
            print(f"❌ Error getting student data: {e}")
            return None

    def get_selected_row_data(self):
        """
        Get data from selected row as a list

        Returns:
            list: List of values from selected row or None
        """
        try:
            selected_items = self.table_widget.selectedItems()
            if not selected_items:
                print("⚠️ No row selected")
                return None

            row = selected_items[0].row()
            row_data = []

            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")

            print(f"✅ Retrieved data from row {row}")
            return row_data

        except Exception as e:
            print(f"❌ Error getting row data: {e}")
            return None

    def get_total_rows(self):
        """
        Get total number of rows in table

        Returns:
            int: Number of rows
        """
        return self.table_widget.rowCount()

    def close_connection(self):
        """Close database connection"""
        try:
            del self.model
            print("🔒 Controller closed database connection")
        except Exception as e:
            print(f"❌ Error closing connection: {e}")