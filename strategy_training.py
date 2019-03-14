#!/usr/bin/env python
# coding: utf-8

# # Vampire Werewolves strategy training

# ## 1.Dependencies

# In[ ]:


import numpy as np
import random
import copy
import time
import pickle
USE_PICKLE = False


# ## 2.Board object
# Structure and initialisation

# In[ ]:


class Point:
    """
    Code a point with its coordinates and can store a number to this point
    :param&attributes x: int, x coordinate, the row id of the point in the Board (starting from 0)
    :param&attributes y: int, y coordinate, the collumn id of the point in the Board (starting from 0)
    
    OPTIONAL
    :param&attributes n: int, default_value=None, the number of elements in this point
    """
    def __init__(self, x, y, n=None):
        self.x = x
        self.y = y
        self.n = n
    
    def __repr__(self):
        """
        When ask for a print, show the point as 'x_y'
        """
        ret = str(self.x) + "_" + str(self.y)
        if self.n is not None:
            ret += "n" + str(int(self.n))
        return ret
    
        
class Board:
    """
    A game board for the game.
     ------------->  Y
    |
    |
    |
    |
    |
    v
    
    X
    
    3rd dimension used for number of Vampires, Werewolves, Humans
    
    > PARAMETERS
    :param width: int, wdith of the board
    :param height: int, height of the board
    
    :attribute board: a 3 dimensional numpy array to describe the state of the board
        1st dimension : the x dimension (rows)
        2nd dimension : the y dimension (columns)
        3rd dimension : list of 3 numbers: [number_of_vampires, number_of_werewolves, number_of_humans]
    :attribute id_V: int, id of vampires in the 3rd dimension. Should be 0
    :attribute id_W: int, id of werewolves in the 3rd dimension. Should be 1
    :attribute id_H: int, id of humans in the 3rd dimension. Should be 2
    :attribute size: Size, object to store the board size
    :attribute id_board: int, id of the current board
    
    """
    
    # Ids of Vampires, Werewolves and Humans in the 3rd board dimension
    id_V = 0
    id_W = 1
    id_H = 2
        
    def __init__(self, width, height):
        """
        Constuctor of the board. Initialize it with np.zeros
        :param width: int, width of the board
        :param height: int, height of the board
        """
        self.width = width
        self.height = height
        self.board = np.zeros((self.height, self.width, 3), dtype=np.int8)
    
    
    def init_board_set(self, list_vampires, list_werewolves, list_humans, id_board=0):
        """
        Fill a board with known position of species
        :param list_vampires: list of Point, indicating position and number of vampires
        :param list_werewolves: list of Point, indicating position and number of werewolves
        :param list_humans: list of Point, indicating position and number of humans
        """
        self.id_board = id_board
        for vampire_group in list_vampires:
            self.board[vampire_group.x, vampire_group.y, self.id_V] = vampire_group.n
        for werewolf_group in list_werewolves:
            self.board[werewolf_group.x, werewolf_group.y, self.id_W] = werewolf_group.n
        for human_group in list_humans:
            self.board[human_group.x, human_group.y, self.id_H] = human_group.n
        
            
    
    def init_board_random(self):
        """
        Randomly affect vampires, werewolves and human to the board.
        Use still non random parameters : 
            1 group of 10 Vampires
            1 group of 10 Werewolves
            3 groups of 3, 3, 5 humans
        """
        self.id_board = 0
        ## Affecting vampires in board
        n_vampires = 6
        # Creating a list of possible position in board. We positionate vampires first, every position is possible
        potential_vampires_position = [(x,y) for x in range(self.height) for y in range(self.width)]
        vampires_position = random.choice(potential_vampires_position)
        x_vampires, y_vampires = vampires_position
        self.board[x_vampires, y_vampires, self.id_V] = n_vampires
            
        ## Affecting werewolves
        n_werewolves = 4
        # Creating a list of possible position in board. We remove vampires position from possible ones
        potential_werewolves_position = [(x,y) for x in range(self.height) for y in range(self.width)]
        potential_werewolves_position.remove(vampires_position)
        werewolves_position = random.choice(potential_werewolves_position)
        x_werewolves, y_werewolves = werewolves_position
        self.board[x_werewolves, y_werewolves, self.id_W] = n_werewolves
        
        ## Affecting humans
        n_humans = [4, 2, 2, 1]
        humans_position = []
        
        for group_n_humans in n_humans:
            # Creating a list of possible position in board. We remove vampires, werewolves, and other humans positions.
            potential_humans_position = [(x,y) for x in range(self.height) for y in range(self.width)]
            potential_humans_position.remove(vampires_position)
            potential_humans_position.remove(werewolves_position)
            for previous_human_position in humans_position:
                potential_humans_position.remove(previous_human_position)
        
            group_humans_position = random.choice(potential_humans_position)
            # Storing this group position
            humans_position.append(group_humans_position)
            x_group_humans, y_group_humans = group_humans_position
            self.board[x_group_humans, y_group_humans, self.id_H] = group_n_humans
    
    def display(self):
        """
        Display the board in a ergonomic way, with number of Vampires, Werewolves and Humans on cells.
        They cannot be 2 species in the same cell
        """
        
        for x in range(self.height):
            line = ""
            for y in range(self.width):
                line += "|"
                if self.board[x,y,self.id_V] != 0:
                    cell = str(int(self.board[x,y,self.id_V])) + "V"
                    while len(cell) < 3:
                        cell += " "
                    line += cell
                elif self.board[x,y,self.id_W] != 0:
                    cell = str(int(self.board[x,y,self.id_W])) + "W"
                    while len(cell) < 3:
                        cell += " "
                    line += cell
                elif self.board[x,y,self.id_H] != 0:
                    cell = str(int(self.board[x,y,self.id_H])) + "H"
                    while len(cell) < 3:
                        cell += " "
                    line += cell
                else:
                    line += "   "
            
            line += "|"
            print("-"*len(line))
            print(line)
        print("-"*len(line))
    
    def deepcopy(self):
        new_board = Board(self.width, self.height)
        new_board.id_board = self.id_board
        new_board.board = self.board.copy()
        return new_board


