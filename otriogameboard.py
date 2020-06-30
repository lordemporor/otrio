class game():
    win_types = ["123", "321", "111", "222", "333"]
    all_letter_name_positions = "ABCDEFGHI"
    open_places = ""
    player_count = 0
    remaining_pieces = []
    game_state_string = ""
    board_len = 0
    gameboard = []
    game_winner = "0"

    def __init__(self, player_count):
        self.reset(player_count)

    # Look up x and y for letter position, accepts letter and returns x,y
    def letterPositionLookUp(self, letter):
        x = 0
        y = 0
        if letter == "A":
            x = 0
            y = 0
        if letter == "B":
            x = 1
            y = 0
        if letter == "C":
            x = 2
            y = 0
        if letter == "D":
            x = 0
            y = 1
        if letter == "E":
            x = 1
            y = 1
        if letter == "F":
            x = 2
            y = 1
        if letter == "G":
            x = 0
            y = 2
        if letter == "H":
            x = 1
            y = 2
        if letter == "I":
            x = 2
            y = 2
        return x, y

    # Enter in position (letter),ring number returns owner of that tile. if empty returns -1
    def placeOwnerLookUp(self, pos, ring):
        fullPositionString = self.gameboard[self.letterPositionLookUp(pos)[0]][self.letterPositionLookUp(pos)[1]]
        return fullPositionString[int(ring) - 1]

    def checkSameWin(self,player):
        winDetected = False
        for letter in self.all_letter_name_positions:
            place_reference = self.gameboard[self.letterPositionLookUp(letter)[0]][self.letterPositionLookUp(letter)[1]]
            if place_reference[0] == place_reference[1] and place_reference[1] == place_reference[2] and place_reference[2] == place_reference[0] and place_reference[0] == player:
                winDetected = True
        return winDetected

    def checkHLineWin(self, i, player):
        winDetected = False
        for win_type in self.win_types:
            if self.gameboard[0][i][int(win_type[0])-1] == player and self.gameboard[1][i][int(win_type[1])-1] == player and self.gameboard[2][i][int(win_type[2])-1] == player:
                winDetected = True
        return winDetected

    def checkVLineWin(self, i, player):
        winDetected = False
        for win_type in self.win_types:
            if self.gameboard[i][0][int(win_type[0])-1] == player and self.gameboard[i][1][int(win_type[1])-1] == player and self.gameboard[i][2][int(win_type[2])-1] == player:
                winDetected = True
        return winDetected

    def checkDiagonalWin(self, player):
        winDetected = False
        for win_type in self.win_types:
            if self.gameboard[2][2][int(win_type[0]) - 1] == player and self.gameboard[1][1][int(win_type[1]) - 1] == player and self.gameboard[0][0][int(win_type[2]) - 1] == player:
                winDetected = True
            if self.gameboard[0][0][int(win_type[0]) - 1] == player and self.gameboard[1][1][int(win_type[1]) - 1] == player and self.gameboard[2][2][int(win_type[2]) - 1] == player:
                winDetected = True
        return winDetected

    #
    #
    # MAIN FUNCTIONS

    def get_game_state(self):
        self.game_state_string = ""
        for position in self.all_letter_name_positions:
            self.game_state_string += position
            self.game_state_string += self.gameboard[self.letterPositionLookUp(position)[1]][self.letterPositionLookUp(position)[0]]
        return self.game_state_string

    def reset(self, player_count_input):
        self.open_places = "A1A2A3B1B2B3C1C2C3D1D2D3E1E2E3F1F2F3G1G2GH1H2H3I1I2I3"  # Beginning open places to go
        self.all_letter_name_positions = "ABCDEFGHI"
        self.player_count = player_count_input
        self.remaining_pieces = []
        for player_piece_adder in range(self.player_count):
            self.remaining_pieces.append([3,3,3])
        self.game_state_string = ""
        self.board_len = 3
        self.gameboard = []
        self.game_winner = "0"
        for board_creation_length in range(self.board_len):
            self.gameboard.append(["000", "000", "000"])  # Call gameboard[x][y]

    def get_winner(self):
        integer_game_winner = 0
        for player in range(self.player_count):
            for spot in range(2):
                if self.checkHLineWin(spot, str(player)) or self.checkVLineWin(spot, str(player)):
                    integer_game_winner = player
            if self.checkDiagonalWin(str(player)) or self.checkSameWin(str(player)):
                integer_game_winner = player
        self.game_winner = str(integer_game_winner)
        return str(integer_game_winner)

    def place_ring(self, pos, ring, player):
        requested_x, requested_y = self.letterPositionLookUp(pos)
        placement_permitted = False
        if self.gameboard[requested_y][requested_x][int(ring) - 1] == "0" and self.remaining_pieces[int(player) - 1][int(ring) - 1] > 0:
            placement_permitted = True
        if placement_permitted:
            new_ring = int(ring)
            board_update = self.gameboard[requested_y][requested_x]
            #Place piece
            self.gameboard[requested_y][requested_x] = board_update[:(int(new_ring) - 1)] + player + board_update[(int(new_ring)):]
            #Subtract ring
            self.remaining_pieces[int(player) - 1][int(ring) - 1] -= 1
            #Remove from open places
            self.open_places = self.open_places.replace((str(pos) + str(ring)), "")


        return placement_permitted

    def recreate_gamestate(self, gamestate):
        gamestate = list(gamestate)
        iteration = 0
        while iteration < 9:
            alt_x = self.letterPositionLookUp(gamestate[0 + (iteration * 4)])[0]
            alt_y = self.letterPositionLookUp(gamestate[0 + (iteration * 4)])[1]
            self.gameboard[alt_y][alt_x] = gamestate[1 + (iteration * 4)] + gamestate[2 + (iteration * 4)] + gamestate[3 + (iteration * 4)]
            iteration += 1
        player_id = 1
        self.remaining_pieces = []
        for player_piece_adder in range(self.player_count):
            self.remaining_pieces.append([3, 3, 3])
        for player_recreate in self.remaining_pieces:
            iteration = 0
            while iteration < 9:
                if gamestate[1 + (iteration * 4)] == str(player_id):
                    player_recreate[0] -= 1
                if gamestate[2 + (iteration * 4)] == str(player_id):
                    player_recreate[1] -= 1
                if gamestate[3 + (iteration * 4)] == str(player_id):
                    player_recreate[2] -= 1
                iteration += 1
            player_id += 1

    def get_remaining_rings(self, pin_type, player):
        return self.remaining_pieces[int(player - 1)][int(pin_type - 1)]

    def render_ascii(self):
        board = self.get_game_state()
        print('************   otrio   ************')
        print('  by broskisworld and lordemperor  ')
        print('')
        print(' A | B | C ')
        print(f'{board[0:2]}|{board[4:6]}|{board[8:10]}')
        print('   |   |   ')
        print(' D | E | F ')
        print(f'{board[12:14]}|{board[16:18]}|{board[20:22]}')
        print('   |   |   ')
        print(' G | H | I ')
        print(f'{board[23:25]}|{board[26:28]}|{board[29:31]}')
        print('   |   |   ')