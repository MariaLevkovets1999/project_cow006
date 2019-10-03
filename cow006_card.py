class Card:
    """
        Логический класс карты, содержит ее номер и штрафные очки
    """
    def __init__(self, n):
        self.n = n
        self.opened = True

        score = 1

        if self.n % 10 == 0:
            score = 3
        elif self.n % 5 == 0:
            score = 2
        elif self.n > 10 and len(set(str(self.n))) == 1:
            score = 5

        if self.n == 55:
            score = 7

        self.score = score

    def __repr__(self):
        return 'Card n={} (score={})'.format(self.n, self.score)

    def __lt__(self, other):
        return self.n < other.n

    def __eq__(self, other):
        try:
            return self.n == other.n
        except AttributeError:
            return False

    def __hash__(self):
        return self.n

    @staticmethod
    def all_cards(maxsize=104):
        """
            Создание карт для колоды, статический метод
        """
        return [Card(i+1) for i in range(maxsize)]
