# -*- coding: UTF-8 -*-

import argparse
import socket
import struct

HOST = "localhost"
PORT = "5555" 

parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument("port")

args = parser.parse_args()


def receive_data(sock, size, fmt):
    data = bytes()
    while len(data) < size:
        data += sock.recv(size - len(data))
    return struct.unpack(fmt, data)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, int(PORT)))

# NME
sock.send("NME".encode("ascii"))
send(struct.pack("1B", 6))
sock.send(YOURNAMEHEREASSTRING.encode("ascii"))
# SET
header = sock.recv(3).decode("ascii")
if header != "SET":
    print("Protocol Error at SET")
else:
    (height, width )= receive_data(sock, 2, "2B")

# HUM
header = sock.recv(3).decode("ascii")
if header != "HUM":
    print("Protocol Error at HUM")
else:
    number_of_homes = receive_data(sock, 1, "1B")[0]
    homes_raw = receive_data(sock, number_of_homes * 2, "{}B".format(number_of_homes * 2))
    
# HME
header = sock.recv(3).decode("ascii")
if header != "HME":
    print("Protocol Error at HME")
else:
    start_position = tuple(receive_data(sock, 2, "2B"))

# MAP
header = sock.recv(3).decode("ascii")
if header != "MAP":
    print("Protocol Error at MAP")
else:
    number_map_commands = receive_data(sock,1, "1B")[0]
    map_commands_raw = receive_data(sock, number_map_commands * 5, "{}B".format(number_map_commands * 5)

