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
        self.state_action_dict:  Dict[Tuple[int, int, int, int, Tuple[int, int]], float] = {}
        self.poop = 0

    def init_actions(self):
        for x_acceleration in [-1, 0, 1]:
            for y_acceleration in [-1, 0, 1]:
                self.actions.append((x_acceleration, y_acceleration))

    def init_value_iteration(self):
        # initalize non goal states to -1, the goal staes to 1

        self.init_actions()
        rows, columns = self.simulator.model.track.track.shape
        #print( self.simulator.model.track)
        #self.reward_dictionary = np.empty(rows, columns)
        for x_position in range(columns-1):
            self.poop += 1
            print(self.poop)
            for y_position in range(rows-1):
                self.poop += 1
                print(self.poop)
                for x_velocity in range(-5, 6):
                    self.poop += 1
                    print(self.poop)
                    for y_velocity in range(-5, 6):
                        self.poop += 1
                        print(self.poop)
                        #print(y_position, x_position)
                        # if self.simulator.model.track.track[y_position][x_position] == CellType.WALL:
                        #     pass
                            #self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = -10
                        if self.simulator.model.track.track[y_position][x_position] == CellType.FINISH:
                            self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = 0
                            print('if')
                        else:
                            self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = -1
                            print('else')

        # for x_position in range(columns-1):
        #     for y_position in range(rows-1):
        #         for x_velocity in range(-5, 6):
        #             for y_velocity in range(-5 , 6):
        #                 for a in self.actions:
        #                     if self.simulator.model.track.track[y_position][x_position] == CellType.WALL:
        #                         self.state_action_dict[(x_position, y_position, x_velocity, y_velocity, a)] = -10
        #                     elif self.simulator.model.track.track[y_position][x_position] == CellType.FINISH:
        #                         self.state_action_dict[(x_position, y_position, x_velocity, y_velocity, a)] = 0
        #                     else:
        #                         self.state_action_dict[(x_position, y_position, x_velocity, y_velocity, a)] = -1


        #for state in self.model.state_space:

    def value_iteration(self):
        # self.init_value_iteration()
        # values = self.reward_dictionary
        # s_a = self.state_action_dict

        self.init_actions()
        # iterate through array
        # use bellman equation
        # for each state calculate Q(s, a)
        # first pass initalized goal states, and negative states
        # second pass initialize state next to goal states

        training_iterations = 1
        gamma = 1
        for train in range(training_iterations):
            self.poop += 1
            #print("new", self.poop)
            #old_v = deepcopy(values)
            # Q(s,a) = max ( R(s,a) + gamma sum s' T(s,a,s') Vt-1(s') )
            for state in self.model.track_state_space.values():
                self.poop += 1
                #print("new", self.poop)
                q_value = []
                for action in self.actions:
                    self.poop +=1
                    #print("new", self.poop)
                    if(self.poop % 10000 == 0):
                        print("new", self.poop)
                    # sum_of_T_V = 0
                    all_s_primes = self.model.get_transitions_and_probabilities(state, action[0], action[1])
                    # # get R(s,a)
                    # reward_of_sa = self.model.reward(state)
                    # # get all s'
                    for s_prime in all_s_primes:
                        self.poop += 1
                        #print("new", self.poop)
                        # # get V(s')
                        # s_prime_state = s_prime[1]
                        #
                        # value_of_s_prime = old_v.get((s_prime_state.x_pos, s_prime_state.y_pos, s_prime_state.x_vel,
                        #                               s_prime_state.y_vel))
                        # # get T(s,a,s'), probability that s, a, s' happens
                        # probability_of_transition = s_prime[0]
                        # # T(s,a,s') * V(s')
                    #   if (self.simulator.model.track.track[s_prime_state.y_pos][s_prime_state.x_pos] == CellType.WALL):
                    #         value_of_s_prime = -10
                    #
                    #     sum_of_T_V= value_of_s_prime * probability_of_transition + sum_of_T_V
                    # expected_reward =  reward_of_sa + (gamma*sum_of_T_V)
                    #values[(state.x_pos, state.y_pos, state.x_vel, state.y_vel)] = expected_reward
                #     q_value.append(expected_reward)
                #
                # values[(state.x_pos, state.y_pos, state.x_vel, state.y_vel)] = max(q_value)
        return self.poop
                #get max action
                #argMax = np.argmax(s_a[(state.x_pos, state.y_pos, state.x_vel, state.y_ve)])





                #dicounted_future_reward =



                # self.model.reward(state)
                # gammaV*(s')









    def execute_policy(self) -> None:
        pass

    def update_q(self) -> Dict[Tuple[int, int], int]:
        pass





