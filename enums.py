from enum import Enum

class Suit(Enum):
    SPADES = 'S'
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'

class FaceCard(Enum):
    KING = 'K'
    QUEEN = 'Q'
    JACK = 'J'
    ACE = 'A'