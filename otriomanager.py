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
        pass #temporary



class ai_player(player):
    def __init__(self,current_game,id):
        super().__init__(current_game,id)
        self.type = "ai"

    def do_turn(self):
        pass #temporary


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


class algorithm_player(player):
    def __init__(self,current_game,id):
        super().__init__(current_game,id)
        self.type = "algorithm"

    def do_turn(self):
        #Largely copied from otriogameboards checkWin functions
        win_types = ["123", "321", "111", "222", "333"]
        pre_sorted_win_completions = []
        # Read: First 9 Same Place, Horizontal Level 1 with Each Win Type, Horizontal Level 2, etc.,
        # Vertical Level 1 with Each Win Type, etc., Diagonal #1 with Each Win Type
        for i in range(49):
            pre_sorted_win_completions.append(0)
        winDetected = False
        #Same Place Check, Items 0-8
        letter_count = 0
        for letter in self.current_game.all_letter_name_positions:
            place_reference = self.current_game.gameboard[self.current_game.letterPositionLookUp(letter)[0]][self.current_game.letterPositionLookUp(letter)[1]]
            if place_reference[0] == self.id:
                pre_sorted_win_completions[letter_count] += 1
            if place_reference[1] == self.id:
                pre_sorted_win_completions[letter_count] += 1
            if place_reference[2] == self.id:
                pre_sorted_win_completions[letter_count] += 1
            letter_count += 1
        #Hoz, Items 9-23
        item_count = 0
        for i in range(3):
            for win_type in win_types:
                if self.current_game.gameboard[0][i][int(win_type[0]) - 1] == self.id:
                    pre_sorted_win_completions[item_count + 9] += 1
                if self.current_game.gameboard[1][i][int(win_type[1]) - 1] == self.id:
                    pre_sorted_win_completions[item_count + 9] += 1
                if self.current_game.gameboard[2][i][int(win_type[2]) - 1] == self.id:
                    pre_sorted_win_completions[item_count + 9] += 1
                item_count += 1
        #Ver, Items 24-38
        item_count = 0
        for i in range(3):
            for win_type in win_types:
                if self.current_game.gameboard[i][0][int(win_type[0]) - 1] == self.id:
                    pre_sorted_win_completions[item_count + 24] += 1
                if self.current_game.gameboard[i][1][int(win_type[1]) - 1] == self.id:
                    pre_sorted_win_completions[item_count + 24] += 1
                if self.current_game.gameboard[i][2][int(win_type[2]) - 1] == self.id:
                    pre_sorted_win_completions[item_count + 24] += 1
                item_count += 1
        #Dia, Items 39-48
        item_count = 0
        for win_type in win_types:
            if self.current_game.gameboard[0][0][int(win_type[0]) - 1] == self.id:
                pre_sorted_win_completions[item_count + 39]
            if self.current_game.gameboard[1][1][int(win_type[1]) - 1] == self.id:
                pre_sorted_win_completions[item_count + 39]
            if self.current_game.gameboard[2][2][int(win_type[2]) - 1] == self.id:
                pre_sorted_win_completions[item_count + 39]
            item_count += 1
        item_count = 0
        for win_type in win_types:
            if self.current_game.gameboard[0][0][int(win_type[0]) - 1] == self.id:
                pre_sorted_win_completions[item_count + 44]
            if self.current_game.gameboard[1][1][int(win_type[1]) - 1] == self.id:
                pre_sorted_win_completions[item_count + 44]
            if self.current_game.gameboard[2][2][int(win_type[2]) - 1] == self.id:
                pre_sorted_win_completions[item_count + 44]
            item_count += 1
        win_completions = sorted(pre_sorted_win_completions, reverse=True)
        print(pre_sorted_win_completions)
        print(win_completions) #Problem to fix for later, we need to remember where the sorted list parts go, so we know where to place


print("Game creation starting")
window = window()
print("Window created")
print("Game creation specifications")
raw_player_count_input = input("Number of players (int)? ")
try:
    player_count = int(raw_player_count_input)
except:
    print("Invalid entry. Quitting...")
    exit()
loop = game(player_count)
# Asking player
players = []
accepted_player_type_entries = ["random", "algorithm", "ai", "human"]
for player_type in accepted_player_type_entries:
    continue_asking_for_players = True
while continue_asking_for_players:
    if len(players) == 0:
        print("No players currently")
    elif len(players) == 1:
        print("Only one player currently")
    else:
        print("There are currently " + str(len(players)) + " players currently")

    raw_player_type_input = ""
    entry_not_accepted = False
    while not (str.lower(raw_player_type_input) in accepted_player_type_entries):
        raw_player_type_input = input("What type of player would you like next?\n")
        if not (str.lower(raw_player_type_input) in accepted_player_type_entries):
            print("Invalid entry")
    players.append(raw_player_type_input)
    if len(players) >= player_count:
        continue_asking_for_players = False

if len(players) == 0:
    print("No players currently")
elif len(players) == 1:
    print("Only one player currently")
else:
    print("There are currently " + str(len(players)) + " players currently")

current_player_turn = 1
gameRunning = True
loop.recreate_gamestate("A110B000C000D000E000F000G000H000I000")
bob = algorithm_player(loop,"1")
bob.do_turn()
