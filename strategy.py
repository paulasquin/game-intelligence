import sys
import tools


def playing_game(srv):
    # send_move(sock,'MOV')
    while True:
        # UPD---------------------
        header = srv.sock.recv(3).decode("ascii")
        if header == "UPD":
            print('A UPD Packet has been received')
            srv.update_agent_state()
            print(srv.agent_state)
            print('------------------------------------------------------------------------------------------')
            srv.update_board_matrix()

            # Send Move Command Randomly or through using Search Methods
            # Also print the Board Matrix
            srv.send_move('MOV')

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
