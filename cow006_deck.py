from random import shuffle
from cow006_card import Card

class Deck:
    """
        Класс колоды
    """
    def __init__(self):
        self.cards = Card.all_cards()

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __str__(self):
        return '\n'.join([str(card) for card in self.cards])
