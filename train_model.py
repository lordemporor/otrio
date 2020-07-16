#!/usr/bin/python3
import gym
import numpy as np
import scipy
from scipy.sparse import coo_matrix
from scipy.sparse import csc_matrix
from big_sparse_matrix import BigSparseMatrix
import random
from os import system

import gym_otrio
import otriogameboard

# config training vars
# confidence in new training - smaller values will increase confidence in previous training
ALPHA = 0.1
# additional reward for choosing states with good next state-action values (coefficient * next_max)
GAMMA = 0.6
# exploration weighting - higher values prefer learning new q-table state-action values than improving previous q-table
EPSILON = 0.1
MAX_EPISODE_TICKS = 100000
BOARD_STATES_LEN = 5**27
NUM_OF_ACTIONS = 27

# plotting metrics
all_events = []

# init environment and model
env = gym.make('otrio-v0')
q_table = BigSparseMatrix(BOARD_STATES_LEN, NUM_OF_ACTIONS)
render_every_step = False
pause_every_step = False

def zero_model():
    global q_table

    q_table = BigSparseMatrix(BOARD_STATES_LEN, NUM_OF_ACTIONS)


def train_model(episode_count):
    global q_table

    for episode in range(episode_count):
        reward = 0
        cur_game = otriogameboard.game(2)

        observation = env.reset(cur_game, '1')
        print('initial observation: ' + str(observation))

        tick = 0
        done = False
        while not done and tick < MAX_EPISODE_TICKS:

            # alternate between improving model and utilizing model
            if random.uniform(0, 1) < EPSILON:
                # explore new actions
                action = env.action_space.sample()
                #print(f'AI action [random]       (0-26): {action}')
            else:
                # use known q-table vals
                action = np.argmax(q_table[observation])
                #print(f'AI action [from q-table] (0-26): {action}')

            # perform AI step
            prev_state = observation
            observation, reward, done, info = env.step(action)

            #print(f'obs: {observation}, action: {action}')
            prev_state_action_val = q_table[observation, action]  # prev action preference

            # calculate adjusted q table
            next_max = np.max(q_table[observation])  # based on current confidence level?
            # balance % of old q-table to keep with % of just learned knowledge
            new_state_action_val = \
                ((1 - ALPHA) * prev_state_action_val) + \
                (ALPHA * (reward + (GAMMA * next_max)))
            q_table[observation, action] = new_state_action_val # TODO: element by element access is inefficient - use lil format or matrix x matrix op


            # reset for next calculation
            prev_state = observation

            #print(f'AI post-action observation: {observation}')

            if done:
                print('AI wins!')
                breakpoint()
                break

            # player 2
            random_action = gen_random_move(cur_game)
            #print(f'opponent action: {random_action}')
            cur_game.place_ring(random_action[0], random_action[1], '2')

            # TODO: add training for other players (also choose random first player)

            if render_every_step:
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                cur_game.render_ascii()

            if pause_every_step:
                input('press enter for next step...')

            tick += 1
            all_events.append(0)    # TODO: event types for metrics (bad move, lose, etc)

        # end of episode
        print(f'episode #{episode} finished after {tick} ticks!')

    # end of training
    print(f'end of training! total ticks: {len(all_events)}')


def gen_random_move(game):
    #print(f'open places: {game.open_places}')
    move_choice = random.randrange(0, len(game.open_places) - 1, 2)
    return game.open_places[move_choice:move_choice + 2]


# utils
def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


# interactive menu
quit_menu = False
print('************   otrio   ************')
print('  by broskisworld and lordemperor  ')
print('***********************************')
print('')
print('if needed, type help or ?')
while not quit_menu:
    usr_choice = ''
    usr_choice = input('otrio model trainer> ')

    if usr_choice == 'zero-q':
        zero_model()
    elif usr_choice[:5] == 'train':
        # TODO: more training vars (train from file, configure alpha, gamma, and epsilon vars, configure num of players, starting player, etc.)
        if is_int(usr_choice[6:]):
            train_model(int(usr_choice[6:]))
        else:
            print('usage: train [n episodes]')
    elif usr_choice[:6] == 'render':
        if usr_choice[7:] == 'on':
            render_every_step = True
            pause_every_step = False
        elif usr_choice[7:] == 'onkey':
            render_every_step = True
            pause_every_step = False
        elif usr_choice[7:] == 'off':
            render_every_step = False
            pause_every_step = False
        else:
            print('usage: render [on/onkey/off]')
    elif usr_choice == 'view':
        env.render()
    elif usr_choice == 'quit':
        print('bye!')
        quit_menu = True
    elif usr_choice == 'help' or usr_choice == '?':
        print('commands: zero-q, train [n episodes], render [on/onkey/off], view, quit, help, ?')
    else:
        print('invalid command. type help or ? to view options')

env.close()