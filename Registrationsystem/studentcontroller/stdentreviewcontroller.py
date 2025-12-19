from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QFileDialog
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


class StudentReviewController:
    def __init__(self, view):
        self.view = view
        self.model = None
        self.initialize_model()
        self.setup_connections()
        self.load_student_data()

    def initialize_model(self):
        """Initialize the student model"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from studentmodel.modelstudent import StudentModel
            self.model = StudentModel()
        except Exception as e:
            print(f"❌ Error initializing model: {e}")
            self.model = None

    def setup_connections(self):
        """Connect all buttons to their handlers"""
        try:
            # Connect PDF button
            self.view.pushButton_6.clicked.connect(self.export_unified_summary_pdf)

            # Connect back button
            if hasattr(self.view, 'pushButton_2'):
                self.view.pushButton_2.clicked.connect(self.go_back_to_admin)
        except Exception as e:
            print(f"❌ Error setting up connections: {e}")

    def load_student_data(self):
        """Load all students from database and display in tableWidget"""
        if not self.model:
            print("❌ No model available")
            return

        try:
            from PyQt6.QtCore import Qt

            students = self.model.get_all_students()
            print(f"📊 Loaded {len(students)} students")

            # Set column count
            columns = [
                'Student ID',
                'Full Name',
                'Birth Date',
                'Sex',
                'Mobile',
                'Emergency',
                'Email',
                'Grade',
                'Strand',
                'School Year',
                'Staff ID',
                'Photo',
                'Status 33',
                'Status 34'
            ]

            self.view.tableWidget.setColumnCount(len(columns))
            self.view.tableWidget.setHorizontalHeaderLabels(columns)
            self.view.tableWidget.setRowCount(len(students))

            for row_idx, student in enumerate(students):
                # STUDENT ID (column 0)
                item = QTableWidgetItem(str(student.get('student_id', '')))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 0, item)

                # FULL NAME (column 1)
                full_name = f"{student.get('first_name', '')} {student.get('middle_name', '')} {student.get('last_name', '')}".strip()
                item = QTableWidgetItem(full_name)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 1, item)

                # BIRTH DATE (column 2)
                birth_date = str(student.get('birth_date', '')) if student.get('birth_date') else ''
                item = QTableWidgetItem(birth_date)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 2, item)

                # SEX (column 3)
                item = QTableWidgetItem(student.get('sex', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 3, item)

                # MOBILE NUMBER (column 4)
                item = QTableWidgetItem(student.get('mobile_number', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 4, item)

                # EMERGENCY NUMBER (column 5)
                item = QTableWidgetItem(student.get('emergency_number', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 5, item)

                # EMAIL (column 6)
                item = QTableWidgetItem(student.get('email', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 6, item)

                # GRADE (column 7)
                item = QTableWidgetItem(student.get('grade', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 7, item)

                # STRAND (column 8)
                item = QTableWidgetItem(student.get('strand', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 8, item)

                # SCHOOL YEAR (column 9)
                school_year = str(student.get('school_year', '')) if student.get('school_year') else ''
                item = QTableWidgetItem(school_year)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 9, item)

                # STAFF ID (column 10)
                item = QTableWidgetItem(str(student.get('staff_id', '')))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 10, item)

                # PHOTO (column 11)
                item = QTableWidgetItem(student.get('photo', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 11, item)

                # RADIO 33 STATUS (column 12)
                item = QTableWidgetItem(student.get('radio33_status', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 12, item)

                # RADIO 34 STATUS (column 13)
                item = QTableWidgetItem(student.get('radio34_status', ''))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.view.tableWidget.setItem(row_idx, 13, item)

            print(f"✅ Loaded {len(students)} students into table")

        except Exception as e:
            print(f"❌ Error loading student data: {e}")
            import traceback
            traceback.print_exc()

    def export_unified_summary_pdf(self):
        """Export unified enrollment summary report to PDF"""
        try:
            if not self.model:
                QMessageBox.warning(self.view, "Error", "Database connection not available!")
                return

            students = self.model.get_all_students()

            if not students:
                QMessageBox.warning(self.view, "No Data", "No student records found!")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Save Enrollment Summary Report",
                f"Enrollment_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return

            self.create_unified_summary_pdf(file_path, students)

            QMessageBox.information(self.view, "✓ Success",
                                    f"Enrollment Summary Report exported successfully!\n\nSaved to:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to export PDF: {e}")
            import traceback
            traceback.print_exc()

    def get_enrollment_statistics(self, students):
        """Calculate enrollment statistics from student data"""
        total_students = len(students)

        grade_counts = {'Grade 11': 0, 'Grade 12': 0}
        strand_counts = {'STEM': 0, 'HUMSS': 0, 'ABM': 0, 'GAS': 0}
        gender_counts = {'Male': 0, 'Female': 0}
        radio33_counts = {'yes': 0, 'no': 0}
        radio34_counts = {'yes': 0, 'no': 0}

        for student in students:
            # Grade count
            grade = student.get('grade', '')
            if grade in grade_counts:
                grade_counts[grade] += 1
            elif grade == '11':
                grade_counts['Grade 11'] += 1
            elif grade == '12':
                grade_counts['Grade 12'] += 1

            # Strand count
            strand = student.get('strand', '')
            if strand in strand_counts:
                strand_counts[strand] += 1

            # Gender count
            sex = student.get('sex', '')
            if sex and sex.lower() == 'male':
                gender_counts['Male'] += 1
            elif sex and sex.lower() == 'female':
                gender_counts['Female'] += 1

            # Radio button counts
            radio33 = student.get('radio33_status', '')
            if radio33 and radio33.lower() == 'yes':
                radio33_counts['yes'] += 1
            elif radio33:
                radio33_counts['no'] += 1

            radio34 = student.get('radio34_status', '')
            if radio34 and radio34.lower() == 'yes':
                radio34_counts['yes'] += 1
            elif radio34:
                radio34_counts['no'] += 1

        return {
            'total_students': total_students,
            'grade_counts': grade_counts,
            'strand_counts': strand_counts,
            'gender_counts': gender_counts,
            'radio33_counts': radio33_counts,
            'radio34_counts': radio34_counts
        }

    def create_unified_summary_pdf(self, filename, students):
        """Create comprehensive report with summary and detailed student table - ALL LANDSCAPE"""
        # Use landscape for entire document
        doc = SimpleDocTemplate(
            filename,
            pagesize=landscape(letter),
            rightMargin=30,
            leftMargin=30,
            topMargin=50,
            bottomMargin=40
        )

        elements = []
        styles = getSampleStyleSheet()

        # Color definitions
        BLUE_DARK = colors.HexColor('#2C3E50')
        BLUE_MEDIUM = colors.HexColor('#3498DB')
        GREY_MEDIUM = colors.HexColor('#95A5A6')
        GREY_LIGHT = colors.HexColor('#ECF0F1')
        WHITE = colors.white

        # ===== PAGE 1: SUMMARY STATISTICS =====
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=BLUE_DARK,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=colors.HexColor('#7F8C8D')
        )

        title = Paragraph("STUDENT ENROLLMENT REPORT", title_style)
        elements.append(title)

        report_date = Paragraph(
            f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            subtitle_style
        )
        elements.append(report_date)

        # Get statistics
        stats = self.get_enrollment_statistics(students)
        total = stats['total_students']

        # Build summary table
        summary_data = []
        summary_data.append(['CATEGORY', 'COUNT', 'PERCENTAGE'])
        summary_data.append(['═══ TOTAL ENROLLMENT ═══', str(total), '100.0%'])
        summary_data.append(['─── GRADE LEVEL ───', '', ''])

        grade_11 = stats['grade_counts']['Grade 11']
        grade_12 = stats['grade_counts']['Grade 12']

        summary_data.append([
            '   • Grade 11',
            str(grade_11),
            f"{(grade_11 / total * 100):.1f}%" if total > 0 else "0.0%"
        ])
        summary_data.append([
            '   • Grade 12',
            str(grade_12),
            f"{(grade_12 / total * 100):.1f}%" if total > 0 else "0.0%"
        ])

        summary_data.append(['─── STRAND DISTRIBUTION ───', '', ''])

        for strand_name in ['STEM', 'HUMSS', 'ABM', 'GAS']:
            count = stats['strand_counts'][strand_name]
            summary_data.append([
                f'   • {strand_name}',
                str(count),
                f"{(count / total * 100):.1f}%" if total > 0 else "0.0%"
            ])

        summary_data.append(['─── GENDER DISTRIBUTION ───', '', ''])

        male = stats['gender_counts']['Male']
        female = stats['gender_counts']['Female']

        summary_data.append([
            '   • Male',
            str(male),
            f"{(male / total * 100):.1f}%" if total > 0 else "0.0%"
        ])
        summary_data.append([
            '   • Female',
            str(female),
            f"{(female / total * 100):.1f}%" if total > 0 else "0.0%"
        ])

        summary_data.append(['─── RADIO BUTTON STATUS ───', '', ''])

        radio33_yes = stats['radio33_counts']['yes']
        radio33_no = stats['radio33_counts']['no']
        radio34_yes = stats['radio34_counts']['yes']
        radio34_no = stats['radio34_counts']['no']

        summary_data.append([
            '   • Radio 33 (Yes)',
            str(radio33_yes),
            f"{(radio33_yes / total * 100):.1f}%" if total > 0 else "0.0%"
        ])
        summary_data.append([
            '   • Radio 33 (No)',
            str(radio33_no),
            f"{(radio33_no / total * 100):.1f}%" if total > 0 else "0.0%"
        ])
        summary_data.append([
            '   • Radio 34 (Yes)',
            str(radio34_yes),
            f"{(radio34_yes / total * 100):.1f}%" if total > 0 else "0.0%"
        ])
        summary_data.append([
            '   • Radio 34 (No)',
            str(radio34_no),
            f"{(radio34_no / total * 100):.1f}%" if total > 0 else "0.0%"
        ])

        # Create summary table with landscape width
        summary_table = Table(summary_data, colWidths=[5 * inch, 2 * inch, 2 * inch])

        summary_style = [
            ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, 1), BLUE_DARK),
            ('TEXTCOLOR', (0, 1), (-1, 1), WHITE),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 12),

            ('BACKGROUND', (0, 2), (-1, 2), BLUE_MEDIUM),
            ('TEXTCOLOR', (0, 2), (-1, 2), WHITE),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),

            ('BACKGROUND', (0, 5), (-1, 5), BLUE_MEDIUM),
            ('TEXTCOLOR', (0, 5), (-1, 5), WHITE),
            ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),

            ('BACKGROUND', (0, 10), (-1, 10), BLUE_MEDIUM),
            ('TEXTCOLOR', (0, 10), (-1, 10), WHITE),
            ('FONTNAME', (0, 10), (-1, 10), 'Helvetica-Bold'),

            ('BACKGROUND', (0, 13), (-1, 13), BLUE_MEDIUM),
            ('TEXTCOLOR', (0, 13), (-1, 13), WHITE),
            ('FONTNAME', (0, 13), (-1, 13), 'Helvetica-Bold'),

            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),

            ('GRID', (0, 0), (-1, -1), 1, GREY_MEDIUM),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),

            ('BACKGROUND', (0, 3), (-1, 3), GREY_LIGHT),
            ('BACKGROUND', (0, 6), (-1, 6), GREY_LIGHT),
            ('BACKGROUND', (0, 8), (-1, 8), GREY_LIGHT),
            ('BACKGROUND', (0, 11), (-1, 11), GREY_LIGHT),
            ('BACKGROUND', (0, 14), (-1, 14), GREY_LIGHT),
            ('BACKGROUND', (0, 16), (-1, 16), GREY_LIGHT),
            ('BACKGROUND', (0, 18), (-1, 18), GREY_LIGHT),
        ]

        summary_table.setStyle(TableStyle(summary_style))
        elements.append(summary_table)
        elements.append(PageBreak())

        # ===== PAGE 2+: DETAILED STUDENT TABLE =====
        detail_title_style = ParagraphStyle(
            'DetailTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=BLUE_DARK,
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        detail_title = Paragraph("DETAILED STUDENT INFORMATION", detail_title_style)
        elements.append(detail_title)
        elements.append(Spacer(1, 0.15 * inch))

        # Prepare detailed table data with ALL columns INCLUDING STAFF ID
        detail_data = []

        # Headers - ALL DATABASE FIELDS INCLUDING STAFF ID
        headers = [
            'ID',
            'First Name',
            'M.I.',
            'Last Name',
            'Sex',
            'Birth Date',
            'Mobile',
            'Emergency',
            'Email',
            'Street',
            'Subdivision',
            'City',
            'Province',
            'Grade',
            'Strand',
            'School Year',
            'Staff ID',  # ADDED STAFF ID
            'R33',
            'R34'
        ]
        detail_data.append(headers)

        # Add all student data INCLUDING STAFF ID
        for student in students:
            row = [
                str(student.get('student_id', '') or ''),
                str(student.get('first_name', '') or ''),
                str(student.get('middle_name', '') or '')[:1] + '.' if student.get('middle_name') else '',
                str(student.get('last_name', '') or ''),
                str(student.get('sex', '') or '')[:1],
                str(student.get('birth_date', '') or '')[:10],
                str(student.get('mobile_number', '') or ''),
                str(student.get('emergency_number', '') or ''),
                str(student.get('email', '') or ''),
                str(student.get('street', '') or ''),
                str(student.get('subdivision', '') or ''),
                str(student.get('city', '') or ''),
                str(student.get('province', '') or ''),
                str(student.get('grade', '') or '').replace('Grade ', ''),
                str(student.get('strand', '') or ''),
                str(student.get('school_year', '') or '')[:10],
                str(student.get('staff_id', '') or ''),  # ADDED STAFF ID
                str(student.get('radio33_status', '') or '')[:3],
                str(student.get('radio34_status', '') or '')[:3]
            ]
            detail_data.append(row)

        # Column widths optimized for landscape - ADJUSTED FOR STAFF ID
        col_widths = [
            0.35 * inch,  # ID
            0.75 * inch,  # First Name
            0.25 * inch,  # M.I.
            0.75 * inch,  # Last Name
            0.25 * inch,  # Sex
            0.65 * inch,  # Birth Date
            0.7 * inch,  # Mobile
            0.7 * inch,  # Emergency
            1.0 * inch,  # Email
            0.8 * inch,  # Street
            0.7 * inch,  # Subdivision
            0.6 * inch,  # City
            0.6 * inch,  # Province
            0.35 * inch,  # Grade
            0.4 * inch,  # Strand
            0.65 * inch,  # School Year
            0.4 * inch,  # Staff ID - ADDED
            0.3 * inch,  # R33
            0.3 * inch  # R34
        ]

        detail_table = Table(detail_data, colWidths=col_widths, repeatRows=1)

        detail_style = [
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),

            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ID
            ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # Sex
            ('ALIGN', (13, 1), (13, -1), 'CENTER'),  # Grade
            ('ALIGN', (14, 1), (14, -1), 'CENTER'),  # Strand
            ('ALIGN', (16, 1), (16, -1), 'CENTER'),  # Staff ID - ADDED
            ('ALIGN', (17, 1), (-1, -1), 'CENTER'),  # Radio buttons
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, GREY_MEDIUM),
            ('LINEBELOW', (0, 0), (-1, 0), 2, BLUE_DARK),

            # Padding
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ]

        # Alternating row colors
        for i in range(1, len(detail_data)):
            if i % 2 == 0:
                detail_style.append(('BACKGROUND', (0, i), (-1, i), GREY_LIGHT))

        detail_table.setStyle(TableStyle(detail_style))
        elements.append(detail_table)

        # Footer
        elements.append(Spacer(1, 0.2 * inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER
        )
        footer = Paragraph(
            f"Generated from Student Registration System | Total Records: {len(students)}",
            footer_style
        )
        elements.append(footer)

        # Build PDF
        doc.build(elements, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)
        print("✅ PDF report created successfully with all data in landscape format")

    def add_page_number(self, canvas, doc):
        """Add page number to all pages"""
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(10.5 * inch, 0.3 * inch, text)
        canvas.restoreState()

    def go_back_to_admin(self):
        """Navigate back to admin window"""
        try:
            from admin.adminpov import adminwindow
            self.view.admin_window = adminwindow()
            self.view.admin_window.show()
            self.view.hide()
        except Exception as e:
            print(f"❌ Error going back to admin: {e}")

    def cleanup(self):
        """Clean up resources"""
        if self.model:
            self.model.close_connection()