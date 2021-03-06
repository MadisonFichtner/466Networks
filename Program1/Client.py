import Board as b
import sys
import http.client
import urllib.parse

#for player 1's client against player 2, run as:
#python client.py 127.0.0.1 1024 x y own_board_1.txt opp_board_1.txt


#for player 1's client against player 2, run as:
#python client.py 127.0.0.1 1024 x y own_board_1.txt opp_board_1.txt


ip = (sys.argv[1])  # ip address
port = int(sys.argv[2])  # port address
x = (sys.argv[3])  # x coordinate shot at
y = (sys.argv[4])  # y coordinate shot at

file_name = (sys.argv[5]) # opp_board
own_file_name = (sys.argv[6]) # own_board

def main():
    int_x = int(x)
    int_y = int(y)

    # Read in inputted file as opp_board
    # with open(file_name) as textFile:
    #       opp_board = [line.split() for line in textFile]
    # b.print_board(opp_board)

    # establish connection to server with ip and port
    client = http.client.HTTPConnection(ip, port)

    coord = urllib.parse.urlencode({'x': x, 'y': y})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    user = 'User-agent: Client.py'
    contentLength = 'Content-Length: %s' % (len(coord))
    param = urllib.parse.urlencode({'ip': ip, 'port': port})


    # print("test print ", param, "coord", coord, headers)
    # sends POST message to server
    client.request('POST', param, coord)

    # gets response from server
    response = client.getresponse()
    print("status : ", response.status, " reason: ", response.reason)

    ship = 'X'
    update = '0'
    # update board
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
        # if repose is a miss update board with M
        update = '2'
        
    # check if ship has sunk
    elif response.reason == "C/hit= 1/&sunk=C" or response.reason == "B/hit= 1/&sunk=B" or \
                    response.reason == "R/hit= 1/&sunk=R" or response.reason == "S/hit= 1/&sunk=S" or \
                    response.reason == "D/hit= 1/&sunk=D" or response.reason == "already hit":
        if response.reason == "already hit":
            ship = 'X'
        else:
            andLocation = response.reason.find("&")
            slashLocation = response.reason.find("/")
            sunken = response.reason[andLocation:]
            ship = response.reason[0:slashLocation]
            
            # print sunk message
            print("You sunk your opponents: ", ship, " ship!")
            print(" ___   _   _   _  _   _  __")
            print("/ __| | | | | | \| | | |/ /")
            print("\__ \ | |_| | | .` | | ' < ")
            print("|___/  \___/  |_|\_| |_|\_\\")
        update = '1'
    with open(file_name) as textFile:
        opp_board = [line.split() for line in textFile]
    with open(own_file_name) as textFile:
        own_board = [line.split() for line in textFile]
    b.update_board(opp_board, int_x, int_y, update, ship)
    
    # print updated opponent and own boards
    print("\nOpponents updated board:")
    b.print_board(opp_board)
    b.write_board(opp_board, file_name)
    print("\nYour current board:")
    b.print_board(own_board)

main()
