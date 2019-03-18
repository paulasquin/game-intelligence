# game-intelligence
Game from CentraleSupélec on Artificial Intelligence face to face confrontation by [Ayush Rai](https://www.linkedin.com/in/ayush-rai-8ab9b24a/) and [Paul Asquin](https://www.linkedin.com/in/paulasquin).

# Install the project  
The gameboard framework has been developped by our teacher for a Windows environment. Then, if you want to reproduce this project, be sure to run it on a Windows environnement. Still, you can absolutely run game-strategy tests in any environment, using nothing but a jupyter notebook.  

## Clone the repo
```bash
git clone https://github.com/paulasquin/game-intelligence.git
cd game-intelligence
```

## Get the dependencies
Docker may have been an overkill regarding the depencies we need. Just be sure to run this project using python3 and install the requirements:
```bash
pip install -r requirements.txt
```

# Start the project  
Run the program Resources/VampiresVSWerewolvesGameServer.exe then execute from the "game-intelligence" folder:  
```bash
python connect_server.py --myparams 127.0.0.1 5555
```
This will run a instance of a player. Run the same command in a new terminal to connect a second player.

# Files introduction
- [strategy_training.ipynb](strategy_training.ipynb): AI strategy implementation. Dev was done in a jupyter notebook. This is the most important file you want to look at as it is the game strategy.
- [connect_server.ipynb](connect_server.ipynb): Server management implementation. Dev was done in a jupyter notebook.
- ".py: notebook exportation in regular python files to be run for the server connection.
- [Projectv10.pdf](Projectv10.pdf): Project instructions
- Resources Folder: Server runnable file and its dependencies. Use \*.xml and \*.config to configure maps and player max response time.
