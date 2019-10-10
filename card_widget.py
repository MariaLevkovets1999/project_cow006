import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)

from base_widget import BaseWidget

class CardWidget(BaseWidget):
    """
        Виджет для карты
    """
    STANDARD_WIDTH = 100
    STANDARD_HEIGHT = 140
    def __init__(self, card, options={}, clickable=False):
        super().__init__()
        self.card = card
        self.width = options.get('width') or self.STANDARD_WIDTH
        self.height = options.get('height') or self.STANDARD_HEIGHT

        self.clickable = clickable
        self.selected = False

        self.setObjectName("container_widget")

        self.init_ui()

    def init_ui(self):
        card = self.card
        if card.opened:
            number_widget = QLabel(str(card.n))
            number_widget.setStyleSheet("color: black; font-weight: bold; font-size: 30px;")
            number_widget.setAlignment(Qt.AlignCenter)

            score_widget = QLabel(str(card.score))
            score_widget.setStyleSheet("color:black ; font-size: 20px;")
            score_widget.setAlignment(Qt.AlignCenter)

            score_layout = QHBoxLayout()
            score_layout.addStretch(1)
            score_layout.addWidget(score_widget)
            score_layout.addStretch(10)

            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignCenter)

            layout.addStretch(0)
            layout.addLayout(score_layout)
            layout.addStretch(2)
            layout.addWidget(number_widget)
            layout.addStretch(10)

            self.setLayout(layout)

            self.setStyleSheet("#container_widget {background-color: #d342ff; border: 2px solid black; color: blue;}")
        else:
            self.setStyleSheet("#container_widget {background-color: green; border: 1px solid gray;}")

        width, height = self.width, self.height

        
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.resize(width, height)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)




        self.selected = False
        stretch_param = 6

        if self.clickable:
            def on_card_click(event=None):
                if self.parent().parent().parent().parent().objectName() == 'user_card_list_widget':
                    last_func_name = sys._getframe(1).f_code.co_name
                    current_func_name = sys._getframe(0).f_code.co_name
                    for i in range(self.parent().layout().count()):
                        w = self.parent().layout().itemAt(i).widget()
                        if w.selected and w != self and last_func_name != current_func_name:
                            w.mouseReleaseEvent()

                x0 = self.pos().x()
                y0 = self.pos().y()

                d = stretch_param
                if not self.selected:
                    self.selected = True
                    old_rect = QRect(x0, y0, width, height)
                    new_rect = QRect(x0 - d, y0 - d, width + 2*d, height + 2*d)
                else:
                    self.selected = False
                    old_rect = QRect(x0, y0, width + 2*d, height + 2*d)
                    new_rect = QRect(x0 + d, y0 + d, width, height)

                #container_widget.setGeometry(rect)
                self.anim = QPropertyAnimation(self, b"geometry")
                self.anim.setDuration(150)
                self.anim.setStartValue(old_rect)
                self.anim.setEndValue(new_rect)
                self.anim.start()

            self.mouseReleaseEvent = on_card_click

    def set_card(self, card):
        """
            Связывание объекта карты и виджета для отображения данных
        """
        self.card = card
        self.reset()

    @classmethod
    def define_standard_size(cls, width, height):
        """
            Метода класса для переопределения
            стандартных размеров карты
        """
        cls.STANDARD_WIDTH = width
        cls.STANDARD_HEIGHT = height
