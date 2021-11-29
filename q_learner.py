from typing import Tuple, List, Dict

from race_car.simulator import Simulator


class QLearner:

    def __init__(self) -> None:
        self.simulator: Simulator = Simulator()
        self.q: List[Dict[Tuple[int, int], int]] = []
        pass

    def init_q(self) -> None:
        # we may just want to use the __init__() for this
        pass

    def q_learn(self) -> None:
        pass

    def calculate_policy(self) -> None:
        pass

    def step_simulation(self) -> None:
        pass
