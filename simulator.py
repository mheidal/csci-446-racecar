import random
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
        self.time += 1
        self.race_car.x = self.race_car.x + (self.race_car.v_x * 1) + (.5 * (self.race_car.a_x * 1 ** 2))
        self.race_car.y = self.race_car.y + (self.race_car.v_y * 1) + (.5 * (self.race_car.a_y * 1 ** 2))

    def act(self) -> None:
        pass


if __name__ == "__main__":
    sim: Simulator = Simulator()
    for i in range(0, 100):
        sim.time_step()
        sim.race_car.accelerate(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
    pass
