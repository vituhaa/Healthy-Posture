from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from widgets.notification import Notification
from constants import MIN_PADDING, MAX_PADDING

class NotificationManager(QObject):
    notification_clicked = pyqtSignal() # click notification signal
    def __init__(self):
        super().__init__()
        self.__notification_categories = {} # types of notifications
        self.__screen_geometry = self.__calculate_screen_geometry()
    
    def __calculate_screen_geometry(self):
        screen = QApplication.primaryScreen()
        return screen.availableGeometry() # window geometry without tasks panel    
    
    def add_notification_category(self, category_name):
        self.__notification_categories[category_name] = Notification()
        self.__notification_categories[category_name].set_title(category_name)
        self.__notification_categories[category_name].clicked.connect(self.notification_clicked.emit)
        
    def show_notification(self, category_name, text):
        if category_name in self.__notification_categories:
            notification = self.__notification_categories[category_name]
            notification.set_text(text)
            
            x = self.__screen_geometry.right() - notification.width() - MIN_PADDING
            y = self.__screen_geometry.bottom() - notification.height() - MAX_PADDING
            notification.setGeometry(x, y, notification.width(), notification.height())
            
            self.__update_notifications_pos(notification.height())
            notification.show_notification()
    
    def __update_notifications_pos(self, height):
        for notification in self.__notification_categories.values():
            if notification.isVisible():
                notification.move(notification.pos().x(), notification.pos().y() - height - MAX_PADDING)
        
        
    def close_all_notifications(self):
        for notification in self.__notification_categories.values():
            notification.close()
            notification.deleteLater()