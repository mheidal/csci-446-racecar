from typing import Dict, Tuple, List

from racecar.model import Model
from racecar.simulator import Simulator


class ValueIterator:

    def __init__(self) -> None:
        self.q: List[Dict[Tuple[int, int], int]]
        self.v: List[Tuple[Tuple[int, int], int]]
        self.policy: List[Tuple[Tuple[int, int], int]]
        self.simulator: Simulator = Simulator()
        self.model: Model = Model()

    def value_iteration(self) -> None:
        pass

    def execute_policy(self) -> None:
        pass

    def update_q(self) -> Dict[Tuple[int, int], int]:
        pass
