import socket
from deck import *

def commands():
    pass

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
    quit = False
    while True:
        while turn == 1:
            code1, a1 = sock1.recvfrom(4096)
            code2, a2 = sock2.recvfrom(4096)
            
            if code1:
                c1 = code1.decode('utf-8')
                if c1 == "quit":
                    m = "Player 1 has ended the game."
                    m1 = m.encode('utf-8')
                    sock1.sendto(m1, a1)
                    sock2.sendto(m1, a2)
                    quit = True
                    break
                
                code1 = None
                #Okay hold on, this probably doesn't work. 
                #We have to deal with cards, the deck, and passing information back to the players.
                commands()

            if code2:
                c2 = code2.decode('utf-8')
                if c2 == "quit":
                    m = "Player 2 has ended the game."
                    m1 = m.encode('utf-8')
                    sock1.sendto(m1, a1)
                    sock2.sendto(m1, a2)
                    quit = True
                    break

                code2 = None

        while turn == 2:
            code1, a1 = sock1.recvfrom(4096)
            code2, a2 = sock2.recvfrom(4096)

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