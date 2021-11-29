from typing import Tuple

from racecar.race_car import RaceCar
from racecar.track import Track


class Simulator:

    def __init__(self) -> None:
        self.track: Track = Track()
        start_state: Tuple[int, int] = self.track.start_state()
        self.race_car: RaceCar = RaceCar(start_state[0], start_state[1])
        self.time: int = 0

    def time_step(self) -> None:
        pass

    def act(self) -> None:
        pass
