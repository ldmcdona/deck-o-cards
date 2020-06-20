#This file exists to do testing of deck.py stuff without having to go through the sockets.
from deck import *

h = Hand()
d = Deck()

d.sort()
temp = d.deal()
h.add_card(temp)

x = h.cards[0]
x.flip()
print(x.hidden)