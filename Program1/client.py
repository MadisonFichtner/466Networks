import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('hello'.encode('utf-8'), ('127.0.0.1',5000))
