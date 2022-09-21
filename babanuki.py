import random

class Dealer():

    def __init__(self, *args):
        self.initial_deck = self.create_initial_deck()
        self.players = self.initial_deal(*args)
        for i in range(len(self.players)):
            self.players[i].deck = self.initial_putdown(self.players[i].deck)

    def create_initial_deck(self) -> list:
        """
        トランプのリストを作成。
        4種 * 13枚 + X(joker) = 計53枚 
        """
        initial_deck = [i for i in range(2, 11)] + ['A', 'J', 'Q', 'K']
        initial_deck = initial_deck * 4
        initial_deck.append('X')
        print(initial_deck)
        print(len(initial_deck))
        return initial_deck


    def initial_deal(self, *args) -> list:
        """
        各プレイヤーにトランプを分配する。
        """
        players = list(args)
        random.shuffle(self.initial_deck)
        q, mod = divmod(len(self.initial_deck), len(players))
        for i in range(len(players)):
            slice_n = q
            if i < mod:
                slice_n = q + 1
            players[i].deck = self.initial_deck[:slice_n]
            del self.initial_deck[:slice_n]
        return players


    def initial_putdown(self, deck) -> list:
        """
        ペアのトランプを捨てる。
        """
        while len(set(deck)) != len(deck):
            poped_card = deck.pop(0)
            if poped_card in deck:
                deck.remove(poped_card)
            else:
                deck.append(poped_card)
        return deck


class Player():
    """
    プレイヤー インスタンスを作成。
    """
    def __init__(self, name, is_auto=True):
        self.name = name
        self.deck = []
        self.card_exists = True
        self.is_auto = is_auto

    def __repr__(self):
        return self.name + ' Object'


class Babanuki():

    def __init__(self, players, passer_i = 0):
        self.players = players
        self.passer_i = passer_i
        self.taker_i = self.passer_i + 1
        self.passer = self.players[self.passer_i]
        self.taker = self.players[self.taker_i]
        self.rank = []
        for player in self.players:
            self.check_is_zero(player)  

    def create_turn_index(self) -> None:
        """
        プレイヤーがトランプを渡す、引く順番を生成。
        """
        def decide_turn_index(turn_i, players, check_equal = None) -> int:
            """
            プレイヤーがトランプを渡す、引く順番が正しいか判定。
            """
            while True:
                if turn_i >= len(players):
                    turn_i = 0
                    continue
                if not players[turn_i].card_exists:
                    turn_i += 1
                    continue
                if turn_i == check_equal:
                    turn_i += 1
                    continue
                break
            return turn_i

        self.passer_i = self.taker_i
        self.passer_i = decide_turn_index(self.passer_i, self.players)
        self.taker_i = self.passer_i + 1
        self.taker_i = decide_turn_index(
            self.taker_i, self.players, check_equal=self.passer_i)


    def select(self) -> str:
        """
        トランプを選択する。
        """
        if self.taker.is_auto:
            select_index = random.randrange(len(self.passer.deck))
        else:
            print(f' ==> Your cards {self.taker.deck}', end='')
            while True:
                text = ''
                for n in range(len(self.passer.deck)):
                    text += f'[{n+1}] '
                select_index = input(
                    f'\n\n\tSelect card of {self.passer.name} from {text}: ')
                try:
                    select_index = int(select_index) - 1
                    if select_index < 0 or select_index >= len(self.passer.deck):
                        raise IndexError()
                except ValueError:
                    print('\t*please input intger!!!')
                except IndexError:
                    print('\t*please input right number!!!')
                else:
                    break
            print(f'\tChoose the "{self.passer.deck[select_index]}"', end='')
            print('\t', end='')
        selected_card = self.passer.deck.pop(select_index)
        return selected_card

    def putdown_or_add(self, selected_card):
        """
        ペアのトランプがあれば排除。
        ペアにならない場合は、追加。
        """
        try:
            self.taker.deck.remove(selected_card)
        except ValueError:
            self.taker.deck.append(selected_card)

    def check_is_zero(self, player: Player) -> None:
        """
        プレイヤーのトランプが0枚であるか確認。
        """
        if len(player.deck) == 0:
            player.card_exists = False
            self.rank.append(player.name)

    def run(self):
        """
        ババ抜き開始。
        """
        self.passer_i = self.passer_i - 1
        self.taker_i = self.taker_i - 1

        loop = 0
        print('GAME START')

        while len(self.players) - len(self.rank) > 1:
            loop += 1
            print(f'\n[TURN {loop}]', end='')

            self.create_turn_index()

            self.passer = self.players[self.passer_i]
            self.taker = self.players[self.taker_i]

            print(f'\t{self.passer.name} --> {self.taker.name}', end='')

            text = '\t\t'
            for player in self.players:
                text += f'{player.name}:{len(player.deck)} '
            print(text, end='')

            selected_card = self.select()
            self.check_is_zero(self.passer)

            self.putdown_or_add(selected_card)
            self.check_is_zero(self.taker)

            text = '==> '
            for player in self.players:
                text += f'{player.name}:{len(player.deck)} '
            print(text, end='')

            print(f'\tWINNERS: {",".join(self.rank)}')

        player_name = [p.name for p in self.players if p.card_exists][0]
        self.rank.append(player_name)

        print('\n\nBABANUKI GAME END\n')
        for i, name in enumerate(self.rank):
            print(f'RANK {i+1}: {name}')

## test
# player1 = Player('中野', is_auto=False)
# player2 = Player('田中')
# player3 = Player('武田')

# dealer = Dealer(player1, player2, player3)

# babanuki = Babanuki(dealer.players)
# babanuki.run()

