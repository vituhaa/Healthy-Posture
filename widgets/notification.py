from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QToolButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

from constants import FONT, MIN_PADDING, MAX_PADDING

class Notification(QWidget):
    clicked = pyqtSignal() # click notification signal
    def __init__(self, title=None, text=None):
        super().__init__()
        # notfication window design
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | # delete standard window design
                            Qt.WindowType.Tool | # do not show in task panel as an independent app
                            Qt.WindowType.WindowStaysOnTopHint) # show on top of all windows
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating) # do not move focus when opening
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # make clickable
        
        self.__icon = QIcon("icons/app_icon.png")
        self.__app_name = QLabel("Healthy Posture")
        self.__title = QLabel(title)
        self.__text = QLabel(text)
        self.__time = 3000 # 3 seconds showing
        self.__close_button = QToolButton()
        
        self.__create_main_layout()
        
    def __create_main_layout(self):
        icon_label = QLabel()
        icon_label.setPixmap(self.__icon.pixmap(16, 16))
        icon_label.adjustSize()
        
        font = QFont(FONT)
        font.setPointSize(8)
        self.__app_name.setFont(font)
        font.setPointSize(9)
        self.__text.setFont(font)
        font.setBold(True)
        self.__title.setFont(font)
        
        self.__close_button.setText("x")
        self.__close_button.setStyleSheet("QToolButton { border: none; background-color: transparent; color: black; }"
                                          "QToolButton::hover { color: gray; }"
                                          "QToolButton::pressed { color: black; }")
        self.__close_button.clicked.connect(self.hide)
        
        layout = QGridLayout()
        layout.setContentsMargins(MIN_PADDING, MIN_PADDING, MIN_PADDING, MIN_PADDING)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.addWidget(icon_label, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.__app_name, 0, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.__close_button, 0, 2, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.__title, 1, 0, 1, 2)
        layout.addWidget(self.__text, 2, 0, 1, 2)
        self.setLayout(layout)
                
    def set_title(self, title):
        self.__title.setText(title)
        
    def set_text(self, text):
        self.__text.setText(text)
         
    def show_notification(self):
        if self.__title and self.__text:
            self.adjustSize()
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry() # window geometry without tasks panel
            x = screen_geometry.right() - self.width() - MIN_PADDING
            y = screen_geometry.bottom() - self.height() - MAX_PADDING
            self.setGeometry(x, y, self.width(), self.height())
            self.show()
            QTimer.singleShot(self.__time, self.hide)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit() # send click signal
            self.hide()
        super().mousePressEvent(event)