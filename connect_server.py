#!/usr/bin/env python
# coding: utf-8

# # Connect to server and performe command sending

# ## Import the strategy

# In[ ]:


from strategy_training import *


# ## Server tools

# In[ ]:


class Tools:
    @staticmethod
    def update_board_matrix(board_matrix, agent_state):
        board_info = list(agent_state['map_commands_raw'])
        for i in range(len(board_info)):
            if i % 5 == 0:
                temp_cell = [board_info[i + 2], board_info[i + 3], board_info[i + 4]]
                #             humans             vampires            werewolves
                board_matrix[board_info[i + 1]][board_info[i]] = temp_cell
        return board_matrix
    
    @staticmethod
    def board2points(board_matrix):
        """
        Convert board_matrix to 3 lists of Point object: Vampires, Werewolves, Humans.
        :param board_matrix:
        
        :return list_creatures: list of Point
            list_vampires
            list_werewolves
            list_humans
        """
        human_groups_positon = np.argwhere(board_matrix[:,:, 0] > 0)
        vampire_groups_positon = np.argwhere(board_matrix[:,:, 1] > 0)
        werewolf_groups_positon = np.argwhere(board_matrix[:,:, 2] > 0)
        
        list_humans = []
        list_vampires = []
        list_werewolves = []
        
        for humans_position in human_groups_positon:
            x_position = humans_position[0]
            y_position = humans_position[1]
            population = board_matrix[x_position, y_position, 0]
            list_humans.append(Point(x_position, y_position, population))
        
        for vampires_position in vampire_groups_positon:
            x_position = vampires_position[0]
            y_position = vampires_position[1]
            population = board_matrix[x_position, y_position, 1]
            list_vampires.append(Point(x_position, y_position, population))
            
        for werewolves_position in werewolf_groups_positon:
            x_position = werewolves_position[0]
            y_position = werewolves_position[1]
            population = board_matrix[x_position, y_position, 2]
            list_werewolves.append(Point(x_position, y_position, population))
        
        return list_vampires, list_werewolves, list_humans
    
    @staticmethod
    def identify_species(board_matrix, agent_state):
        x_initial = agent_state['start_position'][0]
        y_initial = agent_state['start_position'][1]
        temp_cell = board_matrix[y_initial][x_initial]

        if temp_cell[1] > 0:
            species_dict = {'our_species': 'vampires', 'opponent_species': 'werewolves'}
        elif temp_cell[2] > 0:
            species_dict = {'our_species': 'werewolves', 'opponent_species': 'vampires'}
        else:
            raise NameError("Can't guess our species")

        return species_dict


# ## Server communication

# ### Dependencies

# In[ ]:


import socket
import sys
import struct
import os
import numpy as np
import time


# In[ ]:


