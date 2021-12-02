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

    def reward(self, state: Tuple[int, int]) -> float:
        pass
