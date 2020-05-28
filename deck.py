import random
import os

class Card:
    def __init__(self, s, v):
        self.suit = s
        self.value = v
        self.display = "X|X"

    def peak(self):
        print(self.value + "|" + self.suit)

    def flip(self):
        if self.display == "X|X":
            self.display = self.value + "|" + self.suit
        else:
            self.display = "X|X"


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
        return self.deck.pop(0)

    def replace(self, card):
        self.deck.append(card)