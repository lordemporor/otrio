from otriogameboard import game
from otriographics import window
from random import randint


class player():
    def __init__(self, current_game, id):
        self.current_game = current_game
        self.id = id

    def do_turn(self):
        pass


class human_player(player):
    def __init__(self,current_game,id):
        super().__init__(current_game,id)
        self.type = "human"

    def do_turn(self):
        #When graphics is done implement that here



class ai_player(player):
    def __init__(self,current_game,id):
        super().__init__(current_game,id)
        self.type = "ai"

    def do_turn(self):



class random_player(player):
    def __init__(self,current_game,id):
        super().__init__(current_game,id)
        self.type = "random"

    def do_turn(self):
        position = self.current_game.all_letter_name_positions[randint(0,len(self.current_game.all_letter_name_positions - 1))]
        ring = randint(1,3)
        while not(self.current_game.place_ring(position,ring,self.id)):
            position = self.current_game.all_letter_name_positions[randint(0, len(self.current_game.all_letter_name_positions - 1))]
            ring = randint(1, 3)


print("Game creation starting")
window = window()
print("Window created")
print("Switching to window terminal")
window.terminal()
loop = game(int(input("Number of players (int)? ")))