class Server:
    def __init__(self, host, port, name="Us"):
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
        self.send_nme('NME', name)
        # Receiving SET, HUM, HME, MAP, UPD, END, BYE
        self.get_set()
        self.get_hum()
        self.get_hme()
        self.get_map()
        # Creating a map array board matrix
        self.set_board_matrix()
        # Guess if we are Vampire or Werewolves
        self.species = self.perform_species_guess()

    def perform_species_guess(self):
        """
        Display if we are vampires ou werewolves using tools
        :return:
        """
        species_dict = Tools.identify_species(self.board_matrix, self.agent_state)
        if species_dict['our_species'] == 'vampires':
            print('We are vampires')
            return "V"
        elif species_dict['our_species'] == 'werewolves':
            print('We are werewolves')
            return "W"
        else:
            raise NameError("I don't recognize this species" + str(species_dict['our_species']))

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
        """
        print("HUM: Getting info on human an houses")
        header = self.sock.recv(3).decode("ascii")
        if header != "HUM":
            print("Protocol Error at HUM")
        else:
            self.agent_state['number_of_homes'] = self.receive_data(1, "1B")[0]
            self.agent_state['homes_raw'] =                 self.receive_data(
                    self.agent_state['number_of_homes'] * 2,
                    "{}B".format(self.agent_state['number_of_homes'] * 2)
                )

    def get_hme(self):
        """
        Getting start position
        """
        print("HME: Getting our start position")
        header = self.sock.recv(3).decode("ascii")
        if header != "HME":
            print("Protocol Error at HME")
        else:
            self.agent_state['start_position'] = tuple(self.receive_data(2, "2B"))

    def get_map(self):
        """
        Getting map and write it to agent state
        """
        print("MAP: Getting map first state")
        header = self.sock.recv(3).decode("ascii")
        if header != "MAP":
            print("Protocol Error at MAP")
        else:
            self.update_agent_state()

    def set_board_matrix(self):
        """
        Init a board matrix and try a first update
        """
        print("Creating a Numpy Array for Board.")
        self.board_matrix = np.zeros(shape=(self.agent_state['height'], self.agent_state['width'], 3))
        print("Try board matrix update")
        self.board_matrix = Tools.update_board_matrix(self.board_matrix, self.agent_state)

    def receive_data(self, size, fmt):
        data = bytes()
        while len(data) < size:
            data += self.sock.recv(size - len(data))
        return struct.unpack(fmt, data)

    def send_move(self, migration):
        """
        Send the move to the server
        :param migration: Migration, the migration to perform, in the strategy referential
        """
        ## Testing the Move command. Right now just making few random moves.
        self.sock.send("MOV".encode("ascii"))
        
        origin_position = migration.origin_position
        population = migration.population
        target_position = migration.target_position
        print("Performing", migration)
        # Sending move to server
        self.sock.send(struct.pack("1B", 1))
        self.sock.send(struct.pack("2B", origin_position.y, origin_position.x))
        self.sock.send(struct.pack("1B", population))
        self.sock.send(struct.pack("2B", target_position.y, target_position.x))

    def update_agent_state(self):
        self.agent_state['number_map_commands'] = self.receive_data(1, "1B")[0]
        self.agent_state['map_commands_raw'] =             self.receive_data(
                self.agent_state['number_map_commands'] * 5,
                "{}B".format(self.agent_state['number_map_commands'] * 5)
            )

    def update_board_matrix(self):
        self.board_matrix = Tools.update_board_matrix(self.board_matrix, self.agent_state)


# ## Init connection

# In[ ]:


def playing_game(srv):
    # send_move(sock,'MOV')
    while True:
        # UPD---------------------
        header = srv.sock.recv(3).decode("ascii")
        if header == "UPD":
            print('A UPD Packet has been received')
            srv.update_agent_state()
            # print(srv.agent_state)
            print('------------------------------------------------------------------------------------------')
            
            # Update the matrix
            srv.update_board_matrix()
            # Get it
            current_board_matrix = srv.board_matrix
            
            # Get the creatures Point lists
            list_vampires, list_werewolves, list_humans = Tools.board2points(board_matrix=current_board_matrix)

            # Get the best move to perform
            best_move_migration = interface_strategy(
                width=srv.agent_state['width'], 
                height=srv.agent_state['height'], 
                list_vampires=list_vampires, 
                list_werewolves=list_werewolves,
                list_humans=list_humans, 
                our_species=srv.species, 
                max_depth=5, 
                our_name="Dracula", 
                enemy_name="Garou", 
                verbose=1)
            srv.send_move(best_move_migration)
        # END--------------------------------------------------------------------------------------------------------------
        elif header == "END":
            print('The END Packet has been received')
            print("The Game has ended")
            print("Closing the connection now")
            srv.sock.close()
            sys.exit()

        # BYE------------------------------------------------------------------------------------------------------------
        elif header == "BYE":
            print('BYE Packet has been received')
            print("Closing the connection now")
            srv.sock.close()


# In[ ]:


SERVER_PROGRAM_PATH = 'game-intelligence\\Resources\\VampiresVSWerewolvesGameServer'
import random

def main(host='localhost', port = 5555):
    # server.start_server(SERVER_PROGRAM_PATH)
    srv = Server(host, port, "#" + str(random.randint(1, 555)))
    print("Width:", srv.agent_state['width'])
    print("Height:", srv.agent_state['height'])
    playing_game(srv)


# ## Unleashing hell

# In[ ]:


import sys
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No parameters given. Using default")
        main()
    elif len(sys.argv) == 4 and sys.argv[1] == "--myparams":
        host = sys.argv[2]
        port = int(sys.argv[3])
        main(host, port)
    else:
        print("Error in usage")
        print("usage: python name_of_file.py --myparams 123.123.3.5 6666")

