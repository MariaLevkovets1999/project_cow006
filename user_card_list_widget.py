from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
    QGraphicsOpacityEffect, QScrollArea
)

from base_widget import BaseWidget
from card_widget import CardWidget

class UserCardListWidget(BaseWidget):
    """
        Виджет текущих карт игрока-человека.
        Визуальная обертка для списка карт.
    """
    def __init__(self, user=None):
        super().__init__()

        self.user = user

        self.setObjectName("user_card_list_widget")
        self.set_accessable(False)

    def init_ui(self):

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        user = self.user
        #self.setStyleSheet("background-color: #aaf;")

        user_cards_scroll = QScrollArea()
        user_cards_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        user_cards_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        user_cards_scroll.setWidgetResizable(True)
        #self.user_cards_scroll = user_cards_scroll

        user_cards_layout = QHBoxLayout()
        self.user_cards_layout = user_cards_layout
        user_cards_layout.setContentsMargins(10, 15, 10, 15);

        for card in user.hand:
            card_widget = CardWidget(card, clickable=True)
            user_cards_layout.addWidget(card_widget)
            card_widget.setEnabled(False)


        widget = QWidget()
        user_cards_layout.setAlignment(Qt.AlignCenter)
        #widget.setMinimumWidth(self.frameGeometry().width() - 2)
        widget.setLayout(user_cards_layout)
        widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        widget.resize(widget.sizeHint());
        #self.user_cards_scroll_widget = widget
        user_cards_scroll.setWidget(widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0);
        layout.addWidget(user_cards_scroll)
        self.setLayout(layout)

    def get_cards(self):
        """
            Получение списка виджетов-карт
        """
        if hasattr(self, 'user_cards_layout'):
            return (self.user_cards_layout.itemAt(i) for i in range(self.user_cards_layout.count()))
        else:
            return []

    def remove_card(self, number):
        """
            Удаление виджета карты из контейнера по ее номеру
        """
        items = self.get_cards()
        for w in items:
            if w.widget().card.n == number:
                w.widget().deleteLater()

    def set_user(self, user):
        """
            Установка новых виджетов-карт для нового пользователя
        """
        self.user = user
        self.reset()

    def set_accessable(self, value):
        """
            Переключатель для изменения состояния возможности взаимодействовать с виджетом
        """
        for card in self.get_cards():
            card.widget().setEnabled(value)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.transparent)
        op = QGraphicsOpacityEffect(self)
        if value:
            op.setOpacity(1.0)
        else:
            op.setOpacity(0.4)
        self.setGraphicsEffect(op)
        #self.setAutoFillBackground(False)
        self.setPalette(p)
