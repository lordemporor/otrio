import gym
from gym import error, spaces, utils
from gym.utils import seeding
from baseconvert import base

# game constants
GAMEBOARD_LOCATION = ['ADG', 'BEH', 'CFI']
GAMEBOARD_LOCATION_CHARS = 'ABCDEFGHI'
OBSERVATION_SPACE_DISCRETE_SIZE = 5**27 * 4**3  # 27 ring place locations, 5 possible player vals (4 and the 0-player), and an inventory of 3 ring types quantities 0-3
ACTION_SPACE_DISCRETE_SIZE = 27  # 9 board spots, 3 ring place locations each

# rewards constants
REWARD_MAX = 50

class OtrioEnv(gym.Env):
    """An OpenAI Gym Env class implementation of lordemporor's digital Otrio game"""

    def __init__(self):
        super(OtrioEnv, self).__init__()

        # define action and observation space as gym.spaces objects
        self.action_space = spaces.Discrete(ACTION_SPACE_DISCRETE_SIZE)
        self.observation_space = spaces.Discrete(OBSERVATION_SPACE_DISCRETE_SIZE)

        # gym vars
        metadata = {'render.modes': ['human']}
        reward_range = (0, REWARD_MAX)

        self.current_step = 0
        self.cur_game = None
        self.game_id = '0'
        self.done = False

    def step(self, action):
        # living is pain. punish them every moment so they try and end it as fast as possible
        reward = -1

        # action as discrete number
        location, ring = self.place_discrete_action(action)

        # check if ai lost during non-ai action
        if self.cur_game.get_winner() != 0:
            reward = -30

            if not self.cur_game.place_ring(location, ring, self.game_id):
                # ai being a big dumb
                reward = -5

            winner = self.cur_game.get_winner()
            if winner != '0':
                if winner == self.game_id:
                    reward = 30
                else:
                    reward = -30

        self.observation_space = self.get_discrete_game_state()

        self.current_step += 1

        return self.observation_space, reward, self.done, None

    def reset(self, cur_game, game_id):
        # reset game
        self.cur_game = cur_game
        self.game_id = game_id

        return self.get_discrete_game_state()

    def render(self, mode='human', close=False):
        self.cur_game.render_ascii()

    # utility functions
    def place_discrete_action(self, discrete_action):
        action_int = int(discrete_action)
        row = int(action_int / 9)
        col = int((action_int - (row * 9)) / 3)
        ring = int(action_int - ((row * 9) + (col * 3))) + 1 # add 1 bc so that state 0-2 means something

        #print(f'discrete action #{action_int} -> place @{GAMEBOARD_LOCATION[col][row]}{str(ring)}')

        self.cur_game.place_ring(GAMEBOARD_LOCATION[col][row], str(ring), self.game_id)

        return GAMEBOARD_LOCATION[col][row], str(ring)

    def get_discrete_game_state(self):
        # converts game state string to base-5 number 27 digits long, then into a discrete base-10 state, multiplied by the ring state
        gameboard_str = self.cur_game.get_game_state()

        #print(f'gameboard state: {gameboard_str}')
        for char in GAMEBOARD_LOCATION_CHARS:
            gameboard_str = gameboard_str.replace(char, '')

        #print(f'base 5 gameboard state: {gameboard_str}')
        base5_board_state = int(gameboard_str)
        base10_board_state = int(base(base5_board_state, 5, 10, string=True))

        return base10_board_state

        # converts the remaining rings list into a 3-digit base-4 number (i.e. 213, 333, 000, etc.)
        # base-4 number is converted to a base-10 discrete state
        remaining_pins = self.cur_game.get_remaining_rings('1', self.game_id)
        remaining_small_rings = self.cur_game.get_remaining_rings('2', self.game_id)
        remaining_large_rings = self.cur_game.get_remaining_rings('3', self.game_id)
        base4_ring_state = int(str(remaining_pins) + str(remaining_small_rings) + str(remaining_large_rings))
        base10_ring_state = int(base(base4_ring_state, 4, 10, string=True))

        return base10_board_state * base10_ring_state