import socket
import sys
import argparse

#parser = argparse.ArgumentParser(description='Server details.')
#parser.add_argument()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 5000))
data, addr = s.recvfrom(64)
print("Received message: " + data.decode('utf-8') +"'")
