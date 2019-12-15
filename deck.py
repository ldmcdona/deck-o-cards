import random
import os

class Deck():
    deck = []
    suits = ['\u2660', '\u2665', '\u2663', '\u2666'] #Spades, hearts, clubs, diamonds
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    random.seed(os.urandom(1))

    def sort(self):
        i = 0
        for j in range(4):
            for k in range(13):
                self.deck[i] = [self.suits[j], self.values[k]]
                i += 1
    
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