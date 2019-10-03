from cow006_player import Player
from cow006_table import Table, Row
from cow006_deck import Deck

LIMIT_SCORE = 66

class Game:
    """
        Главный класс игры. В нем происходит логика игры
        и взаимодействие других логических классов
    """
    def __init__(self, players, rows=4, maxinrow=6, maxhand=10):
        self.players = players
        self.maxhand = maxhand

        # из колоды раздают карты на стол и игрокам, больше она не нужна
        deck = Deck()
        #print(deck)
        deck.shuffle()

        self.table = Table(deck, rows, maxinrow)
        for p in self.players:
            p.init_hand(deck, maxhand)


    def run(self):
        """
            Генератор для получения игровых состояний и данных и
            проброс их в виджеты
        """
        choosen_cards = {}
        # пока не закончатся карты на руке
        for step in range(self.maxhand):
            # все игроки кладут закрытые карты
            for player in self.players:
                if player.is_bot:
                    card = player.choose_card(self.table)
                else:
                    card = yield 'HUMAN_SELECT_CARD', {}
                choosen_cards[card] = player
                data = {
                    'player': player,
                    'card': card
                }
                yield 'PLAYER_PLACE_CARD', data

            yield 'OPEN_ALL_CARDS', {}

            # карты открываются и выкладываются на стол
            for card, player in sorted(choosen_cards.items()):
                print('Resolve {} from {}'.format(card, player))
                row, index = self.table.find_row(card)

                if row is None:
                    if player.is_bot:
                        # игрок выбирает, в какой ряд положить
                        r = player.choose_row(self.table, card)
                    else:
                        data = {
                            'player': player,
                            'card': card,
                        }
                        r = yield 'HUMAN_SELECT_ROW', data
                    # кладет карту в конец ряда
                    r.add_card(card)
                    # забирает все карты, кроме последней
                    cutted = r.cut()
                    # карты, что забрал игрок, добавляются на его счет
                    player.add_score(cutted)
                    data = {
                        'player': player,
                        'card': card,
                        'row_index': self.table.get_index(r)
                    }
                    yield 'PLAYER_CANNOT_PLACE', data
                else:
                    row.add_card(card)
                    data = {
                        'player': player,
                        'card': card,
                        'row_index': index
                    }
                    yield 'PLAYER_MOVE_TO_ROW', data

                    # это шестая карта?
                    if row.overflow():
                        # забираем карты, кроме последней и добавляем их в счет игрока
                        cutted = row.cut()
                        player.add_score(cutted)
                        yield 'PLAYER_CARD_OVERFLOW', data

            choosen_cards.clear()

        state, data = self.end()
        yield state, data

    def end(self):
        """
            Обработка окончания функции run и принятие решения
            об окончании всей игры или только тура
        """
        winlist = self.players[:]
        winlist.sort(key=lambda item: item.score)
        max_score = winlist[-1].score

        if max_score < LIMIT_SCORE:
            return 'NEW_TOUR', {}
        else:
            return 'FINISH', {'winlist': winlist}
