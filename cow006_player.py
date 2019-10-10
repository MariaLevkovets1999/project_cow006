PLAYER_NAMES = [
    'John',
    'Bob',
    'Adam',
    'Alice',
    'Olivia',
    'Amanda',
    'Portia',
    'Charlie',
    'William',
    'Sophie',
    'Mia',
    'Isabella',
    'Emily'
]

class Player:
    """
        Класс логики игрока
    """
    def __init__(self, name, is_bot=True):
        self.name = name
        self.hand = []
        self.score = 0 
        self.fullScore = 0 
        self.is_bot = is_bot

    def init_hand(self, deck, maxhand):
        """
            Инициализация карт игрока
        """
        self.hand.clear()
        for i in range(maxhand):
            card = deck.draw()
            self.hand.append(card)

    def add_score(self, cards):
        """
            Добавление штрафных очков игроку с полученных карт
        """
        self.score += sum([card.score for card in cards])


    def add_card(self, card):
        """
            Добавление карты
        """
        self.hand.append(card)

    def choose_row(self, table, card):
        """
            Выбор (для бота) ряда с наименьшим кол-вом штрафных очков
            при невозможности положить карту
        """
        min_score = 100000
        min_index = -1
        for i, row in enumerate(table):
            score = row.get_score()
            if score < min_score:
                min_score = score
                min_index = i
        return table[min_index]

    def choose_card(self, table):
        """
            Выбор (для бота) карты, которую он положит рубашкой вверх
            Бот кладет карту с минимальной разницей между своей картой и последней картой в ряду
        
        """
        lastcards = []
        for i, row in enumerate(table):
            lastcards.append(row.top().n)
        
        B=[0]*4
        A=[[1]*len(self.hand) for i in range(4)] #Это двумерный массив из разностей последней карты в ряду и карт бота
        for j in range(4):
            for i in range(len(self.hand)):
                A[j][i]= (abs(lastcards[j]-self.hand[i].n))   
            B[j]=min(A[j])
        for h in range(4):
            if B.index(min(B)) == h:
                c = A[h].index(min(A[h]))
                card = self.hand.pop(c)



        return card

 
       
            
        #Старая версия кода, где бот берет последнюю карту
        #card = self.hand.pop()
        #return card
    
    def new_tour_score(self):
        self.fullScore +=self.score
        self.score = 0
                

    def __str__(self):
        return self.name +':'+' Штраф за тур:' + str(self.score) 

