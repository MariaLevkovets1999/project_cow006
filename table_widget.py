import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QScrollArea
)

from base_widget import BaseWidget
from card_widget import CardWidget

class TableWidget(BaseWidget):
    """
        Виджет-контейнер для рядов карт, которые образуются в процессе игры
    """
    def __init__(self, table=None, callback=None):
        super().__init__()
        self.table = table
        self.callback = callback or (lambda i, row: None)

        self.setObjectName("table_widget")

    def init_ui(self):
        self.setStyleSheet("#table_widget {background: blue; max-width: 500px;}")
        #self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #self.setMinimumWidth(400)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.rows = []

        for i, row in enumerate(self.table.rows):
            row_layout = QVBoxLayout()
            row_layout.setAlignment(Qt.AlignTop)
            for card in row:
                card_widget = CardWidget(card)
                row_layout.addWidget(card_widget)

            row_layout.setSpacing(0);
            row_layout.setContentsMargins(2, 0, 2, 0);
            self.rows.append(row_layout)
            row_widget = QWidget()
            #row_widget.setStyleSheet('background-color: red;')
            row_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            print('!!!row = ', row)
            row_widget.mouseReleaseEvent = lambda evt, i=i, row=row: self.callback(i, row)
            row_widget.setLayout(row_layout)
            layout.addStretch(1)
            layout.addWidget(row_widget)
        layout.addStretch(1)

        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(True)
        self.scroll_area = scroll_area

        layout.setSpacing(2);
        layout.setContentsMargins(2, 6, 2, 2);

        w = QWidget()
        w.setLayout(layout)
        scroll_area.setWidget(w)

        container_layout = QVBoxLayout()
        container_layout.addWidget(scroll_area)
        container_layout.setContentsMargins(0, 0, 0, 0);
        self.setLayout(container_layout)

    def scroll_to_bottom(self):
        """
            Скроллинг вниз области, используется, когда добавляется новая карта в ряд
        """
        scroll_area_max = self.scroll_area.verticalScrollBar().maximum()
        self.scroll_area.verticalScrollBar().setValue(scroll_area_max);

    def add_card(self, row_index, card):
        """
            Добавить карту в ряд
        """
        card_widget = CardWidget(card)
        self.rows[row_index].addWidget(card_widget)
        QTimer.singleShot(100, self.scroll_to_bottom)

    def overflow_row(self, row_index):
        """
            Обработка переполнения ряда - удаление всех карт, кроме последней
        """
        layout = self.rows[row_index]
        for i in range(layout.count() - 1):
            layout.itemAt(i).widget().deleteLater()

    def set_table(self, table):
        """
            Связывание объекта таблицы и данного виджета для отображения данных
        """
        self.table = table
        self.reset()
