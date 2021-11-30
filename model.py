from typing import List, Dict, Tuple

from simulator import Simulator
from track import Track


class Model:

    def __init__(self, track: Track) -> None:
        self.discount_factor_gamma: float
        self.bellman_error_epsilon: float
        self.track = track
        self.state_space = self.initialize_state_space()
        # self.action_space:

    def initialize_state_space(self):
        pass

    def transition(self, initial_state: Tuple[int, int], action: int) -> Tuple[int, int]:
        pass

    def reward(self, state: Tuple[int, int]) -> float:
        pass
