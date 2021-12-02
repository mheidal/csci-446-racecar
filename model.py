from typing import List, Dict, Tuple

from track import Track
from state import State

class Model:

    def __init__(self, track: Track) -> None:
        self.discount_factor_gamma: float
        self.bellman_error_epsilon: float
        self.track = track
        self.state_space = self.initialize_state_space()
        # self.action_space:

    def initialize_state_space(self):
        possible_velocities = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        state_space: Dict[Tuple[int, int, int, int], State] = {}
        for y, row in enumerate(self.track.track):
            for x, cell in enumerate(row):
                for i in possible_velocities:
                    for j in possible_velocities:
                        state_space[(x, y, i, j)] = State(x, y, i, j)
        return state_space

    def transition(self, initial_state: State, x_a: int, y_a: int) -> Tuple[int, int]:
        pass

        # max_positive_acceleration: int = 1
        # max_positive_velocity: int = 5
        #
        # # constrain to be in +/-1
        # self.a_x = self.a_x if self.a_x <= max_positive_acceleration else max_positive_acceleration
        # self.a_x = self.a_x if self.a_x >= -max_positive_acceleration else -max_positive_acceleration
        #
        # self.a_y = self.a_y if self.a_y <= max_positive_acceleration else max_positive_acceleration
        # self.a_y = self.a_y if self.a_y >= -max_positive_acceleration else -max_positive_acceleration
        #
        # # approx. of kinematics for velocity
        # self.v_x = self.a_x + self.v_x
        # self.v_y = self.a_y + self.v_y
        #
        # # constrain vel. to be in +/-5
        # self.v_x = self.v_x if self.v_x <= max_positive_velocity else max_positive_velocity
        # self.v_x = self.v_x if self.v_x >= -max_positive_velocity else -max_positive_velocity
        #
        # self.v_y = self.v_y if self.v_y <= max_positive_velocity else max_positive_velocity
        # self.v_y = self.v_y if self.v_y >= -max_positive_velocity else -max_positive_velocity

    def reward(self, state: State) -> float:
        pass
