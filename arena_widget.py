from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
)

from base_widget import BaseWidget
from card_widget import CardWidget

class ArenaWidget(BaseWidget):
    """
        Виджет-контейнер с областью выкладки карт рубашкой вверх в начале игры
    """
    def __init__(self, players=None):
        super().__init__()

        self.players = players


    def init_ui(self):
        koef = 0.75
        width = koef * CardWidget.STANDARD_WIDTH
        height = koef * CardWidget.STANDARD_HEIGHT
        self.card_width = width
        self.card_height = height

        layout = QGridLayout()

        for i in range(3):
            for j in range(4):
                k = 4*i + j
                if len(self.players) <= k:
                    break

                label = QLabel(self.players[k].name)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet('border: 2px dashed black;')

                player_layout = QHBoxLayout()
                player_layout.setContentsMargins(0, 0, 0, 0)
                player_layout.setSpacing(0)

                player_layout.addWidget(label)

                player_place_widget = QWidget()

                player_place_widget.setMaximumWidth(width)
                player_place_widget.setMaximumHeight(height)
                player_place_widget.setMinimumWidth(width)
                player_place_widget.setMinimumHeight(height)
                player_place_widget._name = self.players[k].name
                #player_place_widget.setMinimumWidth(50)
                #player_place_widget.setMaximumWidth(50)
                player_place_widget.setLayout(player_layout)

                layout.addWidget(player_place_widget, i, j)

        self.setLayout(layout)

    def add_card(self, player, card):
        """
            Добавление виджета-карты в область
            по игроку и логическому объекту карты
        """
        card.opened = False
        name = player.name
        options = {
            'width': self.card_width,
            'height': self.card_height
        }
        card_widget = CardWidget(card, options=options)
        items = self.layout()
        for i in range(items.count()):
            w = items.itemAt(i).widget()
            if w._name == name:
                w.layout().itemAt(0).widget().hide()
                w.layout().addWidget(card_widget)

    def remove_card(self, player):
        """
            Удаление виджета карты из контейнера для выбранного игрока
        """
        name = player.name
        items = self.layout()
        for i in range(items.count()):
            w = items.itemAt(i).widget()
            if w._name == name:
                w.layout().itemAt(0).widget().show()
                w.layout().itemAt(1).widget().deleteLater()

    def open_all(self):
        """
            Переворот всех карт в контейнере рубашкой вниз
        """
        items = self.layout()
        for i in range(items.count()):
            w = items.itemAt(i).widget()
            w.layout().itemAt(1).widget().card.opened = True
            w.layout().itemAt(1).widget().reset()

    def set_players(self, players):
        """
            Связывание объекта игроков и данного виджета для отображения данных
        """
        self.players = players
        self.reset()
