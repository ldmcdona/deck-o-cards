import socket
from deck import *

def commands(action, ph, sh, h):
    prime, second = ""
    if " " in action:
        x = action.split(" ")
        if x[1] == "replace":
            temp = ph.cards[x[1]]
            ph.remove_card(x[1])
            h.replace(temp)
            prime = "You return the " + temp.peak + " to the deck.\n"
            second = "The other player returns a card to the bottom of the deck.\n"

        elif x[1] == "discard":
            temp = ph.cards[x[1]]
            ph.remove_card(x[1])
            prime = "You discard the " + temp.peak + "\n"
            if temp.hidden:
                second = "The other player discards a card.\n"
            else:
                second = "The other player discards the " + temp.peak + "\n"

        elif x[1] == "flip":
            ph.cards[x[1]].flip()
            if ph.cards[x[1]].hidden:
                prime = "You conceal the " + ph.cards[x[1]].peak + "\n"
                second = "The other player conceals the " + ph.cards[x[1]].peak + "\n"
            else:
                prime = "You reveal the " + ph.cards[x[1]].peak + "\n"
                second = "The other player reveals the " + ph.cards[x[1]].peak + "\n"

        else:
            print("A critical error has occured.\n")

    else:

        if action == "view":
            prime = ph.view() + "\n"
            second = "The other player looks at their cards.\n"

        elif action == "check":
            prime = sh.check() + "\n"
            second = "The other player looks at your cards.\n"

        elif action == "draw":
            temp = h.deal()

            if temp == "The deck is empty.":
                prime = temp + "\n"
                second = "The other player goes to draw a card, but the deck is empty.\n"

            else:
                ph.add_card(temp)
                prime = "You draw the: " + temp.peak() + "\n"
                second = "The other player draws a card.\n"

        elif action == "shuffle":
            h.sort()
            h.shuffle()
            prime = "You refill and shuffle the deck.\n"
            second = "The other player refills and shuffles the deck.\n"

        elif action == "sort":
            h.sort()
            prime = "You refill the deck.\n"
            second = "The other player refills the deck.\n"

        else:
            #Gonna check validity on client side.
            print("A critical error has occured.\n")

    return prime, second, ph, sh, h

def main():
    house = Deck()
    house.sort()
    house.shuffle()

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address1 = ('localhost', 10000)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address2 = ('localhost', 10001)

    sock1.bind(server_address1)
    sock2.bind(server_address2)

    while True:
        d1, a1 = sock1.recvfrom(4096)
        d2, a2 = sock2.recvfrom(4096)
        p1 = d1.decode('utf-8')
        p2 = d2.decode('utf-8')

        if p1 == "connecting" and p2 == "connecting":
            m = "Both players connected. Beginning Game."
            m1 = m.encode('utf-8')
            sock1.sendto(m1, a1)
            sock2.sendto(m1, a2)
            break

    turn = 1
    hand1 = Hand()
    hand2 = Hand()
    game_over = False

    while True:
        while turn == 1:
            code1, a1 = sock1.recvfrom(4096)
            
            if code1:
                c1 = code1.decode('utf-8')
                code1 = ""

                if c1 == "quit":
                    m = "Player 1 has quit."
                    m1 = m.encode('utf-8')
                    sock1.sendto(m1, a1)
                    sock1.sendto(m1, a2)
                    game_over = True
                    turn = 0

                elif c1 == "end":
                    player_one_message = "You end your turn."
                    player_two_message = "The other player ends their turn. It's your turn."
                    p1m = player_one_message.encode('utf-8')
                    p2m = player_two_message.encode('utf-8')
                    sock1.sendto(p1m, a1)
                    sock2.sendto(p2m, a2)
                    turn = 2

                else:
                    p1m, p2m, hand1, hand2, house = commands(c1, hand1, hand2, house)


        while turn == 2:
            code2, a2 = sock2.recvfrom(4096)
            
            if code2:
                c2 = code2.decode('utf-8')
                code2 = ""

                if c2 == "quit":
                    m = "Player 2 has quit."
                    m1 = m.encode('utf-8')
                    sock1.sendto(m1, a1)
                    sock1.sendto(m1, a2)
                    game_over = True
                    turn = 0

                elif c2 == "end":
                    player_two_message = "You end your turn."
                    player_one_message = "The other player ends their turn. It's your turn."
                    p1m = player_one_message.encode('utf-8')
                    p2m = player_two_message.encode('utf-8')
                    sock1.sendto(p1m, a1)
                    sock2.sendto(p2m, a2)
                    turn = 1

                else:
                    p2m, p1m, hand2, hand1, house = commands(c2, hand2, hand1, house)


        if game_over:
            break


    print("Test complete.")
    sock1.close()
    sock2.close()

    

main()

#https://pymotw.com/2/socket/udp.html
'''
bluuuuuurg.

Alright, bind two sockets and wait for data from em. 
1st socket is player 1, 2nd socket is player 2
Send em both messages as needed. 
'''


'''
Two people playing cards. 
Look at your hand. Look at opponents hand. Draw/Replace cards. Reveal Cards. Shuffle deck. End Turn. 
That sounds like everything unless I want to do a discard pile, but we can save that for later. 
'''