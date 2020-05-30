import socket
from deck import *

def commands(action, ph, sh, h):
    prime, second = ""
    if ":" in action:
        x = action.split(":")
        if x[1] == "replace":
            pass
        elif x[1] == "discard":
            pass
        elif x[1] == "flip":
            pass
        else:
            pass
    else:
        if action == "view":
            prime = ph.view()
            second = "The other player looks at their cards."
        elif action == "check":
            prime = sh.check()
            second = "The other player looks at your cards."
        elif action == "draw":
            temp = h.deal()
            if temp == "Deck is Empty.":
                prime = temp
                second = "The other player goes to draw a card, but the deck is empty."
            else:
                ph.add_card(temp)
                prime = "You draw the: " + temp.peak()
                second = "The other player draws a card."
        elif action == "shuffle":
            h.sort()
            h.shuffle()
            prime = "You refill and shuffle the deck."
            second = "The other player refills and shuffles the deck."
        elif action == "sort":
            h.sort()
            prime = "You refill the deck."
            second = "The other player refills the deck."
        elif action == "end":
            prime = "You end your turn."
            second = "The other player ends their turn."
        #elif action == "quit":
            #pass
            #Might bring back the old check system.
        else:
            #Gonna check validity on client side.
            pass
    return prime, second

def main():
    #actions = ["view", "check", "draw", "replace", "discard", "flip", "shuffle", "sort", "end"]
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
    quit = False
    while True:
        while turn == 1:
            code1, a1 = sock1.recvfrom(4096)
            code2, a2 = sock2.recvfrom(4096)
            
            if code1:
                c1 = code1.decode('utf-8')
                code1 = ""
                p1m, p2m = commands(c1, hand1, hand2, house)

            if code2:
                c2 = code2.decode('utf-8')
                if c2 == "quit":
                    m = "Player 2 has ended the game."
                    m1 = m.encode('utf-8')
                    sock1.sendto(m1, a1)
                    sock2.sendto(m1, a2)
                    quit = True
                    break
                else:
                    m = "It's not your turn."
                    m2 = m.encode('utf-8')
                    sock2.sendto(m2, a2)

                code2 = ""

        while turn == 2:
            code1, a1 = sock1.recvfrom(4096)
            code2, a2 = sock2.recvfrom(4096)
            
            if code2:
                c2 = code2.decode('utf-8')
                code2 = ""
                p2m, p1m = commands(c2, hand2, hand1, house)

            if code1:
                c1 = code1.decode('utf-8')
                if c1 == "quit":
                    m = "Player 1 has ended the game."
                    m1 = m.encode('utf-8')
                    sock1.sendto(m1, a1)
                    sock2.sendto(m1, a2)
                    quit = True
                    break
                else:
                    m = "It's not your turn."
                    m1 = m.encode('utf-8')
                    sock1.sendto(m1, a1)

                code1 = ""

        if quit == True:
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