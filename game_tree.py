import numpy as np


class Player:
    def __init__(self, is_friend):
        self.is_friend = is_friend


class Opponent(Player):
    def __init__(self):
        super().__init__(is_friend=False)


class Friend:
    def __init__(self):
        super().__init__(is_friend=True)


class GameBoard:
    def __init__(self, np_matrix):
        self.matrix = self.create_object_matrix(np_matrix)

    def create_object_matrix(self, np_matrix):
        """
        Make a game board using np_matrix syntax to have an object oriented architecture
        :param np_matrix:
        :return: game board matrix
        """
        pass


class GameNode:

    def __init__(self, board, is_friend_turn):
        self.moves = ['N', 'E', 'S', 'W']
        self.child = {move: None for move in self.moves}
        self.board = board
        self.friend_moving = is_friend_turn
        for i, move in enumerate(self.moves):
            if self.is_possible(move):
                new_board = self.compute_new_board(move)
                self.child[move] = GameNode(new_board)

    def compute_new_board(self, move, ):
        """
        Compute new board from wanted move
        :param move:
        :return:
        """
        print(self.friend_moving)
        print(move)
        print(self.board)
        # TODO

    def is_possible(self, move):
        """
        Return True if move is possible in board, False if not
        :param move:
        :return:
        """
        print(move)
        print(self.board)
        # TODO : return true if move


class GameTree:
    def __init__(self, board):
        self.board = board
