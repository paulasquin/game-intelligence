# game-intelligence
Game from CentraleSupélec on Artificial Intelligence dual team confrontation by [Ayush Rai](https://www.linkedin.com/in/ayush-rai-8ab9b24a/) and [Paul Asquin](https://www.linkedin.com/in/paulasquin).

# Install the project  

## Clone the repo
Be sure to execute the project in a Windows environnement, as the server to run the tests is a .exe file written to work exclusively on Windows.  
Then run:   
```bash
git clone https://github.com/2018-cs-msc-fai-team6/game-intelligence.git
cd game-intelligence
```

## Get the dependencies
```bash
pip3 install -r requirements.txt
```

# Start the project  
Run the program Resources/VampiresVSWerewolvesGameServer.exe then execute from the "game-intelligence" folder:  
```bash
python3 main.py
```

# Functions explaination

## interface_strategy
This function allows us to compute the best move to perfom given a game state. 

Here is the way to use it:

```
from strategy_training import *

best_move_migration = interface_strategy(width, height, list_vampires, list_werewolves, list_humans, our_species, max_depth, our_name, enemy_name, verbose):
```
Here is how to use it

```
"""
NOTE : Point is an object declared in this file, with x, y and n attibutes, 
It is used to describe positon and population of creatures in the board.

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

NOTE : Migration is an object declared in this file. it has attributes
    :attribute origin_position: Point, the position of our creatures moving
    :attribute population: integer, the number of our creatures moving
    :attribute target_position: Point, the position where the creatures are moving

> RETURN
:return best_move_migration: Migration, the best migration computed from the state provided

"""
```