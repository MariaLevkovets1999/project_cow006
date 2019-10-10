#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
from PyQt5.QtCore import Qt, QRegExp, QTimer
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QDesktopWidget, QApplication, QStackedLayout,
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QLabel
)
from PyQt5.QtGui import QColor, QRegExpValidator

from cow006_game import Game
from cow006_player import Player, PLAYER_NAMES

from card_widget import CardWidget
from user_card_list_widget import UserCardListWidget
from panel_widget import PanelWidget
from arena_widget import ArenaWidget
from table_widget import TableWidget

MIN_PLAYER_AMOUNT = 2
MAX_PLAYER_AMOUNT = 10
GAME_TIMEOUT = 1000
FULL_SCREEN = False
SHORT_NEW_TOUR = False


class Window(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.init_ui()

    def init_ui(self):
        width, height = self.width, self.height
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()

        x0 = int((screen_width - width)/2)
        y0 = int((screen_height - height)/2)


        self.setGeometry(x0, y0, width, height)
        self.setWindowTitle('Корова 006')

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(190, 255, 185))
        self.setPalette(p)

        self.stacked_layout = QStackedLayout()  # стэк экранов
        self.stacked_layout.addWidget(self.init_start_screen())  # стартовый экран
        self.stacked_layout.addWidget(self.init_main_screen())  # главный экран с игрой
        self.stacked_layout.addWidget(self.init_finish_screen())  # экран результатов


        self.stacked_layout.setCurrentIndex(0)  # устанавливаем начальны нулевой экран

        main_widget = QWidget()
        main_widget.setLayout(self.stacked_layout)

        self.setCentralWidget(main_widget)

        self.game_state = "Absent"

        self.show()

    def init_start_screen(self):
        """
            Инициализатор старотового экрана с настройками
        """
        name_widget = QLineEdit()
        name_widget.setPlaceholderText("Ваше имя")
        name_widget.setStyleSheet('width: 200px;')

        #name_widget.setText('Мария')
        self.name_widget = name_widget

        number_widget = QLineEdit()
        number_widget.setPlaceholderText("Кол-во игроков")
        number_widget.setStyleSheet('width: 200px;')

        rx = QRegExp('^([2-9]|10)$')
        number_widget.setValidator(QRegExpValidator(rx))
        number_widget.setText('2')

        self.number_widget = number_widget

        start_btn = QPushButton('Старт')
        start_btn.clicked.connect(self.start_game)
        start_btn.setMaximumWidth(100)

        control_hbox = QHBoxLayout()
        control_hbox.addWidget(start_btn)


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addStretch(4)
        layout.addWidget(name_widget)
        layout.addStretch(1)
        layout.addWidget(number_widget)
        layout.addStretch(1.2)
        layout.addLayout(control_hbox)
        layout.addStretch(4)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(layout)
        hbox.addStretch(1)

        widget = QWidget()
        widget.setLayout(hbox)
        return widget

    def init_main_screen(self):
        """
            Инициализатор главного экрана игры
        """
        user_cards_scroll = UserCardListWidget()
        table_widget = TableWidget(callback=self.select_row)
        panel_widget = PanelWidget(start_game=self.start_tour, choose_card=self.choose_card)
        arena_widget = ArenaWidget()

        self.user_cards_scroll = user_cards_scroll
        self.table_widget = table_widget
        self.panel_widget = panel_widget
        self.arena_widget = arena_widget

        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        #user_cards_scroll.setMinimumWidth(self.width)  #!!!
        user_cards_scroll.setMaximumHeight(CardWidget.STANDARD_HEIGHT + 50)
        table_widget.setMinimumWidth(0.42 * self.width)
        table_widget.setMinimumHeight(self.height)  #!!!
        panel_widget.setMinimumWidth(0.2 * self.width)
        panel_widget.setMaximumWidth(0.2 * self.width)
        #user_cards_scroll.setMaximumWidth(self.width)
        #width = mainWindow.frameGeometry().width()

        selected_number_widget = QLineEdit()
        selected_number_widget.setPlaceholderText('Номер для удаления')

        h_layout = QHBoxLayout()
        #h_layout.addWidget(table_widget)  #!!!
        h_layout.addWidget(arena_widget)
        h_layout.addWidget(panel_widget)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(user_cards_scroll)

        layout = QHBoxLayout()  #!!!
        layout.addWidget(table_widget)  #!!!
        layout.addLayout(v_layout)  #!!!

        widget = QWidget()
        widget.setLayout(layout)  #!!!
        #widget.setLayout(v_layout)  #!!!

        return widget

    def init_finish_screen(self):
        """
            Инициализатор экрана с результатами игры
        """
        best_player = ''
        worst_player = ''

        header = QLabel('Игра окончена!')
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet('font-size: 30px; color: blue;')

        best_player_widget = QLabel('')
        self.finish_best_player_widget = best_player_widget
        best_player_widget.setAlignment(Qt.AlignCenter)

        worst_player_widget = QLabel('')
        self.finish_worst_player_widget = worst_player_widget
        worst_player_widget.setAlignment(Qt.AlignCenter)

        new_game_btn = QPushButton('Начать новую игру')

        def renew():
            """
                Сброс настроек игры
            """
            self.players = []
            self.game_state = 'Absent'
            self.user_cards_scroll.set_accessable(False)
            self.stacked_layout.setCurrentIndex(0)

        new_game_btn.clicked.connect(renew)

        exit_btn = QPushButton('Выход')
        exit_btn.clicked.connect(lambda: self.close())

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addStretch(10)
        layout.addWidget(header)
        layout.addStretch(4)
        layout.addWidget(best_player_widget)

        # промежуточные игроки
        self.middle_player_widgets = []
        for i in range(MAX_PLAYER_AMOUNT - 2):
            lbl = QLabel('')
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl)
            self.middle_player_widgets.append(lbl)

        layout.addWidget(worst_player_widget)
        layout.addStretch(2)
        layout.addWidget(new_game_btn)
        layout.addStretch(1)
        layout.addWidget(exit_btn)
        layout.addStretch(10)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def set_result(self, winlist):
        """
            Установка данных результата игры для конечного экрана
        """
        best_player = winlist[0]
        worst_player = winlist[-1]

        best_text = 'Звезда Коровьего Шпионажа: {}. Штрафные очки: {}'.format(best_player.name, best_player.score)
        worst_text = 'Повелитель Коров: {}. Штрафные очки: {}'.format(worst_player.name, worst_player.score)

        self.finish_best_player_widget.setText(best_text)
        self.finish_worst_player_widget.setText(worst_text)

        for lbl in self.middle_player_widgets:
            lbl.setHidden(True)

        for i, player in enumerate(winlist[1:-1]):
            text = 'Середнячок - {}. Штрафные очки: {}'.format(player.name, player.score)
            self.middle_player_widgets[i].setText(text)
            self.middle_player_widgets[i].setHidden(False)

    def init_game(self, name, amount):
        """
            Инициализация игры: создание игрока-человек с именем name и
            amount компьютерных игроков, создание объекта игры с колодой
            и всеми параметрами
        """
        user = Player(name, is_bot=False)

        player_names = PLAYER_NAMES.copy()
        random.shuffle(player_names)
        players = [user]
        players.extend([Player(name) for name in player_names[:amount-1]])
        #players.append(user)
        self.players = players

        self.game = Game(players)

    def start_game(self):
        """
            Обработка нажатия кнопки старта игры на начальном экране.
            Проверка введенных данных и переход на экран игры.
        """
        name = self.name_widget.text().strip()
        player_amount = int(self.number_widget.text() or 0)

        if not name:
            self.show_warn('Вы не ввели имя!', 'Ошибка имени')
            return

        if name.capitalize() in PLAYER_NAMES:
            self.show_warn('Данное имя зарезервированно!', 'Ошибка имени')
            return

        if not MIN_PLAYER_AMOUNT <= player_amount <= MAX_PLAYER_AMOUNT:
            self.show_warn(
                'Кол-во игроков должно быть от {} до {}!'.format(MIN_PLAYER_AMOUNT, MAX_PLAYER_AMOUNT),
                'Ошибка кол-ва игроков'
            )
            return

        self.init_game(name, player_amount)  # инициализация игры

        self.init_game_widgets()

        self.stacked_layout.setCurrentIndex(1)  # переход на главный экран

    def init_game_widgets(self):
        """
            Установка значений для основных виджетов главного экрана
        """
        self.user_cards_scroll.set_user(self.get_user())
        self.table_widget.set_table(self.game.table)
        self.panel_widget.set_players(self.players)
        self.arena_widget.set_players(self.players)

    def _show_modal(self, text, title, type):
        """
            Обобщенная функция создания модального окна
            для различных типов сообщений
        """
        if type == 'warn':
            typeWidget = QMessageBox.Warning
        elif type == 'info':
            typeWidget = QMessageBox.Information

        msgBox = QMessageBox()
        msgBox.setIcon(typeWidget)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        return msgBox.exec()

    def show_warn(self, text, title=''):
        return self._show_modal(text, title, 'warn')

    def show_info(self, text, title=''):
        return self._show_modal(text, title, 'info')

    def start_tour(self):
        """
            Обработка состояния начала нового тура
        """
        for player in self.players:
            player.new_tour_score()
        self.user_cards_scroll.set_accessable(True)
        self.panel_widget.start_btn_hide()
        self.run = self.game.run()
        self.game_state = 'BEGIN'
        self.step()



    def finish_tour(self):
        """
            Обработка состояния окончания тура
        """
        for player in self.players:
            player.new_tour_score()
        r = self.show_info('Тур окончен!\nНачинаем новый тур!')
        self.game = Game(self.players)
        
        self.init_game_widgets()
        for player in self.players:
            player.new_tour_score()


        if SHORT_NEW_TOUR:
            self.start_tour()
            
        else:
            self.user_cards_scroll.set_accessable(False)
            self.panel_widget.start_btn_show()


    def handle_finish(self, winlist):
        """
            Обработка окончания игры для установки результатов в виджеты
            на последнем виджете
        """
        self.set_result(winlist)
        self.stacked_layout.setCurrentIndex(2)

    def step(self, val=None):
        """
            Шаг игры. Взаимодействует с объектом game и генератором run,
            получая один из вариантов и обрабатывая его соответствующим образом.
            После чего эта функция step вызывается снова для продолжения
            работы генератора.
        """
        try:
            if val is None:
                state, data = next(self.run)
            else:
                state, data = self.run.send(val)
            self.game_state = state
            if state == 'PLAYER_PLACE_CARD':
                player = data['player']
                card = data['card']
                self.arena_widget.add_card(player, card)
                QTimer.singleShot(GAME_TIMEOUT, self.step)
            elif state == 'HUMAN_SELECT_CARD':
                self.panel_widget.set_action_label_state(1)
                self.panel_widget.choose_card_btn_show()
            elif state == 'OPEN_ALL_CARDS':
                self.arena_widget.open_all()
                QTimer.singleShot(1.8 * GAME_TIMEOUT, self.step)
            elif state == 'PLAYER_MOVE_TO_ROW':
                player = data['player']
                card = data['card']
                row_index = data['row_index']
                self.arena_widget.remove_card(player)
                #if row_index > -1:
                self.table_widget.add_card(row_index, card)
                QTimer.singleShot(GAME_TIMEOUT, self.step)
            elif state == 'PLAYER_CARD_OVERFLOW':
                player = data['player']
                row_index = data['row_index']
                self.table_widget.overflow_row(row_index)
                self.show_info('Переполнение для ' + player.name + '!')
                self.panel_widget.reset_scores()
                QTimer.singleShot(GAME_TIMEOUT, self.step)
            elif state == 'PLAYER_CANNOT_PLACE':
                player = data['player']
                card = data['card']
                row_index = data['row_index']
                self.arena_widget.remove_card(player)
                self.table_widget.add_card(row_index, card)
                def func():
                    self.table_widget.overflow_row(row_index)
                    self.panel_widget.reset_scores()
                    QTimer.singleShot(GAME_TIMEOUT, self.step)
                QTimer.singleShot(GAME_TIMEOUT, func)
            elif state == 'HUMAN_SELECT_ROW':
                player = data['player']
                card = data['card']
                self.panel_widget.set_action_label_state(2)
                self.show_info('Для карты нет подходящего ряда!\nВыберите штрафной ряд.')
            elif state == 'NEW_TOUR':
                self.finish_tour()
            elif state == 'FINISH':
                winlist = data['winlist']
                self.handle_finish(winlist)



        except StopIteration:
            print('Finish!')

    def choose_card(self):
        """
            Обработка пользовательского события выбора карты
            на этапе сброса карт игры рубашкой вверх
        """
        if self.game_state != 'HUMAN_SELECT_CARD':
            return
        widget = None
        widgets = self.user_cards_scroll.layout().itemAt(0).widget().widget().layout()
        for i in range(widgets.count()):
            w = widgets.itemAt(i).widget()
            if w.selected:
                widget = w
                break

        if widget:
            card = widget.card
            user = self.get_user()
            self.user_cards_scroll.remove_card(card.n)
            self.panel_widget.choose_card_btn_hide()
            QTimer.singleShot(0.1 * GAME_TIMEOUT, lambda: self.step(card))
            return True
        else:
            self.show_warn('Вы не выбрали карту!')
            return False



    def select_row(self, i, row):
        """
            Обработка пользовательского события выбора ряда для взятия
            при невозможности положить карту
        """
        if self.game_state == 'HUMAN_SELECT_ROW':
            self.panel_widget.set_action_label_state(0)
            QTimer.singleShot(0, lambda: self.step(row))


    def get_user(self):
        """
            Получение текущего пользователя
        """
        return [player for player in self.players if not player.is_bot][0]



if __name__ == '__main__':
    if FULL_SCREEN:
        kw = 1
        kh = 1
    else:
        kw = 0.9
        kh = 0.75

    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()

    width, height = kw * size.width(), kh * size.height()
    CardWidget.define_standard_size(0.084 * width, 0.22 * height)
    #CardWidget.define_standard_size(width / 10, height / 4)
    ex = Window(width, height)
    if FULL_SCREEN:
        ex.showFullScreen()
    sys.exit(app.exec_())
