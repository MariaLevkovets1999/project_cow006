import random
from cow006_card import Card
from cow006_container import Container

class Row(Container):
    def __init__(self, card, maxinrow = 6):
        print('card for row = ', card)
        self.cards = [card]
        self.maxinrow = maxinrow        # какая корова "проваливает" ряд

    def __repr__(self):
        return 'Row with cards: ' + ' '.join(map(str, self.cards))

    def __lt__(self, other):
        pass

    def top(self):
        """ возвращает последнюю карту в ряду """
        return self.cards[-1]

    def overflow(self):
        """ проверяет, есть 6 коров в ряду (True) или еще нет (False)"""
        return len(self.cards) >= self.maxinrow

    def acceptable(self, card):
         """ эту карту card можно положить в конец этого ряда? """
         return self.cards[-1].n < card.n

    def cut(self):
        """ Убирает из ряда все карты, кроме последней. Возвращает список убранных карт"""
        cards = self.cards[:-1]
        last_card = self.cards[-1]
        self.cards.clear()
        self.cards.append(last_card)
        return cards

    def get_score(self):
        return sum([card.score for card in self.cards])




class Table:
    def __init__(self, deck, rows = 4, maxinrow = 6):
        self.maxinrow = maxinrow
        self.rows = [Row(deck.draw(), maxinrow) for r in range(rows)]

    def __repr__(self):
        return '\n'.join(['Row{} : {}'.format(i, r) for i, r in enumerate(self.rows)] )

    def find_row(self, card):
        """ ищет, в какие ряды можно положить эту карту, возвращает ряд или None,
        если карту нельзя положить ни в один ряд """

        #index = random.randint(0, 3)
        index = -1
        res_row = None
        diff = 1000000
        for i, row in enumerate(self.rows):
            d = card.n - row.top().n
            if d > 0 and d < diff:
                index = i
                res_row = row
                diff = d

        return res_row, index

    def __getitem__(self, i):
        return self.rows[i]

    def get_index(self, row):
        for i, r in enumerate(self.rows):
            if r == row:
                return i
