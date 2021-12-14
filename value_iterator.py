from copy import deepcopy

from track import Track
from track import CellType, Track
from typing import Dict, Tuple, List
from model import Model
from simulator import Simulator
from state import State
import turtle
from enums import CellType

class ValueIterator:
    def __init__(self, track_file: str, epsilon, gamma) -> None:
        # initializes variables, classes, and tables i need
        #self.simulator: Simulator = Simulator()
        self.model: Model = Model(Track(track_file=track_file))
        self.reward_dictionary: Dict[Tuple[int, int, int, int], float] = {}
        self.actions: List[Tuple[int, int]] = []
        self.state_action_dict:  Dict[Tuple[int, int, int, int, Tuple[int, int]], float] = {}
        self.transition_dict: Dict[Tuple[int, int, int, int, Tuple[int, int]],
                                   List[Tuple[float, State]]] = {}
        self.policy: Dict[Tuple[int, int, int, int], Tuple[int, int]] = {}
        self.delta = 100
        self.gamma = gamma
        self.epsilon = epsilon
        self.iterations: 0

    def init_actions(self):
        """
        initializes all the possible actions
        :return:
        """
        for x_acceleration in [-1, 0, 1]:
            for y_acceleration in [-1, 0, 1]:
                self.actions.append((x_acceleration, y_acceleration))

    def init_value_iteration(self):
        """
        initalize non goal states to -1, and the goal staes to 0 in the value table
        :return:
        """
        self.init_actions()
        rows, columns = self.model.track.track.shape
        for x_position in range(columns-1):
            for y_position in range(rows-1):
                for x_velocity in range(-5, 6):
                    for y_velocity in range(-5, 6):
                        if self.model.track.track[y_position][x_position] == CellType.FINISH:
                            self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = 0
                        else:
                            self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = -1

    def init_policy_extraction(self):
        """
        inits the state_action_dict,
        which is a dict that has state action pairs for keys and the reward for the value
        :return:
        """
        rows, columns = self.model.track.track.shape
        for x_position in range(columns - 1):
            for y_position in range(rows - 1):
                for x_velocity in range(-5, 6):
                    for y_velocity in range(-5, 6):
                        for action in self.actions:
                            # print(y_position, x_position)
                            if self.model.track.track[y_position][x_position] == CellType.WALL:
                                pass
                                # self.reward_dictionary[(x_position, y_position, x_velocity, y_velocity)] = -10
                            elif self.model.track.track[y_position][x_position] == CellType.FINISH:
                                self.state_action_dict[(x_position, y_position, x_velocity, y_velocity, action)] = 0
                                # self.poop+=1
                            else:
                                self.state_action_dict[(x_position, y_position, x_velocity, y_velocity, action)] = -1
                                # self.poop += 1

    def value_iteration(self):
        """
        Use the Bellman equation
        ( Q(s,a) = max ( R(s,a) + (gamma) sum_s' T(s,a,s') Vt-1(s') )
        to find an expected reward for each state and the most optimal action.
        :return policy:
        """
        # initializes all the variables i need
        self.init_value_iteration()
        values = self.reward_dictionary
        trans_dict = self.model.transition_map
        self.init_policy_extraction()
        s_a = self.state_action_dict
        old_v = deepcopy(values)
        self.iterations = 0

        # loop to run value iteration
        while(self.delta > self.epsilon):

            # keeps track of iterations
            self.iterations += 1
            print(self.iterations)

            # variable to be used to refrence the old value table
            old_v = deepcopy(values)

            # loops through all possible states
            max_dif = []
            for state in self.model.track_state_space.values():

                #if statment to account for starting in a finished state
                if self.model.track.track[state.y_pos][state.x_pos] == CellType.FINISH:
                    continue

                #sets a q_value list add and pull the max value from
                q_value = []
                q_value_actions = []

                # loops through all possible actions
                for action in self.actions:

                    # varibale for suming in the bellman equation
                    sum_of_T_V = 0

                    # get all possible states you could end up in from your current state taking action

                    all_s_primes = trans_dict.get((state, action[0], action[1]))

                    # get R(s,a)
                    reward_of_sa = self.model.reward(state)

                    # loop through all s'
                    for s_prime in all_s_primes:

                        # gets the actual state
                        s_prime_state = s_prime[1]

                        # get V(s')
                        value_of_s_prime = old_v.get((s_prime_state.x_pos, s_prime_state.y_pos, s_prime_state.x_vel,
                                                      s_prime_state.y_vel))

                        # get T(s,a,s'), probability that s, a, s' happens
                        probability_of_transition = s_prime[0]

                        # if statment to debug special state problem
                        if (self.model.track.track[s_prime_state.y_pos][s_prime_state.x_pos] == CellType.WALL
                                and not (s_prime_state.y_pos == -1 or s_prime_state.x_pos == -1)):
                             self.model.track.t = turtle.Turtle()
                             self.model.track.display_track_with_turtle()
                             self.model.transition(state, action[0], action[1])
                             value_of_s_prime = -10
                        elif (s_prime_state.y_pos == -1 or s_prime_state.x_pos == -1):
                            value_of_s_prime = 0


                        # sums all of V(s') * T(s,a,s')
                        sum_of_T_V = value_of_s_prime * probability_of_transition + sum_of_T_V

                    # gets total expected reward, this is the bellman equation
                    expected_reward = reward_of_sa + (self.gamma * sum_of_T_V)

                    # updates the state action table
                    s_a[(state.x_pos, state.y_pos, state.x_vel, state.y_vel, action)] = expected_reward

                    # appends expected reward for an action to q_value and append the action to q_value_actions
                    q_value.append(expected_reward)
                    q_value_actions.append(action)

                #gets the max value from q_value list and gets the index so we can refrence it in
                # the q_value_actions list
                max_val = max(q_value)
                max_index = q_value.index(max_val)

                #updates values with the highest expected reward in a state
                values[(state.x_pos, state.y_pos, state.x_vel, state.y_vel)] =  \
                    s_a[(state.x_pos, state.y_pos, state.x_vel, state.y_vel, q_value_actions[max_index])]

                # other way to update values with the highest expected reward in a state
                # values[(state.x_pos, state.y_pos, state.x_vel, state.y_vel)] = max(q_value)

                #get policy
                self.policy[(state.x_pos, state.y_pos, state.x_vel, state.y_vel)] = q_value_actions[max_index]

                # compute maximum diffrence
                # #for state in self.model.track_state_space.values():
                old_v_value = old_v.get((state.x_pos, state.y_pos, state.x_vel,
                          state.y_vel))

                values_value = values.get((state.x_pos, state.y_pos, state.x_vel,
                          state.y_vel))

                max_dif.append(abs(abs(values_value) - abs(old_v_value)))

            self.delta = max(max_dif)

        return self.policy





