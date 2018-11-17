import socket
import sys
import struct
import os
import numpy as np
import tools
import time


class Server:
    def __init__(self, host, port):
        print("Creating connection to server with socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print("Creating agent_state to get playground")
        self.agent_state = {'height': None,
                            'width': None,
                            'number_of_homes': None,
                            'homes_raw': None,
                            'start_position': None,
                            'number_map_commands': None,
                            'map_commands_raw': None}

        # First Send the NME Message to Server
        print('Starting the Game by sending NME and team name')
        self.send_nme('NME', 'Team6')
        # Receiving SET, HUM, HME, MAP, UPD, END, BYE
        self.get_set()
        self.get_hum()
        self.get_hme()
        self.get_map()
        # Creating a map array board matrix
        self.set_board_matrix()
        # Guess if we are Vampire or Werewolves
        self.species_dict = self.perform_species_guess()

    def perform_species_guess(self):
        """
        Display if we are vampires ou werewolves using tools
        :return:
        """
        species_dict = tools.identify_species(self.board_matrix, self.agent_state)
        if species_dict['our_species'] == 'vampires':
            print('We are vampires')
        elif species_dict['our_species'] == 'werewolves':
            print('We are werewolves')
        return species_dict

    @staticmethod
    def start_server_ex(server_path):
        """
        Try to run executable server program
        :param server_path:
        :return:
        """
        print("Starting server from " + server_path)
        os.system('start ' + server_path)

    def send_nme(self, nme_command, msg):
        """
        Send NME command to server with team name
        :param nme_command:
        :param msg:
        :return:
        """
        print('Sending the NME Message to the Server')
        self.sock.send(nme_command.encode("ascii"))
        self.sock.send(struct.pack("1B", len(msg)))
        self.sock.send(msg.encode("ascii"))

    def get_set(self):
        """
        Getting playground size with "SET" command (setting the map)
        :return:
        """
        print("SET: Getting playground size")
        header = self.sock.recv(3).decode("ascii")
        if header != "SET":
            print("Protocol Error at SET")
        else:
            (self.agent_state['height'], self.agent_state['width']) = self.receive_data(2, "2B")

    def get_hum(self):
        """
        Getting human houses positions
        :return:
        """
        print("HUM: Getting info on human an houses")
        header = self.sock.recv(3).decode("ascii")
        if header != "HUM":
            print("Protocol Error at HUM")
        else:
            self.agent_state['number_of_homes'] = self.receive_data(1, "1B")[0]
            self.agent_state['homes_raw'] = \
                self.receive_data(
                    self.agent_state['number_of_homes'] * 2,
                    "{}B".format(self.agent_state['number_of_homes'] * 2)
                )

    def get_hme(self):
        """
        Getting start position
        :return:
        """
        print("HME: Getting our start position")
        header = self.sock.recv(3).decode("ascii")
        if header != "HME":
            print("Protocol Error at HME")
        else:
            self.agent_state['start_position'] = tuple(self.receive_data(2, "2B"))

    def get_map(self):
        """
        Getting map
        :return:
        """
        print("MAP: Getting map first state")
        header = self.sock.recv(3).decode("ascii")
        if header != "MAP":
            print("Protocol Error at MAP")
        else:
            self.update_agent_state()

    def set_board_matrix(self):
        print("Creating a Numpy Array for Board.")
        self.board_cell_dict = {'cell_human_count': 0, 'cell_vampire_count': 0, 'cell_werewolves_count': 0}
        self.board_matrix = np.full(
            shape=(self.agent_state['height'], self.agent_state['width']), fill_value=self.board_cell_dict)
        print("Board matrix is at first:" + str(self.board_matrix))

        print("Try board matrix update")
        self.board_matrix = tools.update_board_matrix(self.board_matrix, self.agent_state)

    def receive_data(self, size, fmt):
        data = bytes()
        while len(data) < size:
            data += self.sock.recv(size - len(data))
        return struct.unpack(fmt, data)

    def send_move(self, mov_command):
        ## Testing the Move command. Right now just making few random moves.
        self.sock.send(mov_command.encode("ascii"))
        # Choosing to perform 1 command
        self.sock.send(struct.pack("1B", 1))
        # Incoming cell
        self.sock.send(struct.pack("2B", 4, 3))
        # 2 vampires
        self.sock.send(struct.pack("1B", 2))
        # Destination cell
        self.sock.send(struct.pack("2B", 4, 4))

    def update_agent_state(self):
        self.agent_state['number_map_commands'] = self.receive_data(1, "1B")[0]
        self.agent_state['map_commands_raw'] = \
            self.receive_data(
                self.agent_state['number_map_commands'] * 5,
                "{}B".format(self.agent_state['number_map_commands'] * 5)
            )

    def update_board_matrix(self):
        self.board_matrix = tools.update_board_matrix(self.board_matrix, self.agent_state)
