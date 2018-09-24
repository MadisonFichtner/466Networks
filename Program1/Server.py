import sys
import argparse
import http.server as s
import urllib as url
import urllib
import Board as b

#For player 2's server playing against player 1, Run as:
#python server.py 127.0.0.1 1024 own_board_2.txt


server = s.HTTPServer
handler = s.BaseHTTPRequestHandler
ip = (sys.argv[1])
port = int(sys.argv[2])
file_name = (sys.argv[3])
own_file_name = (sys.argv[4])

class myHandler(handler):
    # ship count to track sink
    c_ship = int(5)
    b_ship = int(4)
    r_ship = int(3)
    s_ship = int(3)
    d_ship = int(2)
    print(c_ship)

    # takes in response number and message and
    # returns HTTP response to client
    def _set_response(self, n, message):
        num = int(n)
        self.send_response(num, message)
        self.send_header('', '')
        self.end_headers()

    # checks if a ship has been sunk
    @classmethod
    def is_sunk(self, ship):
        if ship == 'C':
            self.c_ship -= 1
            print(self.c_ship)
            if self.c_ship == 0:
                return 1
        elif ship == 'B':
            self.b_ship -= 1
            if self.b_ship == 0:
                return 1
        elif ship == 'R':
            self.r_ship -= 1
            if self.r_ship == 0:
                return 1
        elif ship == 'S':
            self.s_ship -= 1
            if self.s_ship == 0:
                return 1
        elif ship == 'D':
            self.d_ship -= 1
            if self.d_ship == 0:
                return 1

    # handles HTTP post message fro client
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        print("message: ", post_data)
        # ---------obtaining coordinates from data sent over connection---------
        coordinates = urllib.parse.unquote(post_data.decode('utf-8'))
        andLocation = coordinates.find("&")
        xHalf = coordinates[0:andLocation]
        yHalf = coordinates[andLocation + 1: len(coordinates)]
        x = xHalf[xHalf.find("=") + 1:len(xHalf)]
        y = yHalf[yHalf.find("=") + 1:len(yHalf)]

        # prints coordinates
        print("Recieved Coordinates x:", x, " y:", y)


        #-------------updates own board----------------------------------------
        with open(file_name) as textFile:
            own_board = [line.split() for line in textFile]
        with open(own_file_name) as textFile:
            opp_board = [line.split() for line in textFile]

        int_x = int(x)
        int_y = int(y)
        update = '0'
        # if location on board is a ship (a letter) send hit = 1 (or hit)
        if own_board[int_x][int_y] == "C" or \
                        own_board[int_x][int_y] == "B" or \
                        own_board[int_x][int_y] == "R" or \
                        own_board[int_x][int_y] == "S" or \
                        own_board[int_x][int_y] == "D":
            # checks if ship is sunk
            if self.is_sunk(own_board[int_x][int_y]) == 1:
                self._set_response(200, (own_board[int_x][int_y] + '/hit= 1/&sunk=' + own_board[int_x][int_y]))
                update ='1'
            else:
                self._set_response(200, (own_board[int_x][int_y] + '/hit= 1'))
                update ='1'
        # if location on board is empty send hit = 0 (or miss)
        elif own_board[int_x][int_y] == "_" or own_board[int_x][int_y] == "M": #miss
            self._set_response(300, 'hit= 0')
            update = '2'
        # if location on board is X already gone
        elif own_board[int_x][int_y] == "X":
            self._set_response(300, 'Gone')
        # else location is not on board or has already been tried
        else:
            self._set_response(300, 'Not Found')

        b.update_board(own_board, int_x, int_y, update, "X")
        print("\nYour current board:")
        b.print_board(own_board)
        print("\nOpponents current board:")
        b.print_board(opp_board)
        b.write_board(own_board, file_name)
        # ---------------------------------------------------------------------

def run(server=s.HTTPServer, handler_class=myHandler):
    # assign server IP and adress
    server_address = (ip, port)
    # run server
    httpd = server(server_address, handler_class)
    print("server is running...")
    httpd.serve_forever()


run()