# ## 3.Player object
# Moves and their scores

# In[ ]:


class Player:
    """
    An object to describe the player attributes and his potential moves
    
    :attribute name: string, name of the player
    :attribute id_species: int, id of the species used, 0, 1 or 2, see Board object
    :attribute species: string, name of the species, "V" or "W"
    """
    def __init__(self, name, species):
        # Storing player name
        self.name = name
        
        # Storing player species
        if species == "V":
            print(self.name, "is playing vampires")
            self.species = species
            self.id_species = Board.id_V
        elif species == "W":
            print(self.name, "is playing werewolves")
            self.species = species
            self.id_species = Board.id_W
        else:
            raise ValueError("Don't know the species " + str(species))
    
    
    def number_of_creatures(self, game_board):
        """
        Return the numer of friend and enemy creatures in the board
        :param game_board: Board
        :return number_of_our_creatures: int
        :return number_of_enemy_creatures: int
        """
        
        id_enemy_species = (self.id_species+1)%2
        number_of_our_creatures = np.sum(game_board.board[:,:,self.id_species])
        number_of_enemy_creatures = np.sum(game_board.board[:,:,id_enemy_species])
        return number_of_our_creatures, number_of_enemy_creatures
    
    def is_end_of_game(self, game_board):
        """
        Check if the game is still running.
        :param game_board: Board, the game board state to check if the game is ended
        
        :return the_game_is_ended: True if the game is ended, False else
        :return score: 0 if game not ended, +20 if we won, -20 if we lost 
        """
        
        number_of_our_creatures, number_of_enemy_creatures = self.number_of_creatures(game_board)
        
        if number_of_our_creatures == 0:
            # We have no creatures left
            return (True, -20)
        elif number_of_enemy_creatures == 0:
            # We have won, there is no enemy left
            return (True, 20)
        else:
            # The game is not finished yet
            return (False, 0)
    
        
    def possible_moves(self, game_board):
        """
        Compute and return possibles moves with scores.
        
        :param game_board: the game board object
        
        :return moves: list of possibles moves to the format 
            (
            original_point, :Point::
            number_of_creature_moving, :int:
            final_point, :Point
            score, :int:
            new_potential_board :Board:
            )
        """
        
        # Scanning where are our creatures
        our_creatures_groups_position_raw = np.argwhere(game_board.board[:,:,self.id_species] != 0)
        
        # Storing their position as a Point object and storing the number of creatures in each group
        our_creatures_groups_position = []
        our_creatures_groups_population = []
        for group_position_raw in our_creatures_groups_position_raw:
            group_position = Point(group_position_raw[0], group_position_raw[1])
            our_creatures_groups_position.append(group_position)
            our_creatures_groups_population.append(game_board.board[group_position.x, group_position.y, self.id_species])
        
        # NOTE : for now, we will not consider splitting the creatures group
        
        # Exploring possible moves for each group
        moves = []
        for id_group, group_position in enumerate(our_creatures_groups_position):
            for delta_x in [-1, 0, 1]:
                for delta_y in [-1, 0, 1]:
                    new_x = group_position.x + delta_x
                    new_y = group_position.y + delta_y
                    if new_x < 0 or new_x >= game_board.height or new_y < 0 or new_y >= game_board.width or (delta_x == 0 and delta_y == 0):
                        # The new point is out of the game board
                        continue
                    else:
                        new_potential_position = Point(new_x, new_y)
                        group_population = our_creatures_groups_population[id_group]
                        score, new_board = self.score_move(group_position, group_population, new_potential_position, game_board)
                        if score == -666:
                            # We are not allowing this move
                            continue
                        moves.append([group_position, group_population, new_potential_position, score, new_board])
        return moves
            
    
    def score_move(self, origin_position, our_creature_population, target_position, game_board):
        """
        Return the score of the proposed creatures move along with the new board related to this move
        
        :param origin_position: Point, where the creatures came from
        :param our_creature_population: int, number of creatures moving
        :param target_position: Point where the creature are going to
        :param game_board: Board, the board state before the move
        
        :return score: 
            -666: if the move is forbidden
            <0: if the move makes us loss creatures more than killing others for instance 
            0: if the move is neutral
            >0: if we have converted humans, or kill other creatures more than they killed us
        :return new_game_board: Board, The new Board after applying the move
        """
        
        target_cell = game_board.board[target_position.x, target_position.y]

        if max(target_cell) == 0:
            # There are no species in this cell, we apply a neutral score
            ## Lets build the new board of this potentality
            new_game_board = game_board.deepcopy()
            new_game_board.id_board += 1
            # We are leaving the original cell
            new_game_board.board[origin_position.x, origin_position.y, self.id_species] = 0
            # We move to the new cell
            new_game_board.board[target_position.x, target_position.y, self.id_species] = our_creature_population
            return 0, new_game_board
            
        elif target_cell[self.id_species] != 0:
            # We are merging with our own species
            # print(target_cell)
            #we haven't considered splitting, neither merging, groups yet. We forbid the move
            return -666, None
        
        elif target_cell[game_board.id_H] != 0:
            # We are meeting humans
            number_of_humans = target_cell[game_board.id_H]
            if our_creature_population >= int(number_of_humans*1.5):
                # If we are 50% more than humans, we convert all of them
                # Lets consider this as a score equal to "number of converted humans"
                score = number_of_humans*2
                ## Lets build the new board of this potentality
                new_game_board = game_board.deepcopy()
                new_game_board.id_board += 1
                # We are leaving the original cell
                new_game_board.board[origin_position.x, origin_position.y, self.id_species] = 0
                # We are removing humans from the targeted cell
                new_game_board.board[target_position.x, target_position.y, game_board.id_H] = 0
                # We sum number of converted humans and previous our_creatures to create new number of our_creatures
                new_game_board.board[target_position.x, target_position.y, self.id_species] = number_of_humans + our_creature_population
                return score, new_game_board
            
            else:
                E1 = our_creature_population
                E2 = number_of_humans
                if E1 <= E2:
                    P = float(E1)/(2*E2) # force the use of float if using Python2
                    
                else:
                    P = float(E1)/E2 - 0.5
                
                # We win with the propability P. Let's consider esperency
                if P <= 0.5 or number_of_humans >= int(our_creature_population*1.5):
                    ## We have lost the battle. We lose all our creatures and humans also have loses:                    
                    # Lets compute number of humans after battle
                    if number_of_humans >= int(our_creature_population*1.5):
                        number_of_humans_after_battle = number_of_humans
                    else:
                        number_of_humans_after_battle = int((1-P)*number_of_humans)
                    
                    ## Lets build the new board of this potentality
                    new_game_board = game_board.deepcopy()
                    new_game_board.id_board += 1
                    # We are removed from the original cell
                    new_game_board.board[origin_position.x, origin_position.y, self.id_species] = 0
                    # We are refreshing number of humans in the targeted cell
                    new_game_board.board[target_position.x, target_position.y, game_board.id_H] = number_of_humans_after_battle
                    if P == 0.5:
                        return 0, new_game_board
                    return -our_creature_population, new_game_board
                
                else:
                    # We have won the battle. We convert P% of humans and we have a P% chance to survive
                    our_creature_population_after_battle = int(P*(our_creature_population + number_of_humans))
                    ## Lets build the new board of this potentality
                    new_game_board = game_board.deepcopy()
                    new_game_board.id_board += 1
                    # We are moving from the original cell
                    new_game_board.board[origin_position.x, origin_position.y, self.id_species] = 0
                    # We remove humans from the targeted cell
                    new_game_board.board[target_position.x, target_position.y, game_board.id_H] = 0
                    # We are comming in the targeted cell, after winning in the battlefield
                    new_game_board.board[target_position.x, target_position.y, self.id_species] = our_creature_population_after_battle
                    return our_creature_population_after_battle, new_game_board
                
        else:
            # If not humans and not our species, but still there is a species in this cell, it is the enemy creature
            enemy_id = (self.id_species + 1)%2
            number_of_enemy = target_cell[enemy_id]

            if our_creature_population >= int(number_of_enemy*1.5):
                # We are killing every enemy
                # Lets consider this as a score equal to "number of converted humans" with a weight
                score = number_of_enemy*2
                
                ## Lets build the new board of this potentality
                new_game_board = game_board.deepcopy()
                new_game_board.id_board += 1
                # We are leaving the original cell
                new_game_board.board[origin_position.x, origin_position.y, self.id_species] = 0
                # We are removing enemies from the targeted cell
                new_game_board.board[target_position.x, target_position.y, enemy_id] = 0
                # We move to the new cell
                new_game_board.board[target_position.x, target_position.y, self.id_species] = our_creature_population
                return score, new_game_board
            
            else:
                E1 = our_creature_population
                E2 = number_of_enemy
                if E1 < E2:
                    P = float(E1)/(2*E2) # force the use of float if using Python2
                else:
                    P = float(E1)/E2 - 0.5
                
                # We win with the propability E1. Let's consider esperency
                if P<=0.5 or int(our_creature_population*1.5) <= number_of_enemy:
                    ## We have lost the battle. 
                    # Lets compute number of enemies after battle:
                    if our_creature_population*1.5 <= number_of_enemy:
                        number_of_enemy_after_battle = number_of_enemy
                    else:
                        number_of_enemy_after_battle = int((1-P)*number_of_enemy)
                    
                    ## Lets build the new board of this potentality
                    new_game_board = game_board.deepcopy()
                    new_game_board.id_board += 1
                    # We are removed from the original cell
                    new_game_board.board[origin_position.x, origin_position.y, self.id_species] = 0
                    # We are refreshing number of enemies in the targeted cell
                    new_game_board.board[target_position.x, target_position.y, enemy_id] = number_of_enemy_after_battle
                    if P == 0.5:
                        return 0, new_game_board
                    return -our_creature_population, new_game_board
                
                else:
                    # We have won the battle. We kill every enemy and we have a P% chance to survive
                    our_creature_population_after_battle = int(P*our_creature_population)
                    ## Lets build the new board of this potentality
                    new_game_board = game_board.deepcopy()
                    new_game_board.id_board += 1
                    # We are moving from the original cell
                    new_game_board.board[origin_position.x, origin_position.y, self.id_species] = 0
                    # We are removing the enemy from the original cell
                    new_game_board.board[origin_position.x, origin_position.y, enemy_id] = 0
                    # We are comming in the targeted cell, after winning in the battlefield
                    new_game_board.board[target_position.x, target_position.y, self.id_species] = our_creature_population_after_battle
                    return our_creature_population_after_battle, new_game_board
    
    def display_moves(self, moves):
        for id_move, move in enumerate(moves):
            print("-"*10)
            print("Move n°", id_move)
            group_position, group_population, new_potential_position, score, new_board = move
            print("Moving", group_population, self.species, "from", group_position, "to", new_potential_position)
            print("Scored", score)
            print("New board:")
            new_board.display()
        


