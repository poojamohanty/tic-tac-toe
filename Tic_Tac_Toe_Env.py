# from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product


class TicTacToe():
    def __init__(self):
        """initialise the board"""

        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)]  # , can initialise to an array or matrix

        self.reset()
    def reset(self):
        return self.state

    def is_winning(self, curr_state):
        possible_pos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for position in possible_pos:
            if not np.isnan(curr_state[position[0]]) and not np.isnan(curr_state[position[1]]) and not np.isnan(
                    curr_state[position[2]]):
                curr_state_val = curr_state[position[0]] + curr_state[position[1]] + curr_state[position[2]]
                if curr_state_val == 15:
                    return True
        return False

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) == 0:
            return True, 'Tie'

        else:
            return False, 'Resume'

    def allowed_positions(self, curr_state):

        return [i for i, val in enumerate(curr_state) if np.isnan(val)]

    def allowed_values(self, curr_state):

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 != 0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 == 0]

        return (agent_values, env_values)

    def action_space(self, curr_state):

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)

    def state_transition(self, curr_state, curr_action):

        curr_state[curr_action[0]] = curr_action[1]
        return curr_state

    def step(self, curr_state, curr_action):
        win_state = False
        next_state = self.state_transition(curr_state, curr_action)
        win_state, game_status = self.is_terminal(next_state)
        if win_state == True:
            if game_status == 'Win':
                reward = 10
            else:
                reward = 0
        else:
            next_position = random.choice(self.allowed_positions(next_state))
            next_value = random.choice(self.allowed_values(next_state)[1])
            next_state[next_position] = next_value
            win_state, game_status = self.is_terminal(next_state)
            if win_state == True:
                if game_status == 'Win':
                    reward = -10
                else:
                    reward = 0
            else:
                reward = -1
        return next_state, reward, win_state