import random

from cow006_card import Card

class Container:
    """
        Контейнер для карт, реализует базовые методы для работы с ними
    """
    def __init__(self):
        self.cards = []

    def add_card(self, c):
        self.cards.append(c)

    def draw(self):
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, i):
        return self.cards[i]

    def __repr__(self):
        return ''

def test1():
    deck = Container()
    deck.add(Card(44))
    deck.add(Card(5))
    deck.add(Card(81))

    print(deck)
