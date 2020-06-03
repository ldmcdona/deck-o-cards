import socket
from deck import *

def game_loop(turn, sock, server_address):
    actions = ["view", "check", "draw", "replace", "discard", "flip", "shuffle", "sort", "end", "quit", ""]
    while True:
        if turn:
            x = input()
            if x in actions:
                if x == 'quit':
                    #return
                    pass
                elif x == '':
                    #invalid
                    pass
                elif x == 'end':
                    #turn = False, send message
                    pass
                else:
                    #general send message.
                    pass
        else:
            #Might have to rethink being able to quit on opponents turn.
            #It'd be nice, but at present it's causing issues with flow.
            #Alternative would be some kind of async.
            x = input()
            if x in actions:
                if x == 'quit':
                    #return
                    pass
                elif x == '':
                    #literaly just pass
                    pass
                else:
                    #Not your turn.
                    pass
            data, server = sock.recvfrom(4096)


def main():
    host = input("Please enter server address: ")
    player = input("Are you player one or player two (enter 'one' or 'two'): ")

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

        """
        if p == 1:
            print("You get to go first.\n")
            print("Available actions are as follows:\n")
            print("'view' to look at your hand.\n'check' to look at the other players hand.\n'draw' to draw a card.\n")
            print("'replace x' to return card #x in your hand to the deck.\n'discard x' to discard car #x from your hand.\n")
            print("'flip x' to reveal or conceal card #x in your hand.\n'shuffle' to refill and shuffle the deck.\n")
            print("'sort' to refill and order the deck.\n'end' to end your turn.\n'quit' to quit the game.\n")       

        else:
            print("The other player gets to go first.\n")
            print("Please wait for your turn.\n")
            print("Type 'quit' to quit the game.\n")
        """


    finally:
        print("Test complete.")
        sock.close()

main()