# ## 4.Game tree architecture
# Build a tree of the potential possibilities

# In[ ]:


class Migration:
    """
    Object to store a migration of a number of creatures from a Point to another
    
    :param&attribute origin_position: Point
    :param&attribute population: integer, number of creatures moving
    :param&attribute target_position: Point
    """
    def __init__(self, origin_position, population, target_position):
        self.origin_position = origin_position
        self.population = int(population)
        self.target_position = target_position
    
    def __repr__(self):
        return("Moving " + str(self.population) + " from " + str(self.origin_position) + " to " + str(self.target_position))

class Node:
    def __init__(self, name, last_player, next_player, game_board, score, friend_is_next_player, depth, father, migration, max_depth):
        """
        A game_tree node: a state of the game
        
        :param name: string, name of the node
        :param last_player: Player, the last player to have plated
        :param next_player: Player, the next player
        :param game_board: Board, a game_board object
        :param score: int, the inner score of this node
        :param friend_is_next_player: boolean, True if the next player to move is the friend
        :param depth: int, actual depth in the search tree
        :param father: Node, the father node
        :param migration: Migration, the migration object the lead to this node
        :param max_depth: int, the maximum depth of a node
        
        :attribute value: int, the value of the node, for the alpha_beta search algorithm
        
        """
        self.name = name
        self.last_player = last_player
        self.next_player = next_player
        self.game_board = game_board
        self.score = score
        self.friend_is_next_player = friend_is_next_player
        self.depth = depth
        self.father = father
        self.migration= migration
        self.max_depth = max_depth
        self.__value = None
        self.__childrens = None
    
    def display_board(self):
        print("Node", self.name)
        self.game_board.display()
    
    def childrens(self, verbose=False):
        """
        Compute and return children if needed
        """
        if self.__childrens == None:
            self.__childrens = self.get_childrens(verbose=verbose)
        
        return self.__childrens
            
    
    def get_childrens(self, verbose=False):
        """
        Compute and return the childrens of the node.
        Manage the value affectation when we are reaching max depth
        
        :param verbose: boolean, set to True to display more information on nodes.
        :return childrens: list of Nodes, the potential Nodes generated from the current state
            return [] if the game is ended of if we have reached the maximum depth
        
        """
        ## Check if last node : max_depth or if the game is ended
        the_game_is_ended, end_score = self.next_player.is_end_of_game(self.game_board)
        if the_game_is_ended or self.depth >= self.max_depth:
            return []
        
        ## Create childrens
        childrens = []
        moves = self.next_player.possible_moves(self.game_board)
        for id_move, move in enumerate(moves):
            origin_position, population, target_position, score, new_board = move
            
            # Checking if not already explored state
            father = self.father
            visited = False
            while father is not None and not visited:
                if np.array_equal(father.game_board.board, new_board.board):
                    visited = True
                father = father.father
            if visited:
                continue
            
            migration = Migration(origin_position, population, target_position)
            childrens.append(
                Node(
                    name=self.name + str(id_move),
                    last_player=self.next_player,
                    next_player=self.last_player,
                    game_board=new_board,
                    score=score,
                    friend_is_next_player=self.friend_is_next_player==False,
                    depth=self.depth+1,
                    father=self,
                    migration=migration,
                    max_depth=self.max_depth
                )
            )
        return childrens
    
    def value(self):
        if self.__value == None:
            self.__value = self.get_value()
        return self.__value
    
    def get_value(self):        
        # Get scores from father, giving enemy scores as malus
        value = 0
        father = self
        scores = []
        while father is not None:
            if father.friend_is_next_player:
                scores.append(-father.score)
            else:
                scores.append(father.score)
            father = father.father
        
        number_of_our_creatures, number_of_enemy_creatures = self.next_player.number_of_creatures(self.game_board)
        balance_creatures = number_of_our_creatures - number_of_enemy_creatures
        
        if self.friend_is_next_player:
            value += balance_creatures
        else:
            value -= balance_creatures
        
        # Put more weight on wining the game sooner
        if (number_of_enemy_creatures == 0 and self.friend_is_next_player)         or (number_of_our_creatures == 0 and not self.friend_is_next_player):
                value += self.max_depth - self.depth
        
        if (number_of_our_creatures == 0 and self.friend_is_next_player)         or (number_of_enemy_creatures == 0 and not self.friend_is_next_player):
                value -= self.max_depth - self.depth
        
        # Put more weight on gaining score quickly
        if max(scores) > 0:
            value += (1+np.argmax(scores))*0.1
        return value
            
    
    def display_tree(self):
        print(("-" + str(self.depth) + "-")*self.depth + self.name + " score:" + str(self.score) + " value:" + str(self.value()))
        self.game_board.display()
        for child in self.childrens():
            if child is not None:
                child.display_tree()
            
        
