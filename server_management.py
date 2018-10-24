import socket
import time
import threading as th
import struct

host = 'localhost'
port = 5555
TEAM_NAME = "Test"


def wait_msg(external_con, msg, delay):
    # wait for receiving HLO, wait for less than 5 sec
    rep = b""
    start_wait = time.time()
    while rep != msg and time.time() - start_wait < delay:
        rep = external_con.recv(1024)
    # if we didn't received msg, raise an error
    if rep != msg:
        raise NameError("Failed receiving " + str(msg))


class Client(th.Thread):
    def __init__(self):
        print("Initialing client")
        th.Thread.__init__(self)
        self.server_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_con.connect((host, port))

    def run(self):
        # We have to start by sending NME and our team name
        # wait_msg(self.server_con, b"NME", 5)
        msg_format = '3c c ' + str(len(TEAM_NAME)) + 'c'
        print(msg_format)
        nme_msg = struct.pack(msg_format, bytes(len(TEAM_NAME)), TEAM_NAME.encode('utf-8'))
        print(nme_msg)
        self.server_con.send(nme_msg)
        rep = b""
        while rep != b"BYE":
            rep = self.server_con.recv(1024)
            print(rep.decode())
        print("Closing client")
        self.server_con.close()


def main():
    # server = Server()
    # server.start()
    client = Client()
    client.start()
    # server.join()
    client.join()


if __name__ == "__main__":
    main()
