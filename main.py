import sys
import sqlite3
from pathlib import Path
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QGridLayout,
    QLineEdit,
    QPushButton,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Mangement System")

        # Build menu bar options
        file_menu_item = self.menuBar().addMenu("&File")
        add_student = QAction("Add Student", self)
        file_menu_item.addAction(add_student)

        help_menu_item = self.menuBar().addMenu("&Help")
        help = QAction("Get Help", self)
        help_menu_item.addAction(help)

        # Build table for student data display
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "PHONE"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

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

        # self.table


def main():
    app = QApplication(sys.argv)
    sms = MainWindow()
    sms.show()
    sms.load_data()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
