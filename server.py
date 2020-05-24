import socket
from deck import *

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
        d1, a1 = sock1.recvform(4096)
        d2, a2 = sock2.recvform(4096)

        if d1 and d2:
            m = "Both players connected.\n Beginning Game."
            sock1.sendto(m, a1)
            sock2.sendto(m, a2)
            break

    turn = 1
    print("Test complete")
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