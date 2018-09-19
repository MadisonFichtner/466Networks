import socket
import Board as b
import argparse
import sys
import http.client
import urllib.parse
import urllib as u

ip = (sys.argv[1])  # ip address
port = int(sys.argv[2])  # port address
x = (sys.argv[3])  # x coordinate shot at
y = (sys.argv[4])  # y coordinate shot at
file_name = (sys.argv[5])


def main():
    int_x = int(x)
    int_y = int(y)
    # Read in inputted file as opp_board
    # with open(file_name) as textFile:
    #    opp_board = [line.split() for line in textFile]
    # b.print_board(opp_board)

    client = http.client.HTTPConnection(ip, port)

    coord = urllib.parse.urlencode({'x': x, 'y': y})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    user = 'User-agent: Client.py'
    contentLength = 'Content-Length: %s' % (len(coord))
    param = urllib.parse.urlencode({'ip': ip, 'port': port})

    print("test print ", param, "coord", coord, headers)
    client.request('POST', param, coord)

    # b.read_board("opp_board.txt", 1, 1)

    response = client.getresponse()
    print("status : ", response.status, " reason: ", response.reason)

    ship = 'X'
    update = '0'
    if response.reason == "C/hit= 1" or response.reason == "B/hit= 1" or \
                    response.reason == "R/hit= 1" or response.reason == "S/hit= 1" or \
                    response.reason == "D/hit= 1" or response.reason == "already hit":
        if response.reason == "already hit":
            ship = 'X'
        else:
            slashLocation = response.reason.find("/")
            ship = response.reason[0:slashLocation]
            print("ship ", ship)
        update = '1'
    elif response.reason == "hit= 0":
        update = '2'

    with open(file_name) as textFile:
        opp_board = [line.split() for line in textFile]
    b.update_board(opp_board, int_x, int_y, update, ship)
    b.print_board(opp_board)
    b.write_board(opp_board, file_name)


main()
