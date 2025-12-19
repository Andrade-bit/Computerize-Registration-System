
#controller
import math
import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt6.QtWidgets import QFrame, QWidget

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adminmodel.adminmodel import adminmodel


class adminpovcontroller:
    def __init__(self):
        self.model = adminmodel()

    def get_staff_list(self):
        # Get all staff from database through model
        return self.model.get_all_staff()

    def populate_staff_table(self, table_widget, staff_list):
        # Populate the staff table with data
        from PyQt6.QtWidgets import QTableWidgetItem

        try:
            table_widget.setRowCount(len(staff_list))

            for row_idx, staff in enumerate(staff_list):
                table_widget.setItem(row_idx, 0, QTableWidgetItem(staff['name']))
                table_widget.setItem(row_idx, 1, QTableWidgetItem(staff['username']))
                table_widget.setItem(row_idx, 2, QTableWidgetItem(staff['password']))

            print(f"✅ Loaded {len(staff_list)} staff members into table")
            return True
        except Exception as e:
            print(f"Error populating staff table: {e}")
            import traceback
            traceback.print_exc()
            return False

    def setup_student_review_table(self, stacked_widget):
        # Setup student review table in page_2 of stacked widget
        from PyQt6.QtWidgets import QTableWidget, QVBoxLayout, QWidget

        try:
            page2_widget = QWidget()
            page2_widget.setStyleSheet("background-color: #ffffff;")

            student_table = QTableWidget()
            student_table.setColumnCount(7)
            student_table.setHorizontalHeaderLabels([
                "FULL NAME", "DATE OF BIRTH", "SEX", "MOBILE NUMBER",
                "EMAIL ADDRESS", "STRAND CHOOSEN", "STUDENT ID"
            ])
            student_table.horizontalHeader().setDefaultSectionSize(104)

            layout = QVBoxLayout(page2_widget)
            layout.setContentsMargins(30, 40, 30, 40)
            layout.addWidget(student_table)

            old_page2 = stacked_widget.widget(1)
            stacked_widget.removeWidget(old_page2)
            stacked_widget.insertWidget(1, page2_widget)

            print("✅ Student review page setup complete")
            return student_table
        except Exception as e:
            print(f"Error setting up student review page: {e}")
            import traceback
            traceback.print_exc()
            return None

    def setup_dashboard_page(self, stacked_widget):
        """Setup dashboard page in the stacked widget"""
        from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel,
                                     QGroupBox, QGridLayout, QWidget, QScrollArea,
                                     QFrame)
        from PyQt6.QtCore import Qt, QRect
        from PyQt6.QtGui import QFont, QPainter, QColor, QBrush, QPen
        import math

        try:
            # Create scroll area for dashboard
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("""
                QScrollArea { 
                    border: none; 
                    background-color: #ffffff;
                }
            """)

            dashboard_widget = QWidget()
            dashboard_widget.setStyleSheet("background-color: #ffffff;")

            main_layout = QVBoxLayout(dashboard_widget)
            main_layout.setContentsMargins(30, 40, 30, 40)
            main_layout.setSpacing(20)

            # Title
            title = QLabel("📊 Student Registration Dashboard")
            title_font = QFont()
            title_font.setPointSize(18)
            title_font.setBold(True)
            title.setFont(title_font)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(title)

            # Student Registration Pie Chart
            pie_group = QGroupBox("📈 Student Registration Statistics")
            pie_group.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            pie_group.setStyleSheet("""
                QGroupBox {
                    border: 2px solid #2196F3;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 10px 0 10px;
                    color: #2196F3;
                }
            """)

            pie_layout = QHBoxLayout()
            pie_layout.setContentsMargins(20, 20, 20, 20)

            # Create pie chart widget
            pie_chart_widget = PieChartWidget()
            pie_layout.addWidget(pie_chart_widget, 1)

            # Create legend widget
            legend_widget = self.create_legend_widget()
            pie_layout.addWidget(legend_widget, 0)

            pie_group.setLayout(pie_layout)
            main_layout.addWidget(pie_group)

            # Total Students Counter (Centered)
            total_layout = QHBoxLayout()
            total_layout.addStretch()

            total_container = QFrame()
            total_container.setStyleSheet("""
                QFrame {
                    background-color: #E3F2FD;
                    border: 2px solid #2196F3;
                    border-radius: 10px;
                    padding: 15px;
                }
            """)

            total_inner_layout = QVBoxLayout(total_container)
            total_inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            total_label = QLabel("Total Registered Students")
            total_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            total_label.setStyleSheet("color: #1565C0;")
            total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            total_inner_layout.addWidget(total_label)

            label_total_students = QLabel("0")
            label_total_students.setFont(QFont("Arial", 28, QFont.Weight.Bold))
            label_total_students.setStyleSheet("color: #2196F3;")
            label_total_students.setAlignment(Qt.AlignmentFlag.AlignCenter)
            total_inner_layout.addWidget(label_total_students)

            total_layout.addWidget(total_container)
            total_layout.addStretch()

            main_layout.addLayout(total_layout)

            # Grade Level Group
            grade_group = QGroupBox("📚 Grade Level Distribution")
            grade_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            grade_layout = QGridLayout()

            grade_layout.addWidget(QLabel("Grade 11:"), 0, 0)
            label_grade11_count = QLabel("0")
            grade_layout.addWidget(label_grade11_count, 0, 1)
            label_grade11_percent = QLabel("0.0%")
            label_grade11_percent.setStyleSheet("color: #4CAF50; font-weight: bold;")
            grade_layout.addWidget(label_grade11_percent, 0, 2)

            grade_layout.addWidget(QLabel("Grade 12:"), 1, 0)
            label_grade12_count = QLabel("0")
            grade_layout.addWidget(label_grade12_count, 1, 1)
            label_grade12_percent = QLabel("0.0%")
            label_grade12_percent.setStyleSheet("color: #4CAF50; font-weight: bold;")
            grade_layout.addWidget(label_grade12_percent, 1, 2)

            grade_group.setLayout(grade_layout)
            main_layout.addWidget(grade_group)

            # Strand Distribution Group
            strand_group = QGroupBox("🎓 Strand Distribution")
            strand_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            strand_layout = QGridLayout()

            strand_layout.addWidget(QLabel("STEM:"), 0, 0)
            label_stem_count = QLabel("0")
            strand_layout.addWidget(label_stem_count, 0, 1)
            label_stem_percent = QLabel("0.0%")
            label_stem_percent.setStyleSheet("color: #FF9800; font-weight: bold;")
            strand_layout.addWidget(label_stem_percent, 0, 2)

            strand_layout.addWidget(QLabel("HUMSS:"), 1, 0)
            label_humss_count = QLabel("0")
            strand_layout.addWidget(label_humss_count, 1, 1)
            label_humss_percent = QLabel("0.0%")
            label_humss_percent.setStyleSheet("color: #FF9800; font-weight: bold;")
            strand_layout.addWidget(label_humss_percent, 1, 2)

            strand_layout.addWidget(QLabel("ABM:"), 2, 0)
            label_abm_count = QLabel("0")
            strand_layout.addWidget(label_abm_count, 2, 1)
            label_abm_percent = QLabel("0.0%")
            label_abm_percent.setStyleSheet("color: #FF9800; font-weight: bold;")
            strand_layout.addWidget(label_abm_percent, 2, 2)

            strand_layout.addWidget(QLabel("GAS:"), 3, 0)
            label_gas_count = QLabel("0")
            strand_layout.addWidget(label_gas_count, 3, 1)
            label_gas_percent = QLabel("0.0%")
            label_gas_percent.setStyleSheet("color: #FF9800; font-weight: bold;")
            strand_layout.addWidget(label_gas_percent, 3, 2)

            strand_group.setLayout(strand_layout)
            main_layout.addWidget(strand_group)

            main_layout.addStretch()

            scroll_area.setWidget(dashboard_widget)

            # Add to stacked widget at index 2
            if stacked_widget.count() > 2:
                old_page = stacked_widget.widget(2)
                stacked_widget.removeWidget(old_page)
                stacked_widget.insertWidget(2, scroll_area)
            else:
                stacked_widget.addWidget(scroll_area)

            print("✅ Dashboard page setup complete at index 2")

            # Initialize dashboard controller with labels
            from dashboardcontroller.controllerdashboard import DashboardController

            # Create a dummy object to hold the labels
            class DashboardHolder:
                pass

            holder = DashboardHolder()
            holder.label_total_students = label_total_students
            holder.label_grade11_count = label_grade11_count
            holder.label_grade11_percent = label_grade11_percent
            holder.label_grade12_count = label_grade12_count
            holder.label_grade12_percent = label_grade12_percent
            holder.label_stem_count = label_stem_count
            holder.label_stem_percent = label_stem_percent
            holder.label_humss_count = label_humss_count
            holder.label_humss_percent = label_humss_percent
            holder.label_abm_count = label_abm_count
            holder.label_abm_percent = label_abm_percent
            holder.label_gas_count = label_gas_count
            holder.label_gas_percent = label_gas_percent

            # Add the pie chart widget
            holder.pie_chart_widget = pie_chart_widget
            holder.legend_widget = legend_widget

            # Create dummy labels for compatibility
            from PyQt6.QtWidgets import QLabel
            holder.label_male_count = QLabel("0")
            holder.label_female_count = QLabel("0")
            holder.label_male_percent = QLabel("0.0%")
            holder.label_female_percent = QLabel("0.0%")
            holder.label_docs_complete = QLabel("0")
            holder.label_docs_incomplete = QLabel("0")
            holder.label_docs_complete_percent = QLabel("0.0%")
            holder.label_docs_incomplete_percent = QLabel("0.0%")

            dashboard_controller = DashboardController(holder)
            dashboard_controller.load_statistics()

            return True
        except Exception as e:
            print(f"Error setting up dashboard page: {e}")
            import traceback
            traceback.print_exc()
            return False

    def create_legend_widget(self):
        """Create a legend widget for the pie chart"""
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont, QPainter, QColor

        class LegendWidget(QWidget):
            def __init__(self):
                super().__init__()
                self.setMinimumWidth(200)

                layout = QVBoxLayout(self)
                layout.setContentsMargins(10, 10, 10, 10)
                layout.setSpacing(8)

                # Legend title
                title = QLabel("Legend")
                title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                title.setStyleSheet("color: #333;")
                title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(title)

                # Add a line separator
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet("background-color: #ddd;")
                layout.addWidget(line)

                # Create legend items for each category
                self.legend_items = {}
                categories = [
                    ("Grade 11", "#4CAF50"),
                    ("Grade 12", "#2196F3"),
                    ("STEM", "#FF5722"),
                    ("HUMSS", "#9C27B0"),
                    ("ABM", "#FF9800"),
                    ("GAS", "#00BCD4")
                ]

                for category, color in categories:
                    item_layout = QHBoxLayout()

                    # Color box
                    color_box = QLabel()
                    color_box.setFixedSize(20, 20)
                    color_box.setStyleSheet(f"background-color: {color}; border: 1px solid #666; border-radius: 3px;")

                    # Category label
                    label = QLabel(category)
                    label.setFont(QFont("Arial", 9))
                    label.setStyleSheet("color: #333;")

                    # Count label
                    count_label = QLabel("0")
                    count_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
                    count_label.setStyleSheet(f"color: {color};")
                    count_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                    item_layout.addWidget(color_box)
                    item_layout.addWidget(label)
                    item_layout.addStretch()
                    item_layout.addWidget(count_label)

                    layout.addLayout(item_layout)

                    # Store reference to count label
                    self.legend_items[category] = count_label

                layout.addStretch()

            def update_counts(self, counts):
                """Update the counts in the legend"""
                for category, count in counts.items():
                    if category in self.legend_items:
                        self.legend_items[category].setText(str(count))

        return LegendWidget()

    def open_student_review_window(self, parent_window):
        # Open student review window
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from student.studentreviews import studends
            student_review_window = studends()
            student_review_window.show()
            parent_window.hide()
            return student_review_window
        except Exception as e:
            print(f"Error opening student review: {e}")
            import traceback
            traceback.print_exc()
            return None

    def open_create_account_window(self, parent_window):
        # Open create account window
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from createstaffs.createastaffs import createacc
            create_acc_window = createacc()
            create_acc_window.show()
            parent_window.close()
            return create_acc_window
        except Exception as e:
            print(f"Error opening create account: {e}")
            import traceback
            traceback.print_exc()
            return None


