from typing import List

from racecar.race_car import RaceCar


class Track:

    def __init__(self) -> None:
        self.track: List[List[Enum]]
        self.track_name: str = ""
        self._str: str = ""
        pass

    def detect_collision(self, race_car: RaceCar) -> None:
        pass
