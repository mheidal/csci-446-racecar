import turtle
from typing import Tuple

from race_car import RaceCar
from track import Track, CellType
from model import Model, CrashType
from model import Model
from state import State
from race_car import RaceCar
from track import Track
from enums import CellType


class Simulator:

    def __init__(self, *, activate_turtle: bool = False, track: str = "L-track",
                 crash_type_restart: bool = True) -> None:
        self.model: Model = Model(Track(track_file=track), crash_type=(
            CrashType.RESTART if crash_type_restart else CrashType.STOP)) if not activate_turtle else Model(
            Track(track_file=track, turt=turtle.Turtle()),
            crash_type=(CrashType.RESTART if crash_type_restart else CrashType.STOP))
        self._str = ""
        start_state: State = self.model.track.start_state()
        self.race_car: RaceCar = RaceCar(start_state)
        self.time: int = 0

    def act(self, a_x: int, a_y: int) -> None:
        """
        Calls the transition function in this simulators model
        :param a_x: new acceleration for the racecar in the x direction
        :param a_y: new accleration for the racecar in the y direction
        :return: None.
        """
        self.race_car.state = self.model.transition(self.race_car.state, a_x, a_y)
        self.time += 1

    def __str__(self):
        # if self._str == "":
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
