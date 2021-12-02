import random
from typing import Tuple

# from racecar.race_car import RaceCar
# from racecar.track import Track
from race_car import RaceCar
from track import Track


class Simulator:

    def __init__(self) -> None:
        self.track: Track = Track()
        start_state: Tuple[int, int] = self.track.start_state()
        self.race_car: RaceCar = RaceCar(start_state[0], start_state[1])
        self.time: int = 0

    def time_step(self) -> None:
        self.time += 1

        # approx. of kinematics for position update
        self.race_car.x = self.race_car.v_x + self.race_car.x
        self.race_car.y = self.race_car.v_y + self.race_car.y

    def act(self) -> None:
        self.race_car.accelerate(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

    def manual_control(self) -> None:
        print(self.track.detect_finish(self.race_car))
        while(self.track.detect_finish(self.race_car) == False):
            print("hello")
            direction = input("")
            # if you press a
            if (direction == 'a'):
                self.race_car.accelerate(0, -1)
            # if you press d
            if (direction == 'd'):
                self.race_car.accelerate(0, 1)
            # if you press w
            if (direction == 'w'):
                self.race_car.accelerate(1, 0)
            # if you press s
            if (direction == 's'):
                self.race_car.accelerate(-1, 0)

if __name__ == "__main__":
    sim: Simulator = Simulator()
    print(sim.race_car)
    for i in range(0, 100):
        sim.time_step()
        sim.act()
    pass




