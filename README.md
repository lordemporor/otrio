# otrio
Otrio Q-Learning Project

This is an attempt of using Q-Learning on a board game called Otrio by lordemporor and broskisworld in Python.  
If you would like more context look up the game and how to play and win  
The project is split into 4 python modules, not all are finished yet.  
otriogameboard runs the main board game work, placing rings, telling what places you can go, if someone has won.  
otrioaigym (something like that) trains the ai, and will create a file of the ai's neural network  
otriographics interfaces with the human player(s)  
otriomanager manages the game. It creates a game and asks each group what they would like to do  
  
otriomanager requests from the seperate modules to play when it decides its their turn.  
There are 4 types of players:  
Random - Places in a random spot that is allowed  
Algorithm - An algorithm that just tries to win. It doesn't block nor try to win in two places at once  
 Note: *Algorithm would be super easy against a human, its made solely for training the ai how to block*  
Human - A human player interfaced through otriographics.py  
Ai - Q-Learning AI that is the main goal of the project, to make a decent one.  
  
These four types of players can be mismatched in a game to any amount in otriomanager.  
However there are some combinations that wouldn't work well (Anything with only Algorithm and Random)  
