import socket
from deck import *

#The 'commands' function handles everything to do with cards, hands, deck, and actions.
#It is passed a string 'action', two hands, 'ph' and 'sh', and the deck, 'h'.
#It returns a message for the primary player, 'prime', a message for the secondary player, 'second', both hands, and the deck.
#Will cause errors with bad input.
def commands(action, ph, sh, h):
    prime = ""
    second = ""
    #if statement to check for actions requiring an index.
    if " " in action:
        x = action.split(" ")
        if x[0] == "replace":
            temp = ph.remove_card(int(x[1]))
            h.replace(temp)
            prime = "You return the " + temp.peak() + " to the deck."
            second = "The other player returns the " + temp.peak() + " to the deck."

        elif x[0] == "discard":
            temp = ph.remove_card(int(x[1]))
            prime = "You discard the " + temp.peak()
            if temp.hidden:
                second = "The other player discards a card."
            else:
                second = "The other player discards the " + temp.peak()

        elif x[0] == "flip":
            temp = ph.flip(x[1])
            if ph.cards[int(x[1])].hidden:
                prime = "You conceal the " + temp.peak()
                second = "The other player conceals the " + temp.peak()
            else:
                prime = "You reveal the " + temp.peak()
                second = "The other player reveals the " + temp.peak()

        #Bad input will be flagged here and no messages will be sent.
        else:
            print("A critical error has occured.")
            print(action, "not recognized.")

    #Actions that don't require and index.
    else:

        if action == "view":
            prime = ph.view()
            second = "The other player looks at their cards."

        elif action == "check":
            prime = sh.check()
            second = "The other player looks at your cards."

        elif action == "draw":
            temp = h.deal()

            #Haven't properly tested this if statement, but it should be solid.
            if temp == "The deck is empty.":
                prime = temp + ""
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

        #Bad input will be flagged here and no messages will be sent.
        else:
            #Action validity should be checked on client side.
            print("A critical error has occured.")
            print(action, "not recognized.")

    return prime, second, ph, sh, h

#The 'main' function creates the deck, the sockets, the hands, and manages the turns and messaging.
#Probably could have stood to break it up more but it is what it is at this point.
def main():
    house = Deck()
    house.sort()
    house.shuffle()

    #The sockets.
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address1 = ('localhost', 10000)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address2 = ('localhost', 10001)

    sock1.bind(server_address1)
    sock2.bind(server_address2)

    #While-loop will wait for both players to connect then break.
    #Might come back and add an escape here. 
    while True:
        d1, a1 = sock1.recvfrom(4096)
        d2, a2 = sock2.recvfrom(4096)
        p1 = d1.decode('utf-8')
        p2 = d2.decode('utf-8')

        #Players will initially send 'connecting'.
        if p1 == "connecting" and p2 == "connecting":
            m = "Both players connected.\n"
            m1 = m.encode('utf-8')
            sock1.sendto(m1, a1)
            sock2.sendto(m1, a2)
            break

    turn = 1
    hand1 = Hand()
    hand2 = Hand()
    game_over = False

    #'try' 'finally' will send quit message in case of crash.
    try:

        #This is the turn-loop. Only breaks if 'quit' message is received or an error occurs. 
        while True:
            while turn == 1:
                code1, a1 = sock1.recvfrom(4096)
                
                if code1:
                    c1 = code1.decode('utf-8')
                    code1 = ""
                    #Messages from player 1 printed to server here.
                    print(c1)

                    #'quit' is handled outside of 'commands' function for logistical reasons.
                    if c1 == "quit":
                        m = "Player 1 has quit.\n"
                        m1 = m.encode('utf-8')
                        sock1.sendto(m1, a1)
                        sock1.sendto(m1, a2)
                        game_over = True
                        turn = 0

                    #'end' is handled outside of 'commands' function for logistical reasons.
                    elif c1 == "end":
                        player_one_message = "You end your turn."
                        player_two_message = "The other player ends their turn."
                        p1m = player_one_message.encode('utf-8')
                        p2m = player_two_message.encode('utf-8')
                        sock1.sendto(p1m, a1)
                        sock2.sendto(p2m, a2)
                        turn = 2

                    #All other actions will go to commands with player 1 being the primary player and primary hand.
                    else:
                        p1m, p2m, hand1, hand2, house = commands(c1, hand1, hand2, house)
                        p1m = p1m.encode('utf-8')
                        p2m = p2m.encode('utf-8')
                        sock1.sendto(p1m, a1)
                        sock2.sendto(p2m, a2)


            while turn == 2:
                code2, a2 = sock2.recvfrom(4096)
                
                if code2:
                    c2 = code2.decode('utf-8')
                    code2 = ""
                    #Messages from player 2 printed to server here.
                    print(c2)

                    #'quit' is handled outside of 'commands' function for logistical reasons.
                    if c2 == "quit":
                        m = "Player 2 has quit.\n"
                        m1 = m.encode('utf-8')
                        sock1.sendto(m1, a1)
                        sock1.sendto(m1, a2)
                        game_over = True
                        turn = 0

                    #'end' is handled outside of 'commands' function for logistical reasons.
                    elif c2 == "end":
                        player_two_message = "You end your turn."
                        player_one_message = "The other player ends their turn."
                        p1m = player_one_message.encode('utf-8')
                        p2m = player_two_message.encode('utf-8')
                        sock1.sendto(p1m, a1)
                        sock2.sendto(p2m, a2)
                        turn = 1

                    #All other actions will go to commands with player 2 being the primary player and primary hand.
                    else:
                        p2m, p1m, hand2, hand1, house = commands(c2, hand2, hand1, house)
                        p1m = p1m.encode('utf-8')
                        p2m = p2m.encode('utf-8')
                        sock1.sendto(p1m, a1)
                        sock2.sendto(p2m, a2)

            #If game_over is made True via 'quit' if-statement the while-loop breaks. 
            if game_over:
                break
    
    #Sockets closed here to ensure closure in event of error. 
    finally:
        m = "quit"
        m1 = m.encode('utf-8')
        sock1.sendto(m1, a1)
        sock2.sendto(m1, a2)


        print("Test complete.\n")
        sock1.close()
        sock2.close()

    
#Program start.
main()

#Credit to these guys for helping me remember how this works:
#https://pymotw.com/2/socket/udp.html