class PieChartWidget(QWidget):
    """Pie chart widget to show student registrations"""

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(250)
        self.data = {
            "Grade 11": 0,
            "Grade 12": 0,
            "STEM": 0,
            "HUMSS": 0,
            "ABM": 0,
            "GAS": 0
        }
        self.colors = {
            "Grade 11": "#4CAF50",
            "Grade 12": "#2196F3",
            "STEM": "#FF5722",
            "HUMSS": "#9C27B0",
            "ABM": "#FF9800",
            "GAS": "#00BCD4"
        }

    def update_data(self, data):
        """Update the chart with new data"""
        self.data = data
        self.update()

    def paintEvent(self, event):
        """Draw the pie chart"""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get widget dimensions
        width = self.width()
        height = self.height()

        # Calculate pie chart dimensions
        diameter = min(width, height) - 40
        center_x = width // 2
        center_y = height // 2
        radius = diameter // 2

        # Draw only if we have data
        total = sum(self.data.values())
        if total == 0:
            # Draw empty state
            painter.setFont(QFont("Arial", 12))
            painter.setPen(QPen(QColor("#999")))
            painter.drawText(0, 0, width, height,
                             Qt.AlignmentFlag.AlignCenter, "No data available")
            return

        # Calculate start angle and draw slices
        start_angle = 0
        for category, value in self.data.items():
            if value > 0:
                # Calculate slice angle (360 degrees * percentage)
                slice_angle = int(360 * 16 * (value / total))

                # Draw pie slice
                color = self.colors.get(category, "#2196F3")
                painter.setBrush(QBrush(QColor(color)))
                painter.setPen(QPen(QColor("#333"), 1))
                painter.drawPie(center_x - radius, center_y - radius,
                                diameter, diameter, start_angle, slice_angle)

                # Draw percentage label in the middle of each slice
                if value / total >= 0.05:  # Only show label for slices >= 5%
                    percentage = (value / total) * 100
                    mid_angle = start_angle + (slice_angle // 2)
                    mid_angle_deg = mid_angle / 16  # Convert from 1/16th degrees

                    # Calculate label position
                    label_radius = radius * 0.6
                    label_x = center_x + label_radius * math.cos(math.radians(mid_angle_deg))
                    label_y = center_y - label_radius * math.sin(math.radians(mid_angle_deg))

                    # Draw percentage
                    painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
                    painter.setPen(QPen(QColor("#fff")))
                    percent_text = f"{percentage:.1f}%"

                    # Adjust text position based on angle for better readability
                    text_width = painter.fontMetrics().horizontalAdvance(percent_text)
                    text_height = painter.fontMetrics().height()

                    if 45 <= mid_angle_deg <= 135:  # Top half
                        painter.drawText(int(label_x - text_width / 2),
                                         int(label_y - text_height / 2),
                                         percent_text)
                    elif 225 <= mid_angle_deg <= 315:  # Bottom half
                        painter.drawText(int(label_x - text_width / 2),
                                         int(label_y + text_height / 2),
                                         percent_text)
                    else:  # Sides
                        painter.drawText(int(label_x - text_width / 2),
                                         int(label_y - text_height / 2),
                                         percent_text)

                start_angle += slice_angle

        # Draw center circle (donut chart effect)
        painter.setBrush(QBrush(QColor("#fff")))
        painter.setPen(QPen(QColor("#fff"), 1))
        center_radius = radius // 3
        painter.drawEllipse(center_x - center_radius, center_y - center_radius,
                            center_radius * 2, center_radius * 2)

        # Draw total count in center
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        painter.setPen(QPen(QColor("#333")))
        total_text = str(total)
        text_width = painter.fontMetrics().horizontalAdvance(total_text)
        text_height = painter.fontMetrics().height()
        painter.drawText(int(center_x - text_width / 2),
                         int(center_y - text_height / 2),
                         total_text)

        painter.end()