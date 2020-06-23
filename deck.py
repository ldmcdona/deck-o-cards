import random
import os

#Card is passed a character for suit and value.
#Cards are meant to be passed around, not take action themselves.
#Only sub-functions are to return their value|suit, and toggle 'hidden'.
class Card:
    def __init__(self, s, v):
        self.suit = s
        self.value = v
        self.hidden = True

    #Return string of value|suit.
    def peak(self):
        return self.value + "|" + self.suit

    #Toggle 'hidden' boolean.
    def flip(self):
        if self.hidden:
            self.hidden = False
        else:
            self.hidden = True

#Player's hand. Passed nothing initially.
#Hands hold cards, allowing them to be added, removed, viewed, checked, and flipped.
#Sub-functions either return a card or a message, with the exception of 'add_card'.
class Hand:
    def __init__(self):
        self.cards = []

    #Add 'card' to the hand.
    def add_card(self, card):
        self.cards.append(card)

    #Remove Card at 'index' from hand and return it.
    def remove_card(self, index):
        temp = self.cards.pop(index)
        return temp
    
    #Return a string of all cards in you hand.
    def view(self):
        x = str(len(self.cards))
        message = "You have: " + x + " cards: "
        for card in self.cards:
            y = card.peak()
            if card.hidden:
                message += "H(" + y + ") "
            else:
                message += "R(" + y + ") "
        return message

    #Return a string of all cards in the other players hand.
    #Will only show value|suit of Cards with 'hidden' == False.
    def check(self):
        x = str(len(self.cards))
        message = "The other player has: " + x + " cards: "
        for card in self.cards:
            if card.hidden:
                message += "H(X|X) "
            else:
                y = card.peak()
                message += "R(" + y + ") "
        return message

    #Tells card at index 'i' to toggle it's 'hidden' boolean.
    #Returns card.
    def flip(self, i):
        temp = self.cards[int(i)]
        temp.flip()
        return temp

#The game deck. Passed nothing initially. 
#The deck is where the Cards come from and can be returned to.
#Either returns a card or states that it's empty. 
#Uses os and random to shuffle.
class Deck:
    def __init__(self):
        self.deck = []
        self.suits = ['\u2660', '\u2665', '\u2663', '\u2666'] #Spades, hearts, clubs, diamonds.
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        random.seed(os.urandom(1))

    #Creates a standard deck (no jokers) in uniform order.
    def sort(self):
        for j in range(4):
            for k in range(13):
                c = Card(self.suits[j], self.values[k])
                self.deck.append(c)
    
    #Attempts to shuffle the deck through RNG index swapping.
    def shuffle(self):
        for i in range(52):
            a = random.randint(0, 51)
            temp = self.deck[a]
            self.deck[a] = self.deck[i]
            self.deck[i] = temp

    #If the deck has cards, return the first card.
    #Else, send a message.
    def deal(self):
        if len(self.deck) >= 1:
            return self.deck.pop(0)
        else:
            return "The deck is empty."

    #Adds 'card' to the bottom of the deck.
    def replace(self, card):
        self.deck.append(card)