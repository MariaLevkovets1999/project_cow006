from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)

from base_widget import BaseWidget

class PanelWidget(BaseWidget):
    """
        Виджет игры с очками игроков и кнопками управления
    """
    def __init__(self, players=None, start_game=None, choose_card=None):
        super().__init__()
        self.players = players
        self.start_game = start_game
        self.choose_card = choose_card

    def init_ui(self):
        self.setObjectName("panel_widget")
        self.setStyleSheet("#panel_widget {background: #f36223;}")

        score_layout = QVBoxLayout()
        score_widget = QWidget()

        for player in self.players:
            player_lbl = QLabel(str(player))
            score_layout.addWidget(player_lbl)

        score_widget.setLayout(score_layout)
        self.score_widget = score_widget

        self.action_label = QLabel()
        self.action_label.setAlignment(Qt.AlignCenter)
        self.action_label.setStyleSheet('font-size: 14px; color: blue;')
        self.action_label.setHidden(True)


        layout = QVBoxLayout()
        layout.addWidget(score_widget)
        layout.addStretch(10)
        layout.addWidget(self.action_label)


        if self.start_game:
            def on_click_start_btn():
                self.choose_card_btn_show()
                self.start_game()

            start_btn = QPushButton('Старт')
            start_btn.clicked.connect(on_click_start_btn)
            self.start_btn = start_btn
            layout.addWidget(start_btn)

        if self.choose_card:
            def on_click_choose_card_btn():
                if self.choose_card():
                    self.choose_card_btn_hide()
                    self.set_action_label_state(0)

            choose_card_btn = QPushButton('Выбрать карту')
            choose_card_btn.setHidden(True)
            choose_card_btn.clicked.connect(on_click_choose_card_btn)
            self.choose_card_btn = choose_card_btn
            layout.addWidget(choose_card_btn)

        #layout.setContentsMargins(0, 0, 0, 0);
        self.setLayout(layout)

    def reset_scores(self):
        """
            Изменение текстовых данных
            в виджетах для обновления информации
            о штрафных очках игроков
        """
        layout = self.score_widget.layout()
        for i in range(layout.count()):
            w = layout.itemAt(i).widget()
            w.setText(str(self.players[i]))

    def choose_card_btn_show(self):
        """
            Показать кнопку выбора карты
        """
        self.choose_card_btn.setHidden(False)

    def choose_card_btn_hide(self):
        """
            Спрятать кнопку выбора карты
        """
        self.choose_card_btn.setHidden(True)

    def start_btn_show(self):
        """
            Показать кнопку страта игры
        """
        self.start_btn.setHidden(False)

    def start_btn_hide(self):
        """
            Спрятать кнопку страта игры
        """
        self.start_btn.setHidden(True)

    def set_action_label_state(self, state):
        """
            Изменить текстовое поле с сообщением пользователю
            о необходимых действиях:
            0 - сообщение отсутствует
            1 - нужно выбрать карту
            2 - нужно выбрать ряд при невозможности положить карту
        """
        if state == 0:
            self.action_label.setHidden(True)
        else:
            if state == 1:
                self.action_label.setText('Выберите карту')
            elif state == 2:
                self.action_label.setText('Выберите ряд для взятия')
            self.action_label.setHidden(False)

    def set_players(self, players):
        """
            Связывание объекта игроков и данного виджета для отображения данных
        """
        self.players = players
        self.reset()
