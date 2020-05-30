import random
import os

class Card:
    def __init__(self, s, v):
        self.suit = s
        self.value = v
        self.hidden = True

    def peak(self):
        return self.value + "|" + self.suit

    def flip(self):
        if self.hidden:
            self.hidden = False
        else:
            self.hidden = True


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        for i in range(len(self.cards)):
            if card == self.cards[i]:
                self.cards.pop(i)
                break
    
    def view(self):
        message = "You have: " + len(self.cards) + " cards: "
        for card in self.cards:
            if card.hidden:
                message += "H(" + card.peak + ")"
            else:
                message += "R(" + card.peak + ")"
        return message

    def check(self):
        message = "The other player has: " + len(self.cards) + " cards: "
        for card in self.cards:
            if card.hidden:
                message += "H(X|X)"
            else:
                message += "R(" + card.peak + ")"
        return message


class Deck:
    def __init__(self):
        self.deck = []
        self.suits = ['\u2660', '\u2665', '\u2663', '\u2666'] #Spades, hearts, clubs, diamonds
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        random.seed(os.urandom(1))

    def sort(self):
        for j in range(4):
            for k in range(13):
                c = Card(self.suits[j], self.values[k])
                self.deck.append(c)
    
    def shuffle(self):
        for i in range(52):
            a = random.randint(0, 51)
            temp = self.deck[a]
            self.deck[a] = self.deck[i]
            self.deck[i] = temp

    def deal(self):
        if len(self.deck) >= 1:
            return self.deck.pop(0)
        else:
            return "Deck is Empty."

    def replace(self, card):
        self.deck.append(card)