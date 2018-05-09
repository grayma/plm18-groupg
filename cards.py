from random import shuffle

suits = ['hearts', 'diamonds', 'spades', 'clubs']
suit_abbr_map = {'h': 'hearts', 'd': 'diamonds', 's': 'spades', 'c': 'clubs'}
suit_map = {'hearts': 0, 'diamonds': 1, 'spades': 2, 'clubs': 3}
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
values_abbr_map = {'a': 'ace', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
                   '10': '10', 'j': 'jack', 'q': 'queen', 'k': 'king'}
value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 11, 'queen': 12,
             'king': 13, 'ace': 14}


def map_suit(abbr):
    return suit_abbr_map[abbr]


def map_value(card):
    return value_map[card.value]


class Card:
    """
    Wrapper for a playing card
    """

    def __init__(self, value, suit):
        """
        `value` value of the card
        `suit` suit of the card
        """

        self.value = value
        self.suit = suit

    def __repr__(self):
        return str(self.value) + "" + self.suit

    def __eq__(self, other):
        if (str(self.suit) == str(other.suit) and str(self.value) == str(other.value)):
            return True
        else:
            return False

    def abbr(self):
        return (self.value[0] if not self.value == "10" else self.value) + self.suit[0]

    def val(self):
        if(self.value == "ace"):
            return value_map["ace"]
        if (self.value == "2"):
            return value_map["2"]
        if (self.value == "3"):
            return value_map["3"]
        if (self.value == "4"):
            return value_map["4"]
        if (self.value == "5"):
            return value_map["5"]
        if (self.value == "6"):
            return value_map["6"]
        if (self.value == "7"):
            return value_map["7"]
        if (self.value == "8"):
            return value_map["8"]
        if (self.value == "9"):
            return value_map["9"]
        if (self.value == "10"):
            return value_map["10"]
        if (self.value == "jack"):
            return value_map["jack"]
        if (self.value == "queen"):
            return value_map["queen"]
        if (self.value == "king"):
            return value_map["king"]

    @staticmethod
    def from_abbr(abbr):
        if len(abbr) == 3:
            return Card('10', suit_abbr_map[abbr[2]])
        return Card(values_abbr_map[abbr[0]], suit_abbr_map[abbr[1]])


class Pile:
    """
    Pile of cards allowing transfering between piles
    """

    def __init__(self, cards):
        """
        `cards` list of cards to instantiate this pile with
        """
        self.cards = cards

    def __repr__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return self.cards.__iter__()

    def __getitem__(self, index):
        return self.cards[index]

    def pop(self):
        return self.cards.pop()

    def remove(self, c):
        self.cards.remove(c)

    def is_empty(self):
        return not self.cards

    def transfer_to(self, new_pile, subset):
        """
        Transfers a subset of this pile to another pile.
        """
        for c in subset:
            if c not in self.cards:
                raise ValueError('"subset" of pile not actually a subset.')
        self.cards = [c for c in self.cards if c not in subset]
        new_pile.cards.extend(subset)

    def sort(self):
        """
        Sort the pile of cards
        """
        self.cards.sort(key=lambda x: value_map[x.value])
        self.cards.sort(key=lambda x: suit_map[x.suit])


class Deck(Pile):
    """
    Deck of cards allowing for dealing and shuffling
    """

    def __init__(self):
        cards = [Card(value, suit) for value in values for suit in suits]
        super(Deck, self).__init__(cards)

    def deal(self, players, per_player=0):
        """
        Deal the cards in the deck to the given players
        """
        if not per_player:
            per_player = 52 // len(players)
        for p in players:
            self.transfer_to(p.hand, [self.cards[i] for i in range(per_player)])

    def shuffle(self):
        """
        Shuffle the cards in the deck
        """
        shuffle(self.cards)
