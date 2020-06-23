import socket

#The 'turn' function takes input, checks for valid input, and sends messages to the server accordingly.
#It is passed a socket 'sock', and a server_address(?) 'server_address'.
#It returns nothing, merely using return to end the turn or quit the game.  
def turn(sock, server_address):
    actions = ["view", "check", "draw", "replace", "discard", "flip", "shuffle", "sort", "end", "quit"]
    special = ["replace", "discard", "flip"]
    while True:
        x = input(">")
        if x in actions:
            #'quit' is handled seperately for logistical reasons.
            if x == 'quit':
                m1 = x.encode('utf-8')
                sock.sendto(m1, server_address)
                return

            #'end' is handled seperately for logistical reasons.
            elif x == 'end':
                m1 = x.encode('utf-8')
                sock.sendto(m1, server_address)
                data, server = sock.recvfrom(4096)
                m = data.decode('utf-8')
                print(m)
                return

            #Actions requiring an index value are handled seperately in order to receive that index through input.
            elif x in special:
                y = input("Enter index of card.\n>")
                message = x + " " + y
                m1 = message.encode('utf-8')
                sock.sendto(m1, server_address)
                data, server = sock.recvfrom(4096)
                m = data.decode('utf-8')
                print(m)

            #Standard actions are passed directly to the server.
            else:
                m1 = x.encode('utf-8')
                sock.sendto(m1, server_address)
                data, server = sock.recvfrom(4096)
                m = data.decode('utf-8')
                print(m)

        #Invalid actions get a message.
        else:
            print("Invalid input.\n")


#The 'main' function handels the initial connection and the turns.
def main():
    host = input("Please enter server address: ")
    player = input("Are you player one or player two (enter 'one' or 'two'): ")
    game = True

    #Different ports for each player.
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
    #'try' 'finally' will close socket if an error occurs.
    try:
        message = 'connecting'
        m1 = message.encode('utf-8')
        sock.sendto(m1, server_address)

        data, server = sock.recvfrom(4096)
        d1 = data.decode('utf-8')
        print("Message recieved: " + d1 + "\n")

        #Giant list of actions. Was easier to break them up than do \n stuff. 
        print("The game is beginning. On your turn your will be able to take the following actions:")
        print("'view' to look at your hand, with hidden cards being marked H and revealed cards being marked R.")
        print("'check' to look at your oppenents hand, with hidden cards being listed as H(X|X).")
        print("'draw' to draw a new card from the deck.")
        print("'replace' to return a card in your hand to the deck.")
        print("'discard' to remove a card in your hand from the game.")
        print("'flip' to reveal or hide a card in you hand.")
        print("'shuffle' to refill the deck then shuffle it.")
        print("'sort' to refill and order the deck.")
        print("'end' to end your turn.")
        print("'quit' to end the game.")

        #Turn loop. Breaks when "quit" message received.
        while game:
            if p == 1:
                print("It's your turn.\n")
                #'turn' function called here.
                turn(sock, server_address)
                p = 2
            
            #While loop for other players turn, breaks when they end their turn or quit.
            while p == 2:
                data, server = sock.recvfrom(4096)
                d1 = data.decode('utf-8')
                print(d1)
                if "end" in d1:
                    p = 1
                elif "quit" in d1:
                    p = 0
                    game = False

    #Close socket.
    finally:
        print("Test complete.")
        sock.close()

#Program start.
main()