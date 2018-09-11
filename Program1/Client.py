import socket
import Board as b

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('hello'.encode('utf-8'), ('127.0.0.1', 5000))

# initialize and print own board
own_board = []
print("my board")
b.create_empty_board(own_board)
b.print_board(own_board)

# initialize and print opponents board
opp_board = []
print("opponents board")
b.create_empty_board(opp_board)
b.print_board(opp_board)

# Update own board to show X at location (5, 4)
b.update_board(own_board, 5, 4)
print("my updated board")
b.print_board(own_board)
