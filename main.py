import sys
import sqlite3
from pathlib import Path
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Mangement System")
        self.setFixedHeight(400)
        self.setFixedWidth(425)

        # Build menu bar options
        file_menu_item = self.menuBar().addMenu("&File")
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert_student)
        file_menu_item.addAction(add_student_action)

        help_menu_item = self.menuBar().addMenu("&Help")
        help = QAction("Get Help", self)
        help_menu_item.addAction(help)

        # Build table for student data display
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "PHONE"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

    def load_data(self):
        base = Path(__file__).parent / "data"
        db_path = Path(base / "database.db")
        connection = sqlite3.connect(db_path)
        results = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)  # prevents duplicating data
        for row_num, student in enumerate(results):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(student):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        connection.close()

    def insert_student(self):
        dialog = InsertDialog(self.load_data)
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self, reload):
        super().__init__()
        self.setWindowTitle("Insert Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.load_data = reload

        layout = QVBoxLayout()

        stdnt_name = QLabel("Name")
        self.stdnt_edit_line = QLineEdit()
        self.stdnt_edit_line.setPlaceholderText("Name")
        layout.addWidget(stdnt_name)
        layout.addWidget(self.stdnt_edit_line)

        class_name = QLabel("Class")
        self.class_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.class_name.addItems(courses)

        layout.addWidget(class_name)
        layout.addWidget(self.class_name)

        phone_num = QLabel("Phone")
        self.phone_edit_line = QLineEdit()
        self.phone_edit_line.setPlaceholderText("Mobile number")
        layout.addWidget(phone_num)
        layout.addWidget(self.phone_edit_line)

        submit = QPushButton("Submit Student")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)

        # Displays the layout
        self.setLayout(layout)

    def add_student(self):
        base = Path(__file__).parent / "data"
        db_path = Path(base / "database.db")
        connection = sqlite3.connect(db_path)

        name = self.stdnt_edit_line.text()
        course = self.class_name.itemText(self.class_name.currentIndex())
        phone = self.phone_edit_line.text()
        curs = connection.cursor()
        curs.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (
                name,
                course,
                phone,
            ),
        )
        connection.commit()
        curs.close()
        connection.close()
        self.load_data()
        self.close()


def main():
    app = QApplication(sys.argv)
    sms = MainWindow()
    sms.show()
    sms.load_data()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
