#This file exists to do testing of deck.py stuff without having to go through the sockets.

m = "Hello World"
print(m, type(m), "\n")
e = m.encode('utf-8')
print(e, type(e), "\n")
d = e.decode('utf-8')
print(d, type(d), "\n")