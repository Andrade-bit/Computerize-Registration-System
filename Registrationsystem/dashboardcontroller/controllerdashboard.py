
# controllerdashboard.py
from PyQt6.QtWidgets import QMessageBox


class DashboardController:
    def __init__(self, view):
        self.view = view
        self.model = None
        self.initialize_model()

    def initialize_model(self):
        # Initialize the Dashboard Model
        try:
            from dashboardmodel.dashboardmodel import DashboardModel
            self.model = DashboardModel()
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.model = None

    def load_statistics(self):
        # Load and display all statistics
        if not self.model:
            QMessageBox.critical(self.view, "Error", "Database connection not available!")
            return

        try:
            # Get total students
            total_students = self.model.get_total_students()
            self.view.label_total_students.setText(str(total_students))

            # Get students by grade
            grade_data = self.model.get_students_by_grade()
            self.update_grade_statistics(grade_data, total_students)

            # Get students by strand
            strand_data = self.model.get_students_by_strand()
            self.update_strand_statistics(strand_data, total_students)

            # ========== NEW CODE: UPDATE PIE CHART ==========
            # Get the counts for pie chart
            grade_11 = grade_data.get('Grade 11', 0)
            grade_12 = grade_data.get('Grade 12', 0)
            stem = strand_data.get('STEM', 0)
            humss = strand_data.get('HUMSS', 0)
            abm = strand_data.get('ABM', 0)
            gas = strand_data.get('GAS', 0)

            # Update pie chart
            pie_data = {
                "Grade 11": grade_11,
                "Grade 12": grade_12,
                "STEM": stem,
                "HUMSS": humss,
                "ABM": abm,
                "GAS": gas
            }

            # Update the pie chart widget
            self.view.pie_chart_widget.update_data(pie_data)

            # Update the legend
            self.view.legend_widget.update_counts(pie_data)

            print(f"✅ Pie chart updated with data: {pie_data}")
            # ========== END OF NEW CODE ==========

        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to load statistics: {e}")
            import traceback
            traceback.print_exc()

    def update_grade_statistics(self, grade_data, total):
        # Update grade statistics with percentages
        grade_11 = grade_data.get('Grade 11', 0)
        grade_12 = grade_data.get('Grade 12', 0)

        # Update counts
        try:
            self.view.label_grade11_count.setText(str(grade_11))
            self.view.label_grade12_count.setText(str(grade_12))
        except Exception:
            pass

        # Calculate and update percentages
        if total > 0:
            grade_11_percent = (grade_11 / total) * 100
            grade_12_percent = (grade_12 / total) * 100

            try:
                self.view.label_grade11_percent.setText(f"{grade_11_percent:.1f}%")
                self.view.label_grade12_percent.setText(f"{grade_12_percent:.1f}%")
            except Exception:
                pass
        else:
            try:
                self.view.label_grade11_percent.setText("0.0%")
                self.view.label_grade12_percent.setText("0.0%")
            except Exception:
                pass

    def update_strand_statistics(self, strand_data, total):
        # Update strand statistics with percentages
        stem = strand_data.get('STEM', 0)
        humss = strand_data.get('HUMSS', 0)
        abm = strand_data.get('ABM', 0)
        gas = strand_data.get('GAS', 0)

        # Update counts
        try:
            self.view.label_stem_count.setText(str(stem))
            self.view.label_humss_count.setText(str(humss))
            self.view.label_abm_count.setText(str(abm))
            self.view.label_gas_count.setText(str(gas))
        except Exception:
            pass

        # Calculate and update percentages
        if total > 0:
            stem_percent = (stem / total) * 100
            humss_percent = (humss / total) * 100
            abm_percent = (abm / total) * 100
            gas_percent = (gas / total) * 100

            try:
                self.view.label_stem_percent.setText(f"{stem_percent:.1f}%")
                self.view.label_humss_percent.setText(f"{humss_percent:.1f}%")
                self.view.label_abm_percent.setText(f"{abm_percent:.1f}%")
                self.view.label_gas_percent.setText(f"{gas_percent:.1f}%")
            except Exception:
                pass
        else:
            try:
                self.view.label_stem_percent.setText("0.0%")
                self.view.label_humss_percent.setText("0.0%")
                self.view.label_abm_percent.setText("0.0%")
                self.view.label_gas_percent.setText("0.0%")
            except Exception:
                pass