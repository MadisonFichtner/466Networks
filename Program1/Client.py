import socket
import Board as b
import sys
import http.client
import urllib.parse
import urllib as u

ip = (sys.argv[1])  #ip address
port = int(sys.argv[2]) #port address
x = (sys.argv[3])    #x coordinate shot at
y = (sys.argv[4])    #y coordinate shot at

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
locationX = 5;
locationY = 4;
b.update_board(own_board, 5, 4)
print("my updated board")
b.print_board(own_board)

#reading in a file to a 2d array
with open("ownBoard.txt") as textFile:
    lines = [line.split() for line in textFile]

def main():
    client = http.client.HTTPConnection(ip, port)

    coord = urllib.parse.urlencode({'?x': x, '?y': y})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    user = 'User-agent: Client.py'
    contentLength = 'Content-Length: %s' %(len(coord))
    param = urllib.parse.urlencode({'http://': ip, ':': port, 'len': contentLength, 'user': user})
    client.request('POST', param, coord, headers)

    response = client.getresponse()
    print ("status : " , response.status, " reason: " , response.reason)


main()
