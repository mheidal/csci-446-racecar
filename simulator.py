import random
from typing import Tuple

from race_car import RaceCar
from track import Track, CellType
from model import Model
from state import State
from race_car import RaceCar
from track import Track


class Simulator:

    def __init__(self) -> None:
        self.model: Model = Model(Track())
        self._str = ""
        start_state: State = self.model.track.start_state()
        self.race_car: RaceCar = RaceCar(start_state)
        self.time: int = 0

    def time_step(self) -> None:
        self.time += 1

        # approx. of kinematics for position update
        self.race_car.x = self.race_car.v_x + self.race_car.x
        self.race_car.y = self.race_car.v_y + self.race_car.y

    def act(self) -> None:
        self.race_car.accelerate(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

    def manual_control(self) -> None:
        print(self.model.track.detect_finish(self.race_car.state))
        while(self.model.track.detect_finish(self.race_car.state) == False):
            direction = input("")
            # if you press a
            if (direction == 'a'):
                self.race_car.state = self.model.transition(self.race_car.state, 0, -1)
            # if you press d
            if (direction == 'd'):
                self.race_car.state = self.model.transition(self.race_car.state, 0, 1)
            # if you press w
            if (direction == 'w'):
                self.race_car.state = self.model.transition(self.race_car.state, 1, 0)
            # if you press s
            if (direction == 's'):
                self.race_car.state = self.model.transition(self.race_car.state, -1, 0)
            print(self.__str__())

    def __str__(self):
        #if self._str == "":
        string = ""
        for y, row in enumerate(self.model.track.track):
            for x, cell in enumerate(row):
                if self.race_car.state.x_pos == x and self.race_car.state.y_pos == y:
                    string += "X"
                elif cell == CellType.WALL:
                    string += "#"
                elif cell == CellType.START:
                    string += "S"
                elif cell == CellType.FINISH:
                    string += "F"
                else:
                    string += "."
                string += " "
            string += "\n"
            self._str = string
        return self._str

if __name__ == "__main__":
    sim: Simulator = Simulator()
    print(sim.race_car)
    for i in range(0, 100):
        sim.time_step()
        sim.act()
    pass
