class Card:
    def __init__(i, value, suit):
        i.value = value
        i.suit = suit


suits = ['heart', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

#Standard Deck
print("Standard Deck ############################")
deck = [Card(value, suit) for value in values for suit in suits]
for card in deck:
    print(card.value)
    print(card.suit)

#2 player hearts Deck (ONLY: Aces, 2's, 4's, 6's, 8's, 10's, queens)
print("Small Deck #################################")
values = ['ace', '2', '4', '6', '8', '10', 'queen']
smalldeck = [Card(value, suit) for value in values for suit in suits]
for card in smalldeck:
    print(card.value)
    print(card.suit)
