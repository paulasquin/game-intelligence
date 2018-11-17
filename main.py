import server
import strategy
import time

SERVER_PROGRAM_PATH = 'game-intelligence\\Resources\\VampiresVSWerewolvesGameServer'


def main():
    # server.start_server(SERVER_PROGRAM_PATH)
    host = 'localhost'
    port = 5555
    srv = server.Server(host, port)
    srv.send_move('MOV')
    time.sleep(1)
    #strategy.playing_game(srv.sock, srv.agent_state, srv.board_matrix, srv.species_dict)
    strategy.playing_game(srv)

if __name__== '__main__':
    main()