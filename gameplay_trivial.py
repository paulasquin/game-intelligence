#Server Connect
import socket
import sys
import struct
import os
import numpy as np

#-------------------------------------------------------------------------------------------------------
def start_server(SERVER_PROGRAM_PATH):
	os.system('start '+ SERVER_PROGRAM_PATH)

#-------------------------------------------------------------------------------------------------------
def establish_server_connection(host,port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))
	return sock

#---------------------------------------------------------------------------------------------------------
def send_nme(sock,nme_command,msg):

	print('Sending the NME Message to the Server')
	sock.send(nme_command.encode("ascii"))
	sock.send(struct.pack("1B", len(msg)))
	sock.send(msg.encode("ascii"))

#---------------------------------------------------------------------------------------------------------
def receive_data(sock, size, fmt):
    data = bytes()
    while len(data) < size:
        data += sock.recv(size - len(data))
    return struct.unpack(fmt, data)

#--------------------------------------------------------------------------------------------------------------
def send_move(sock,mov_command):

	## Testing the Move command. Right now just making few random moves.
	sock.send(mov_command.encode("ascii"))
	sock.send(struct.pack("1B",1))
	sock.send(struct.pack("2B",4,3))
	sock.send(struct.pack("1B",2))
	sock.send(struct.pack("2B",4,4))

#------------------------------------------------------------------------------------------------------------
def update_board_matrix(board_matrix,agent_state):

	board_info = list(agent_state['map_commands_raw'])

	print(board_info)

	for i in range(len(board_info)):

		if i%5==0:
			temp_dict = {'cell_human_count':board_info[i+2],'cell_vampire_count':board_info[i+3],'cell_werewolves_count':board_info[i+4]}
			board_matrix[board_info[i+1]] [board_info[i]] = temp_dict

	return board_matrix



#------------------------------------------------------------------------------------------------------------
def identify_species(board_matrix,agent_state):

	x_initial = agent_state['start_position'][0]
	y_initial = agent_state['start_position'][1]

	temp_dict = board_matrix[y_initial][x_initial]

	#print(temp_dict)

	if temp_dict['cell_vampire_count'] > 0:
		species_dict = {'our_species':'vampires','opponent_species':'werewolves'}
	elif temp_dict['cell_werewolves_count'] > 0:
		species_dict = {'our_species':'werewolves','opponent_species':'vampires'}

	return species_dict



#--------------------------------------------------------------------------------------------------------------
def start_game():

	# To be set as command line arguments
	host = 'localhost'
	port = 5555
	#SERVER_PROGRAM_PATH = 'game-intelligence\\Resources\\VampiresVSWerewolvesGameServer'

	#start_server(SERVER_PROGRAM_PATH)

	sock=establish_server_connection(host,port)

	agent_state= {'height' : None,
    		      'width' : None,
    		      'number_of_homes' : None,
    		      'homes_raw' : None,
    		      'start_position' : None,
    		      'number_map_commands' : None,
    		      'map_commands_raw' : None}

	# First Send the NME Message to Server

	print('Starting the Game')
	send_nme(sock,'NME','Team6')

	# Receiving SET, HUM, HME, MAP, UPD, END, BYE

	# SET--------------------------------------------------------------------------------------------------
	header = sock.recv(3).decode("ascii")

	if header != "SET":
		print("Protocol Error at SET")
	else:
		(agent_state['height'], agent_state['width'] )= receive_data(sock, 2, "2B")

	# HUM----------------------------------------------------------------------------------------------------
	header = sock.recv(3).decode("ascii")

	if header != "HUM":
		print("Protocol Error at HUM")
	else:
		agent_state['number_of_homes'] = receive_data(sock, 1, "1B")[0]
		agent_state['homes_raw'] = receive_data(sock, agent_state['number_of_homes'] * 2, "{}B".format(agent_state['number_of_homes'] * 2))
    
	# HME--------------------------------------------------------------------------------------------------------
	header = sock.recv(3).decode("ascii")

	if header != "HME":
		print("Protocol Error at HME")
	else:
		agent_state['start_position'] = tuple(receive_data(sock, 2, "2B"))

	# MAP--------------------------------------------------------------------------------------------------------
	header = sock.recv(3).decode("ascii")

	if header != "MAP":
		print("Protocol Error at MAP")
	else:
		agent_state['number_map_commands'] = receive_data(sock,1, "1B")[0]
		agent_state['map_commands_raw'] = receive_data(sock, agent_state['number_map_commands'] * 5, "{}B".format(agent_state['number_map_commands'] * 5))

	print(agent_state)
	print('------------------------------------------------------------------------------------------')

	#Creating a Numpy Array for Board.
	board_cell_dict = {'cell_human_count':0,'cell_vampire_count':0,'cell_werewolves_count':0}
	board_matrix = np.full(shape=(agent_state['height'],agent_state['width']),fill_value=board_cell_dict)
	#print(board_matrix)

	#Update_Board_Matrix
	board_matrix = update_board_matrix(board_matrix,agent_state)

	#print('The board Matrix: ')
	#print(board_matrix[3][4])


	# Identify Who we are
	species_dict = identify_species(board_matrix,agent_state)

	if species_dict['our_species'] == 'vampires':
		print('We are vampires')
	elif species_dict['our_species'] == 'werewolves':
		print('We are werewolves')

	#Send Move Command Randomly or through using Seach Methods
	#send_move(sock,'MOV')
	
	playing_game(sock,agent_state,board_matrix,species_dict)

#---------------------------------------------------------------------------------------------------------------
def playing_game(sock,agent_state,board_matrix,species_dict):

	#send_move(sock,'MOV')

	while True:
		# UPD---------------------
		header = sock.recv(3).decode("ascii")

		#print(header)

		if header == "UPD":
			print('A UPD Packet has been received')
			agent_state['number_map_commands'] = receive_data(sock,1, "1B")[0]
			agent_state['map_commands_raw'] = receive_data(sock, agent_state['number_map_commands'] * 5, "{}B".format(agent_state['number_map_commands'] * 5))


			print(agent_state)
			print('------------------------------------------------------------------------------------------')
			board_matrix = update_board_matrix(board_matrix,agent_state)

			# Send Move Command Randomly or through using Seach Methods
			# Also print the Board Matrix
			send_move(sock,'MOV')

		# END--------------------------------------------------------------------------------------------------------------

		elif header == "END":
			print('The END Packet has been received')
			print("The Game has ended")
			print("Closing the connection now")
			sys.exit()
			sock.close()

		#BYE------------------------------------------------------------------------------------------------------------

		elif header == "BYE":
			print('BYE Packet has been received')
			print("Closing the connection now")
			sock.close()

#---------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	start_game()