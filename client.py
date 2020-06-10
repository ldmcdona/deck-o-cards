import socket
from deck import *

def turn(sock, server_address):
    actions = ["view", "check", "draw", "replace", "discard", "flip", "shuffle", "sort", "end", "quit"]
    while True:
        x = input()
        if x in actions:
            if x == 'quit':
                m1 = x.encode('utf-8')
                sock.sendto(m1, server_address)
                return

            elif x == 'end':
                m1 = x.encode('utf-8')
                sock.sendto(m1, server_address)
                data, server = sock.recvfrom(4096)
                m = data.decode('utf-8')
                print(m)
                return

            else:
                m1 = x.encode('utf-8')
                sock.sendto(m1, server_address)
                data, server = sock.recvfrom(4096)
                m = data.decode('utf-8')
                print(m)
        else:
            print("Invalid input.\n")


def main():
    host = input("Please enter server address: ")
    player = input("Are you player one or player two (enter 'one' or 'two'): ")
    game = True

    if player == "one":
        server_address = (host, 10000)
        p = 1
    elif player == "two":
        server_address = (host, 10001)
        p = 2
    else:
        print("Invalid input\n")
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        message = 'connecting'
        m1 = message.encode('utf-8')
        sock.sendto(m1, server_address)

        data, server = sock.recvfrom(4096)
        d1 = data.decode('utf-8')
        print("Message recieved: " + d1 + "\n")

        print("The game is beginning. On your turn your will be able to take the following actions:\n")
        print("'view' to look at your hand, with hidden cards being marked H and revealed cards being marked R.\n")
        print("'check' to look at your oppenents hand, with hidden cards being listed as H(X|X).\n")
        print("'draw' to draw a new card from the deck.\n")
        print("'replace x' to return card x in your hand to the deck, with x being its spot in your hand stating with 0.\n")
        print("'discard x' to remove card x in your hand from the game.\n")
        print("'flip x' to reveal or hide card x in you hand.\n")
        print("'shuffle' to refill the deck then shuffle it.\n")
        print("'sort' to refill and order the deck.\n")
        print("'end' to end your turn.\n")
        print("'quit' to end the game.\n")

        while game:
            if p == 1:
                print("It's your turn.\n")
                turn(sock, server_address)
                p = 2
            
            while p == 2:
                data, server = sock.recvfrom(4096)
                d1 = data.decode('utf-8')
                print(d1)
                if "end" in d1:
                    p = 1
                elif "quit" in d1:
                    p = 0
                    game = False


    finally:
        print("Test complete.")
        sock.close()

main()