import sys
import argparse
import http.server as s
import urllib as url
import urllib
import Board as b

server = s.HTTPServer
handler = s.BaseHTTPRequestHandler
ip = (sys.argv[1])
port = int(sys.argv[2])
file_name = (sys.argv[3])

class myHandler(handler):
    # all of this is copy and pasted from https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
    def _set_response(self,n , message):
        num = int(n)
        self.send_response(num, message)
        self.send_header('', '')
        self.end_headers()

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

        print("Recieved Coordinates x:", x, " y:", y)


        #-------------updates own board----------------------------------------
        #own_board = []
        #b.own_board(own_board)
        with open(file_name) as textFile:
            own_board = [line.split() for line in textFile]

        int_x = int(x)
        int_y = int(y)
        update = 0
        if own_board[int_x][int_y] == "C" or own_board[int_x][int_y] == "B" or own_board[int_x][int_y] == "R" or own_board[int_x][int_y] == "S" or own_board[int_x][int_y] == "D": #or "B" # or "R" or "S" or "D":
            self._set_response(200, 'hit')
            update = 1
        elif own_board[int_x][int_y] == "_": #miss
            self._set_response(300, 'miss')
            update = 2
        elif own_board[int_x][int_y] == "X":
            self._set_response(300, 'already hit')
        else:
            self._set_response(300, 'nothing')

        b.update_board(own_board, int_x, int_y, update)
        b.print_board(own_board)
        b.write_board(own_board, file_name)
        # ---------------------------------------------------------------------



def run(server=s.HTTPServer, handler_class=myHandler):
    server_address = (ip, port)
    httpd = server(server_address, handler_class)
    print("server is running...")
    httpd.serve_forever()

run()
