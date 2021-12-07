import operator
import random
from typing import Tuple, List, Dict

from track import CellType
from simulator import Simulator
from state import State
from race_car import RaceCar


class QLearner:

    def __init__(self) -> None:
        self.simulator: Simulator = Simulator()
        self.q: Dict[Tuple[State, Tuple[
            int, int]]] = {}  # make a dict of w/ key of Tuple(state, action), value: Reward. Implement the comparable and hashable methods to pass in State as an key
        self.gamma: float = 1
        self.previous_reward: int = 0
        pass

    def init_q(self) -> None:
        rows, columns = self.simulator.model.track.track.shape
        for x_position in range(columns):
            for y_position in range(rows):
                if self.simulator.model.track.track[y_position][x_position] is CellType.WALL:
                    continue
                for x_velocity in range(-5, 5):
                    for y_velocity in range(-5, 5):
                        for x_acceleration in [-1, 0, 1]:
                            for y_acceleration in [-1, 0, 1]:
                                self.q[(State(x_position, y_position, x_velocity, y_velocity),
                                        (x_acceleration, y_acceleration))] = 0
        # entries: int = 0
        # for key in self.q:
        #     print(f"key: {str(key[0]), key[1]} value: {self.q.get(key)}")
        #     entries += 1
        # print(entries)

    def q_learn(self, *, number_of_episodes: int = 10) -> None:
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
        self.init_q()
        for episode in range(number_of_episodes):
            if episode > 0:
                self.simulator.race_car = RaceCar(self.simulator.model.track.start_state())
            self.previous_reward: int = 0
            while self.simulator.race_car.state not in self.simulator.model.track.finish_states:
                a_x: int
                a_y: int
                a_x, a_y = self.boltzmann_distribution(self.simulator.race_car.state)

        pass

    def calculate_policy(self) -> None:
        pass

    def step_simulation(self) -> None:
        pass

    @staticmethod
    def q_sub_t(state: State, action: Tuple[int, int]) -> int:
        pass

    def boltzmann_distribution(self, state: State) -> Tuple[int, int]:

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
        # from https://www.programiz.com/python-programming/methods/built-in/max#:~:text=The%20max()%20function%20returns,between%20two%20or%20more%20parameters.
        max_key = max(state_action_dict, key=lambda k: state_action_dict[k])

        temperature: float = 1.0

        # [e^(Q-sub-t(s, a)/Temp)] / [sum over all actions (a') in action space (A): (e^(Q-sub-t(s, a'))/Temp)]

        return 0, 0

if __name__ == "__main__":
    q_learner: QLearner = QLearner()
    q_learner.q_learn()
    pass
