import socket
import subprocess
import os
import threading as th
import struct

HOST = 'localhost'
PORT = 5555
TEAM_NAME = "Test"
PATH_SERVER = 'Resources/VampiresVSWerewolvesGameServer.exe'


class Map:
    height = None
    width = None
    number_of_homes = None
    homes_raw = None
    start_position = None
    number_map_commands = None
    map_commands_raw = None


class Client(th.Thread):
    def __init__(self):
        print("Initialing client")
        self.map = Map()
        th.Thread.__init__(self)
        self.server_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_con.connect((HOST, PORT))

    def send_msg(self, protocol, msg):
        msg_format = str(len(protocol)) + 's B ' + str(len(msg)) + 's'
        msg_pack = struct.pack(msg_format, protocol.encode('ascii'), len(msg), msg)
        self.server_con.send(msg_pack)

    def receive_data(self, size, fmt):
        data = bytes()
        while len(data) < size:
            data += self.server_con.recv(size - len(data))
        return struct.unpack(fmt, data)

    def init_communication(self):
        # SET
        header = self.server_con.recv(3).decode("ascii")
        if header != "SET":
            print("Protocol Error at SET")
        else:
            (self.map.height, self.map.width) = self.receive_data(2, "2B")

        # HUM
        header = self.server_con.recv(3).decode("ascii")
        if header != "HUM":
            print("Protocol Error at HUM")
        else:
            self.map.number_of_homes = self.receive_data(1, "1B")[0]
            self.map.homes_raw = self.receive_data(
                self.map.number_of_homes * 2,
                "{}B".format(self.map.number_of_homes * 2)
            )

        # HME
        header = self.server_con.recv(3).decode("ascii")
        if header != "HME":
            print("Protocol Error at HME")
        else:
            self.map.start_position = tuple(self.receive_data(2, "2B"))

        # MAP
        header = self.server_con.recv(3).decode("ascii")
        if header != "MAP":
            print("Protocol Error at MAP")
        else:
            self.map.number_map_commands = self.receive_data(1, "1B")[0]
            self.map.map_commands_raw = self.receive_data(
                self.map.number_map_commands * 5,
                "{}B".format(self.map.number_map_commands * 5)
            )

    def run(self):
        # We have to start by sending NME and our team name
        self.send_msg("NME", TEAM_NAME.encode('ascii'))

        # Then the server is going to answer information SET, HUM, HME and MAP. We have to handle their unpacking
        self.init_communication()
        print(self.map.__dict__)
        print("Closing client")
        self.server_con.close()


class Server(th.Thread):
    def __init__(self):
        print("Starting server program")
        th.Thread.__init__(self)

    def run(self):
        # p = subprocess.Popen(
        #     [PATH_SERVER],
        #     shell=False,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        # stdout, stderr = p.communicate()
        # print(stdout)
        os.system('start ' + PATH_SERVER)


def main():
    # server = Server()
    # server.start()
    # time.sleep(9)

    client = Client()
    client.start()
    client.join()


if __name__ == "__main__":
    main()
