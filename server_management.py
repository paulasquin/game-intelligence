import socket
import subprocess
import os
import threading as th
import struct
import time
import numpy as np

HOST = 'localhost'
PORT = 5555
TEAM_NAME = "Test"
PATH_SERVER = 'Resources/VampiresVSWerewolvesGameServer.exe'


class Map:
    def __init__(self):
        self.height = None
        self.width = None
        self.number_of_homes = None
        self.homes_raw = None
        self.start_position = None
        self.number_map_commands = None
        self.map_commands_raw = None
        self.__matrix = None
        self.init_finished = False

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, x, y, val):
        self.__matrix[x][y] = val

    def guess_species(self, start_position, map_commands_raws):
        pass

    def create_objects(self):
        # Creating the matrix of the map
        print(type(self.height))
        self.__matrix = [[None] * self.height - 1] * self.width - 1
        # Create homes
        # TODO: are home an important thing to care about ? If the home doesn't protect humans in any way,
        # TODO how is a home different from a regular cell ?

        # Our initial position
        # TODO: is start position useful as we already have map_commands
        # TODO that is giving us the position of W, H and W but without the number ?
        # self.matrix(self.__start_position[0], self.__start_position[1], Friend)

        # Fill the matrix with creatures.
        for id_command in range(self.number_map_commands):
            # Rebuilt with allies or enemies
            creatures = [[2, Human], [3, Vampire], [4, Werewolf]]
            for creature in creatures:
                if self.map_commands_raw(id_command * 5 + creature[0]) != 0:
                    print("Found" + str(creature[1]))
                    self.matrix(
                        self.map_commands_raw(
                            id_command * 5,
                            id_command * 5 + 1,
                            [creature[1] for _ in range(id_command * 5 + creature[0])]
                        )
                    )


class Object:
    pass


class Creature(Object):
    pass


class Human(Creature):
    pass


class House(Object):
    pass


class Allies(Creature):
    def move(self, direction):
        if direction == 'n':
            pass


class Enemies(Creature):
    pass


class Client(th.Thread):
    def __init__(self, game_map):
        print("Initialing client")
        self.map = game_map
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
        self.map.init_finished = True

    def run(self):
        # We have to start by sending NME and our team name
        self.send_msg("NME", TEAM_NAME.encode('ascii'))

        # Then the server is going to answer information SET, HUM, HME and MAP. We have to handle their unpacking
        self.init_communication()
        time.sleep(1000)
        print("Closing client")
        self.server_con.close()


def main():
    # Init game map as a shared object.
    game_map = Map()
    # the client is init with the map object. It will affect the first values and let the map be updated.
    client = Client(game_map)
    # Start the client
    client.start()
    while game_map.init_finished:
        time.sleep(0.01)
    game_map.create_objects()
    print(game_map.__dict__)


if __name__ == "__main__":
    main()
