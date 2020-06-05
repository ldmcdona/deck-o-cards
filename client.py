import socket
from deck import *

def turn():
    actions = ["view", "check", "draw", "replace", "discard", "flip", "shuffle", "sort", "end", "quit", ""]
    while True:
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

        while game:
            pass


    finally:
        print("Test complete.")
        sock.close()

main()