from typing import List, Dict, Tuple

from racecar.simulator import Simulator


class Model:

    def __init__(self) -> None:
        self.discount_factor_gamma: float
        self.bellman_error_epsilon: float
        # self.state_space:
        # self.action_space:

    def transition(self, initial_state: Tuple[int, int], action: int) -> Tuple[int, int]:
        pass

    def reward(self, state: Tuple[int, int]) -> float:
        pass
