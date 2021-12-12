import math
import operator
import random
from typing import Tuple, List, Dict, Any
import turtle

from track import CellType
from simulator import Simulator
from state import State
from race_car import RaceCar


class QLearner:

    def __init__(self) -> None:
        self.simulator: Simulator = Simulator(activate_turtle=False)
        self.q: Dict[Tuple[State, Tuple[
            int, int]]] = {}  # make a dict of w/ key of Tuple(state, action), value: Reward. Implement the comparable and hashable methods to pass in State as an key
        self.gamma: float = 1
        self.previous_reward: int = 0
        pass

    def init_q(self) -> None:
        rows, columns = self.simulator.model.track.track.shape
        for x_position in range(columns):
            for y_position in range(rows):
                x = self.simulator.model.start_state.x_pos
                y = self.simulator.model.start_state.y_pos
                if self.simulator.model.track.track[y_position][x_position] == CellType.WALL:
                    continue
                for x_velocity in range(-5, 6):
                    for y_velocity in range(-5, 6):
                        for x_acceleration in [-1, 0, 1]:
                            for y_acceleration in [-1, 0, 1]:

                                self.q[(State(x_position, y_position, x_velocity, y_velocity),
                                        (x_acceleration, y_acceleration))] = -1
        return
        # entries: int = 0
        # for key in self.q:
        #     print(f"key: {str(key[0]), key[1]} value: {self.q.get(key)}")
        #     entries += 1
        # print(entries)

    def q_learn(self, *, number_of_episodes: int = 10000) -> None:
        # init all Q(s, a) arbitrarily
        # for all episodes do the following
        #   initialize s
        #   repeat
        #       choose a using policy derived from Q
        #       apply action a
        #       observe Reward(s, a) and successor state s'
        #       Q(s, a) <-- Q(s, a) + alpha( Reward(s, a)) + [gamma * max_a' * Q(s', a')] - Q(s, a) )
        #       Q(s,a) = prevQ(s,a) + alpha * [reward for moving to this state + gamma (discount factor) * largest Qval aval for any action in the current state (largest predicted sum of future rewards)]
        #               alpha is the learning rate defined by: (alpha-not * tau) / (tau + n-sub-t(s,a)) where tau is tunable between 0 and 1 and n-sub-t is the # of times a state action pair has been visited
        #               may need to make value of self.q a Tuple with (value, number or time visited) implements Boltzmann distribution
        #       s <-- s'
        #   until s is terminal state: if x,y is a finish state... detect_finish() from Track maybe?
        # end for loop

        # Additions:
        # Verify self.q is updating correctly (it's not)
        # Tune params
        # number of episodes should be equal to number or restarts from sim.
        #
        self.init_q()
        alphanums = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        # print(f"Start state is {self.simulator.model.start_state}")
        start_state_sets = self.simulator.model.track.progressive_start_states()
        start_state_subdivision_size = number_of_episodes / len(start_state_sets)
        self.simulator.model.record_length = int(start_state_subdivision_size)
        current_division = 0
        for episode in range(number_of_episodes):
            if episode+1 > start_state_subdivision_size * current_division:
                print(f"On episode {episode}, switching to division {alphanums[current_division+1]}")
                current_division += 1
            self.simulator.model.start_state = random.choice(start_state_sets[current_division-1])

            if episode >= number_of_episodes * (9900 / 10000) and self.simulator.model.track.t is None:
                self.simulator.model.track.t = turtle.Turtle()
                self.simulator.model.track.display_track_with_turtle()

            if episode > 0:
                self.simulator.race_car = RaceCar(self.simulator.model.start_state)
            self.previous_reward: int = 0
            current_state: State = self.simulator.race_car.state
            while current_state is not self.simulator.model.special_state:
                alpha: float = 1

                # choose a derived from Q
                a_x: int
                a_y: int
                accelerations: List[Tuple[int, int]] = []
                acceleration_probability_distribution: List[float] = []
                boltzmann: Tuple[List[Tuple[int, int]], List[float]] = self.boltzmann_distribution(self.simulator.race_car.state)
                accelerations = boltzmann[0]
                acceleration_probability_distribution = boltzmann[1]
                a_x, a_y = random.choices(accelerations, weights=acceleration_probability_distribution)[0]

                # apply action a
                self.simulator.act(a_x, a_y)

                # observe the state that occurred as a result s'
                new_state: State = self.simulator.race_car.state

                # observe the reward from taking action a in state s
                new_state_reward: int = self.simulator.model.reward(new_state)

                # update self.q([s, a])...
                if new_state != self.simulator.model.special_state:
                    self.q[(current_state, (a_x, a_y))] = self.q[(current_state, (a_x, a_y))] + (alpha * (
                            new_state_reward + (self.gamma * self.q[self.q_max(new_state)]) - self.q[(current_state, (a_x, a_y))]))
                else:
                    self.q[(current_state, (a_x, a_y))] = 0

                # set s <= s' and
                current_state = new_state
        pass

    def calculate_policy(self) -> None:
        pass

    def step_simulation(self) -> None:
        pass

    @staticmethod
    def q_sub_t(state: State, action: Tuple[int, int]) -> int:
        pass

    def boltzmann_distribution(self, state: State) -> Tuple[List[Tuple[int, int]], List[Any]]:
        # this should be the probability distributions for the possible actions at this state

        keys_list: List[Tuple[State, Tuple[int, int]]] = []
        for x_acceleration in [-1, 0, 1]:
            for y_acceleration in [-1, 0, 1]:
                keys_list.append((state, (x_acceleration, y_acceleration)))

        values_list: List[int] = []
        for key in keys_list:
            values_list.append(self.q.get(key))

        state_action_dict: dict = {}
        for key, value in zip(keys_list, values_list):
            state_action_dict[key] = value

        probability_distribution_a_given_s: Dict[Tuple[int, int]] = {}
        temperature: float = 1.0
        summation: float = 0

        for key in state_action_dict:
            value: float = (math.exp(self.q[key])/temperature)
            probability_distribution_a_given_s[key[1]] = value
            summation += value

        if summation == 0:
            for key in state_action_dict:
                probability_distribution_a_given_s[key[1]] = 1/9
        else:
            for key in state_action_dict:
                probability_distribution_a_given_s[key[1]] = probability_distribution_a_given_s[key[1]] / summation

        # [e^(Q-sub-t(s, a)/Temp)] / [sum over all actions (a') in action space (A): (e^(Q-sub-t(s, a'))/Temp)]

        return list(probability_distribution_a_given_s), list(probability_distribution_a_given_s.values())  # boltzman distrib should replace this

    def q_max(self, state: State) -> Tuple[State, Tuple[int, int]]:
        keys_list: List[Tuple[State, Tuple[int, int]]] = []
        for x_acceleration in [-1, 0, 1]:
            for y_acceleration in [-1, 0, 1]:
                keys_list.append((state, (x_acceleration, y_acceleration)))

        values_list: List[int] = []
        for key in keys_list:
            values_list.append(self.q.get(key))

        state_action_dict: dict = {}
        for key, value in zip(keys_list, values_list):
            state_action_dict[key] = value
        if values_list[0] is None:
            pass
        # from https://www.programiz.com/python-programming/methods/built-in/max#:~:text=The%20max()%20function%20returns,between%20two%20or%20more%20parameters.
        return max(state_action_dict, key=lambda k: state_action_dict[k])


if __name__ == "__main__":
    q_learner: QLearner = QLearner()
    q_learner.q_learn()
    pass
