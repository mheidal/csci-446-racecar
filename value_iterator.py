from copy import deepcopy

from track import CellType, Track
from typing import Dict, Tuple, List
import numpy as np
from model import Model
from simulator import Simulator


class ValueIterator:

    def __init__(self) -> None:
        self.q: List[Dict[Tuple[int, int], int]]
        self.v: List[Tuple[Tuple[int, int], int]]
        self.policy: List[Tuple[Tuple[int, int], int]]
        self.simulator: Simulator = Simulator()
        self.model: Model = Model(Track())
        self.reward_dictionary: Dict[Tuple[int, int, int, int], float] = {}
        self.actions: List[Tuple[int, int]] = []


    def init_value_iteration(self):
        # initalize non goal states to -1, the goal staes to 1 and all wall states to -10

        rows, columns = self.simulator.model.track.track.shape
        #print( self.simulator.model.track)
        #self.reward_dictionary = np.empty(rows, columns)
        for x_position in range(columns):
            for y_position in range(rows):
                for x_velocity in range(-5, 5):
                    for y_velocity in range(-5 , 5):
                        #print(y_position, x_position)
                        if self.simulator.model.track.track[y_position][x_position] == CellType.WALL:
                            self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = -10
                        elif self.simulator.model.track.track[y_position][x_position] == CellType.FINISH:
                            self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = 0
                        else:
                            self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = -1

        #for state in self.model.state_space:

    def init_actions(self):
        for x_acceleration in [-1, 0, 1]:
            for y_acceleration in [-1, 0, 1]:
                self.actions.append((x_acceleration, y_acceleration))

    def extraxt_all_s_primes(self):

        pass

    def value_iteration(self) -> None:
        self.init_value_iteration()
        values = self.reward_dictionary
        self.init_actions()
        # iterate through array
        # use bellman equation
        # for each state calculate Q(s, a)
        # first pass initalized goal states, and negative states
        # second pass initialize state next to goal states

        training_iterations = 10
        gamma = 1
        old_v = deepcopy(values)

        for state in self.model.state_space:
            expected_reward = []
            for action in self.actions:
            # Q(s,a) = max ( R(s,a) + gamma sum s' T(s,a,s') Vt-1(s') )

            # get R(s,a)
                reward_of_sa = self.model.reward(state)
            # get all possible s'
                s_prime = self.model.transition(state, action[0], action[1])
            # get  all V(s')
                value_of_s_prime = self.model.reward(s_prime)
            # get T(s,a,s'), probability that s, a, s' happens
                # TODO
            # Q(s,a)
                expected_reward = 0



                #dicounted_future_reward =



                # self.model.reward(state)
                # gammaV*(s')

        for train in range(training_iterations):







    def execute_policy(self) -> None:
        pass

    def update_q(self) -> Dict[Tuple[int, int], int]:
        pass