class GameTree:
    def __init__(self, our_player, enemy_player, init_game_board, friend_is_next_player=True, max_depth=6):
        if friend_is_next_player:
            last_player = enemy_player
            next_player = our_player
        else:
            last_player = our_player
            next_player = enemy_player
        self.root = Node(
            name="root",
            last_player=last_player,
            next_player=next_player,
            game_board=init_game_board,
            score=0,
            friend_is_next_player=friend_is_next_player,
            depth=0,
            father=None,
            migration=None,
            max_depth=max_depth
        )
    
    def display(self):
        self.root.display_tree()


# ## 5.Alpha-Beta
# Use the game tree and alpha-beta technique to select the best move to perform

# In[ ]:


class AlphaBeta:
    """
    The alpha beta search tool to explore the game_tree and generate only usefull chidlrens
    
    :param game_tree: GameTree, the tree of the game
    :param verbose: boolean, set to true to display the min-max computations
    """
    def __init__(self, game_tree, verbose=False):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        self.verbose = verbose

    def alpha_beta_search(self, node):
        """
        Manage the alpha beta search by callig the max_value and min_value functions
        :param node: Node, the current state node
        
        :return best_state: Board, the best board to move to
        :return best_val: int, the hoped value with this move
        :return child_depth_2
        """
        if USE_PICKLE:
            try:
                with open('child_depth_2.pickle', 'rb') as file:
                    print("restoring child depth 2")
                    child_depth_2 = pickle.load(file)

                for child in child_depth_2:
                    if np.array_equal(node.game_board.board, child.game_board.board):
                        print("Already seen state. Using memory")
                        node.__childrens = child.__childrens
                        break
            except FileNotFoundError:
                print("No memory file")
        
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        
        # Store best states and vals to choose when having multiple possibilites
        best_states = []
        best_vals = []
        
        for state in successors:
            value = self.min_value(state, best_val, beta)
            
            if value > best_val:
                best_val = value
                best_state = state
                # We have reached a better state, delete previous best states
                best_states = []
                best_vals = []
            if value == best_val:
                # If we have the same result, store it if we have to choose
                best_vals.append(value)
                best_states.append(state)
        
        # Choose if multiple best moves
        if len(best_states) > 0:
            # We have multiple best moves. We have to choose one.
            # If we outnumber enemies by 50%, move towards them
            # Else, move toward the closest group of human we outnumber of more than 50%
            # >>> Move toward the closest group we are more than 50% of.
            
            # Compute position of group to attack
            number_our_creatures, _ = state.last_player.number_of_creatures(state.game_board)
            # Get groups where there is creatures (> 0) and that we outnumber by more that 50%
            positions_to_attack = np.argwhere(
                (state.game_board.board[:,:,:] > 0) & (state.game_board.board[:,:,:] <= number_our_creatures/1.5)
            )
            
            # If not group we outnumber, check if we are as numerous as other groups, and go toward them
            if len(positions_to_attack) == 0:
                # We have multiple best moves. We have to choose one.
                # If we outnumber enemies by 50%, move towards them
                # Else, move toward the closest group of human we outnumber of more than 50%
                # >>> Move toward the closest group we are more than 50% of.

                # Compute position of group to attack
                number_our_creatures, _ = state.last_player.number_of_creatures(state.game_board)
                # Get groups where there is creatures (> 0) and that we outnumber by more that 50%
                positions_to_attack = np.argwhere(
                    (state.game_board.board[:,:,:] > 0) & (state.game_board.board[:,:,:] <= number_our_creatures)
                )
            
            # If no such group
            if len(positions_to_attack) == 0:
                # We will avoid the groups
                try:
                    # Avoid enemies
                    positions_to_avoid = np.argwhere(state.game_board.board[:,:,state.next_player.id_species] > 0)
                    id_best_state = 0
                    max_dist = 0
                    for i, state in enumerate(best_states):
                        # Get our position
                        our_position = np.argwhere(state.game_board.board[:,:,state.last_player.id_species] != 0)[0]
                        # Check if position to attack is the closest to us
                        for position_to_avoid in positions_to_avoid:
                            dist = np.linalg.norm(our_position-position_to_avoid[0:2])
                            # If is the closest, store this state as the best one
                            if dist > max_dist:
                                id_best_state = i
                                max_dist = dist
                    print("Trying to escape with dist", round(max_dist, 2))
                    best_val = best_vals[id_best_state]
                    best_state = best_states[id_best_state]
                except IndexError:
                    # The escape moves are not possible. Lets play random
                    print("Cannot escape")
                    id_best_state = random.randint(0, len(best_states) - 1)
                    best_val = best_vals[id_best_state]
                    best_state = best_states[id_best_state]
            
            # If such group exist
            else:
                id_best_state = 0
                min_dist = np.inf
                for i, state in enumerate(best_states):
                    # Get our position
                    our_position = np.argwhere(state.game_board.board[:,:,state.last_player.id_species] != 0)[0]
                    # Check if position to attack is the closest to us
                    for position_to_attack in positions_to_attack:
                        dist = np.linalg.norm(our_position-position_to_attack[0:2])
                        # If is the closest, store this state as the best one
                        if dist < min_dist:
                            id_best_state = i
                            min_dist = dist
                best_val = best_vals[id_best_state]
                best_state = best_states[id_best_state]            
            
        if self.verbose:
            print("AlphaBeta:  Utility Value of Root Node: = " + str(best_val))
            print("AlphaBeta:  Best State is: " + best_state.name)
        
        # Store 2nd level child to try to improve computational power if this child is appearing
        child_depth_2 = best_state.childrens(node)
        if USE_PICKLE:
            with open('child_depth_2.pickle', 'wb') as file:
                pickle.dump(child_depth_2, file, protocol=pickle.HIGHEST_PROTOCOL)
        
        return best_state, best_val

    def max_value(self, node, alpha, beta):
        """
        Max value function for the alpha beta search
        :param node: Node
        :param alpha: int
        :param beta: int
        
        :return value: int
        """
        if self.verbose:
            print("AlphaBeta-->MAX: Visited Node :: " + node.name)
            # node.display_board()
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        """
        Max value function for the alpha beta search
        :param node: Node
        :param alpha: int
        :param beta: int
        
        :return value: int
        """
        if self.verbose:
            print("AlphaBeta-->MIN: Visited Node :: " + node.name)
            # node.display_board()
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        """
        Get the node childrens as we need them
        :param node; Node
        
        :return childrens: list of Nodes, the children nodes
        """
        assert node is not None
        return node.childrens(self.verbose)

    def isTerminal(self, node):
        """
        Check if the node is a terminal one
        :param node: Node
        :return is_terminal: boolean, True if is terminal, False else
        """
        assert node is not None
        num_childrens = len(node.childrens(self.verbose))
        return num_childrens == 0

    def getUtility(self, node):
        """
        Get the value of a node
        :param node: Node
        :return value: int, the node value
        """
        assert node is not None
        return node.value()


