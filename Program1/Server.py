import socket
import sys
import argparse
import http.server as s
import urllib as url
import urllib
import logging

server = s.HTTPServer
handler = s.BaseHTTPRequestHandler

class myHandler(handler):
    # all of this is copy and pasted from https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        coordinates = post_data.decode('utf-8')

        #---------obtaining coordinates from data sent over connection---------
        coordinates = urllib.parse.unquote(post_data.decode('utf-8'))
        andLocation = coordinates.find("&")
        xHalf = coordinates[0:andLocation]
        yHalf = coordinates[andLocation+1: len(coordinates)]
        x = xHalf[xHalf.find("=")+1:len(xHalf)]
        y = yHalf[yHalf.find("=")+1:len(yHalf)]

        print("Recieved Coordinates x:", x, " y:", y)
        #----------------------------------------------------------------------

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))



def run(server = s.HTTPServer, handler_class = myHandler):
    ip = (sys.argv[1])
    port = int(sys.argv[2])
    #infile = open(sys.argv[3])

    server_address = (ip, port)
    httpd = server(server_address, handler_class)
    print("server is running...")
    httpd.serve_forever()

'''
    data, addr = httpd.recv(1024)
    data1, addr = httpd.recv(1024)
    print("Received message: " + data.decode('utf-8') +"'")
    httpd.close()
'''

'''
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
'''

run()



'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp socket

s.bind(('127.0.0.1', 1024))
s.listen(1)
# client stuff happens
# conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket??

#c.addr = s.accept()
(c, address) = s.accept()
data = c.recv(1024)
c.send(data) # echo

msg = data.decode("ascii")
print ("SERVER RECEIVED: " +msg)
c.close()

'''

'''
import socket
import sys
import argparse


#parser = argparse.ArgumentParser(description='Server details.')
#parser.add_argument()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 5000))

data, addr = s.recvfrom(64)
print("Received message: " + data.decode('utf-8') +"'")


def check_message():
    # inbounds?
    # have coordinates been used
    # is it formatted correctly
    return 0

def check_board():
    # hit/ miss
    # sink
    return 0

# result message

    # HTTPResponse
    # ex: hit=1\&sink=D
        # HTTP ok with:
            # hit =
                # 1 --> hit
                # 0 --> miss
            # sink = letter code (if applicable)
                # ex: (C, B, R, S, D)
        # if out of bounds:
            # HTTP Not Found
        # if coordinates have already been attempted
            # HTTP Bad Request
'''
