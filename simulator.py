from racecar.race_car import RaceCar
from racecar.track import Track


class Simulator:

    def __init__(self) -> None:
        self.race_car: RaceCar = RaceCar()
        self.track: Track = Track()
        self.time: int = 0
        pass

    def time_step(self) -> None:
        pass

    def act(self) -> None:
        pass