# ## 6.Interface strategy
# Interface the strategy with the project

# In[ ]:


def interface_strategy(width, height, list_vampires, list_werewolves, list_humans, our_species, max_depth=6, our_name="Us", enemy_name="Them", verbose=0):
    """
    > MANDATORY PARAMETERS
    :param width: int, width of the board
    :param height: int, height of the board
    :param list_vampires: list of Point describing where are the vampires. It can be on length 1 or more.
    :param list_werewolves: list of Point describing where are the werewolves. It can be on length 1 or more.
    :param list_humans: list of Point describing where are the werewolves. It can be on length 0 or more.
    :param our_species: string, "V" if we play vampires, "W" if we play werewolves
    
    > OPTIONAL PARAMETERS
    :param max_depth: int, default_value = 6, maximum depth of the game tree. Higher give better prediction but cost computation time.
    :param our_name: string, default_value = "Us" the name of the team we are playing. 
    :param enemy_name: string, default_value = "Them" the name of the enemy team. 
    :param verbose: integer, default_value = 0, put to 0 for nothing, 1 for the board, 2 for the whole strategy process.
    
    > RETURN
    :return best_move_migration: Migration, the best migration computed from the state provided
    """
    # Compute time
    tic = time.time()
    
    # Basic input check
    assert our_species == "W" or "V"
    assert height and width > 0
    assert len(list_werewolves) > 0 and len(list_werewolves) > 0
    
    # Get enemy species
    enemy_species = "W" if our_species == "V" else "V"
    
    # Creating board
    game_board = Board(width=width, height=height)
    game_board.init_board_set(
                list_vampires=list_vampires,
                list_werewolves=list_werewolves,
                list_humans=list_humans)
    
    # Creating players
    our_player = Player(our_name, our_species)
    enemy_player = Player(enemy_name, enemy_species)
    
    # Creating game tree
    game_tree = GameTree(
        our_player=our_player, 
        enemy_player=enemy_player, 
        init_game_board=game_board, 
        friend_is_next_player=True,
        max_depth=max_depth)
    
    # Init alpha beta object
    alpha_beta = AlphaBeta(game_tree, verbose=verbose==2)
    
    # Compute and display best move
    best_move, best_val = alpha_beta.alpha_beta_search(alpha_beta.root)
    
    if verbose > 0:
        # Display initial state
        game_tree.root.display_board()
        # Display best move
        print("best move:", best_move.migration, "Hoping for", round(best_val, 4))
        best_move.display_board()
        number_of_our_creatures, number_of_enemy_creatures = our_player.number_of_creatures(best_move.game_board)
        print("Computed in", round(time.time() - tic, 3), "seconds")
        if verbose > 1:
            print("Tree:")
            game_tree.display()
    
    # Return the action to perform
    return best_move.migration


