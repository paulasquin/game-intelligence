import socket
import time
import threading as th

host = 'localhost'
port = 12800


def wait_msg(external_con, msg, delay):
    # wait for receiving HLO, wait for less than 5 sec
    rep = b""
    start_wait = time.time()
    while rep != msg and time.time() - start_wait < delay:
        rep = external_con.recv(1024)
    # if we didn't received msg, raise an error
    if rep != msg:
        raise NameError("Failed receiving " + str(msg))


class Server(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
        self.main_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_con.bind(('', port))
        self.main_con.listen(5)

    def run(self):
        # init connexion
        client_con, info_con = self.main_con.accept()

        client_con.send(b"HLO")
        wait_msg(client_con, b"HLO", 5)

        msg = b""
        while msg != b"QUT":
            msg = client_con.recv(1024)
            client_con.send(compute(msg).encode())

        print("Closing server")
        client_con.close()
        self.main_con.close()


class Client(th.Thread):
    def __init__(self):
        print("Initialing client")
        th.Thread.__init__(self)
        self.server_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_con.connect((host, port))

    def run(self):
        wait_msg(self.server_con, b"HLO", 5)
        self.server_con.send(b"HLO")

        msg = b""
        while msg != b"QUT":
            msg = input("> ").encode()
            self.server_con.send(msg)
            rep = self.server_con.recv(1024)
            print(rep.decode())
        print("Closing client")
        self.server_con.close()


def main():
    server = Server()
    server.start()
    client = Client()
    client.start()
    server.join()
    client.join()


main()
