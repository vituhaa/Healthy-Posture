import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from main_window import MainWindow

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("icons/app_icon.png"))
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
