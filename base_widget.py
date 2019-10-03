from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import sip

class BaseWidget(QWidget):
    """
        Базовый виджет для основных виджетов
        главного экрана игры. Содержит метод
        очистки виджета от виджетов, заполненных
        старыми данными.
    """
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground)

    def reset(self, layout=None):
        if layout is None:
            layout = self.layout()
        if layout:
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if item.widget():
                    item.widget().deleteLater()
                elif item.spacerItem():
                    layout.removeItem(item)
                else:
                    self.reset(item)
            sip.delete(layout)
        self.init_ui()