# ## 7.Test Strategy
# Test the strategy with random and selected state

# In[ ]:


class TestStrategy:
    def test_unit(is_random, max_depth):
        tic = time.time()
        if is_random:
            # Init random size
            height = random.randint(6, 10)
            width = random.randint(6, 10)
            # Board size
            game_board = Board(width=width, height=height)
            # Random init
            game_board.init_board_random()
            # Define players
            player1 = Player("Dracula", "V")
            player2 = Player("Garou", "W")
            # Init game_tree
            game_tree = GameTree(
                our_player=player1, 
                enemy_player=player2, 
                init_game_board=game_board, 
                friend_is_next_player=True,
                max_depth=max_depth)
            # Init alpha beta object
            alpha_beta = AlphaBeta(game_tree, verbose=False)
            # Display initial state
            game_tree.root.display_board()
            # Compute and display best move
            best_move, best_val = alpha_beta.alpha_beta_search(alpha_beta.root)
            # Display best move
            print("best move:", best_move.migration, "Hoping for", round(best_val, 4))
            best_move.display_board()
            number_of_our_creatures, number_of_enemy_creatures = player1.number_of_creatures(best_move.game_board)
            print("number of our creatures", number_of_our_creatures)
            print("number of enemy creatures", number_of_enemy_creatures)
            print("Computed in", round(time.time() - tic, 3), "seconds")
            print("Tree:")
            # game_tree.display()
        
        else:
            ## INTERFACE TEST
            print("Your implementation. Take care of converting to the strategy referential (X is in the height)")
            interface_strategy(
                width=10, 
                height=5, 
                list_vampires=[Point(2, 3, 10)], 
                list_werewolves=[Point(1, 4, 4), Point(4, 4, 2)], 
                list_humans=[Point(2, 2, 4), Point(0, 9, 2), Point(4, 9, 2), Point(2, 9, 1)], 
                our_species="V", 
                max_depth=max_depth, 
                our_name="Dracula", 
                enemy_name="Garou", 
                verbose=1)
    
    @staticmethod
    def multiple_test(number_of_test, max_depth):
        
        print(">>> Board set test")
        TestStrategy.test_unit(is_random=False, max_depth=max_depth)
        print("="*30, "\n")
        
        print(">>> Random tests")
        for id_test in range(number_of_test):
            print("Test", id_test + 1)
            TestStrategy.test_unit(is_random=True, max_depth=max_depth)
            print("="*30, "\n")

## Uncomment to run tests
# TestStrategy.multiple_test(number_of_test=10, max_depth=3)
# %prun TestStrategy.test_unit(is_random=False, max_depth=5)

