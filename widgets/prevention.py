from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QFont, QColor
from functools import partial
from constants import WHITE_COLOR, MIN_PADDING, MAX_PADDING, FONT
from widgets.arrow_button import ArrowButton

class PreventivePage(QWidget):
    def __init__(self):
        super().__init__()
        self.__common_recomendations = ["Каждые 40-60 минут делайте перерывы на 3-5 минут",
                                        "Соблюдайте расстояние 50-70 см от монитора",
                                        "Занимайтесь спортом: плаванием, йогой, силовыми упражнениями"]
        self.__exercises = {"Вытяжение шеи": "Медленно опустите подбородок к груди, потянитесь затылком вверх, 15-20 секунд",
                            "Ухо-плечо": "Откиньте голову назад, медленно коснитесь ухом плеча, повторите для другой стороны",
                            "Отведение подбородка": "Стоя у стены, прижмите затылок и скользите подбородком назад, 10-15 секунд",
                            "Повороты головы": "Прижмите подбородок к груди, медленно поверните голову влево и вправо, 5 раз",
                            "Вращение плечами": "Выполняйте круговые движения назад с максимальным сведением лопаток",
                            "Изометрическое напряжение": "Давите ладонью на голову, сопротивляясь рукой, 10 секунд в каждую сторону"}
        self.__common_rec_widget = None
        self.__exercises_widget = None
        self.__create_main_layout()
        
    def __create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.__create_content())
        scroll_area.setWidgetResizable(True) 
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        
    def __create_content(self):
        widget = QWidget()
        widget.setAutoFillBackground(True) # use own color
        palette = widget.palette() # get current widget palette
        palette.setColor(QPalette.ColorRole.Window, WHITE_COLOR) # background color
        widget.setPalette(palette) # apply
        
        text_font = QFont(FONT)
        text_font.setPointSize(12)
        text_font.setBold(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(MIN_PADDING, MAX_PADDING, MIN_PADDING, MAX_PADDING)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
         # common recomendations
        common_rec_layout = QHBoxLayout()
        common_rec_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        common_rec_layout.setContentsMargins(0, 0, 0, 0)
        common_rec_layout.setSpacing(MAX_PADDING)
        
        common_rec_label = QLabel("Общие рекомендации")
        common_rec_label.setFont(text_font)
        common_rec_layout.addWidget(common_rec_label)
        
        common_rec_button = ArrowButton()
        common_rec_button.set_state(True)
        common_rec_layout.addWidget(common_rec_button)
        
        layout.addLayout(common_rec_layout)
        
        self.__common_rec_widget = self.__create_common_rec_widget()
        layout.addWidget(self.__common_rec_widget, 0, Qt.AlignmentFlag.AlignLeft)
        common_rec_button.clicked.connect(lambda: self.__set_visible_widget(self.__common_rec_widget))
        
        # exercises
        exercises_layout = QHBoxLayout()
        exercises_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        exercises_layout.setContentsMargins(0, 0, 0, 0)
        exercises_layout.setSpacing(MAX_PADDING)
        
        exercises_label = QLabel("Упражнения")
        exercises_label.setFont(text_font)
        exercises_layout.addWidget(exercises_label)
        
        exercises_button = ArrowButton()
        exercises_button.set_state(True)
        exercises_layout.addWidget(exercises_button)
        
        layout.addLayout(exercises_layout)
        
        self.__exercises_widget = self.__create_exercises_widget()
        layout.addWidget(self.__exercises_widget, 0, Qt.AlignmentFlag.AlignLeft)
        exercises_button.clicked.connect(lambda: self.__set_visible_widget(self.__exercises_widget))
        
        widget.setLayout(layout)
        
        return widget
    
    def __create_common_rec_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        text_font = QFont(FONT)
        text_font.setPointSize(12)
        
        for i in range(0, len(self.__common_recomendations)):
            rec_label = QLabel(self.__common_recomendations[i])
            rec_label.setFont(text_font)
            layout.addWidget(rec_label)
            
        widget.setLayout(layout)
        return widget
    
    def __create_exercises_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MAX_PADDING)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title_font = QFont(FONT)
        title_font.setPointSize(12)
        
        text_font = QFont(FONT)
        text_font.setPointSize(11)
        text_color = QColor(WHITE_COLOR.darker(250))
        
        for key in self.__exercises:
            exercise_layout = QHBoxLayout()
            exercise_layout.setContentsMargins(0, 0, 0, 0)
            exercise_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            exercise_layout.setSpacing(MAX_PADDING)
            
            exercise_title = QLabel(key)
            exercise_title.setFont(title_font)
            exercise_layout.addWidget(exercise_title)
            
            exercise_button = ArrowButton()
            exercise_layout.addWidget(exercise_button)
            
            layout.addLayout(exercise_layout)
            
            exercise_text = QLabel(self.__exercises[key])
            exercise_text.setFont(text_font)
            exercise_text.setStyleSheet(f"QLabel {{ color: {text_color.name()}; }}")
            layout.addWidget(exercise_text, 0, Qt.AlignmentFlag.AlignLeft)
            
            exercise_button.clicked.connect(partial(self.__set_visible_widget, exercise_text))
            exercise_text.hide()
            
        widget.setLayout(layout)
        return widget
    
    def __set_visible_widget(self, widget):
        if widget.isVisible():
            widget.hide()
        else:
            widget.show()