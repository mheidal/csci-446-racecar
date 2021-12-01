import random
from typing import Tuple

from model import Model
from race_car import RaceCar
from track import Track


class Simulator:

    def __init__(self) -> None:
        self.model: Model = Model(Track())
        start_state: Tuple[int, int] = self.model.track.start_state()
        self.race_car: RaceCar = RaceCar(start_state[0], start_state[1])
        self.time: int = 0

    def time_step(self) -> None:
        self.time += 1

        # approx. of kinematics for position update
        self.race_car.x = self.race_car.v_x + self.race_car.x
        self.race_car.y = self.race_car.v_y + self.race_car.y

    def act(self) -> None:
        self.race_car.accelerate(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))


if __name__ == "__main__":
    sim: Simulator = Simulator()
    print(sim.race_car)
    for i in range(0, 100):
        sim.time_step()
        sim.act()
    pass
