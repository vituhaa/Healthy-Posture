import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from main_window import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
