import random
from typing import List, Tuple
from enum import IntEnum
import numpy as np
from racecar.race_car import RaceCar


class CellType(IntEnum):
    WALL = 0
    START = 1
    FINISH = 2
    TRACK = 3


class Track:

    def __init__(self, track_file: str = None):
        if track_file is None:
            self.parse_file("L-track.txt")
        else:
            self.parse_file(track_file)
        self._str: str = ""
        self.track_name: str = track_file.split(".")[0]
        self.start_states: List[Tuple[int, int]] = []

    def start_state(self) -> Tuple[int, int]:
        return random.choice(self.start_states)


    def detect_collision(self, race_car: RaceCar) -> bool:
        pass

    def detect_finish(self, race_car: RaceCar) -> bool:
        pass

    def parse_file(self, track_file: str) -> None:
        filename: str = "tracks/" + track_file
        f = open(filename)
        x, y = f.readline().strip('\n').split(',')
        self.track = np.zeros((int(x), int(y)))
        line = f.readline()
        i: int = 0
        j: int = 0
        while line:
            for j, cell in enumerate(line.strip("\n")):
                type: CellType = None
                if cell == "#":
                    type = CellType(0)
                elif cell == "S":
                    type = CellType(1)
                    self.start_states.append((i, j))
                elif cell == "F":
                    type = CellType(2)
                else:
                    type = CellType(3)
                self.track[i][j] = type
            i += 1
            line = f.readline()

    def __str__(self) -> str:
        if self._str == "":
            string = ""
            for row in self.track:
                for cell in row:
                    if cell == CellType.WALL:
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
            return string
        else:
            return self._str


def test():
    tracks = ['L-track.txt', 'O-track.txt', 'R-track.txt']
    for track in tracks:
        t = Track(track)
        print(t)


if __name__ == "__main__":
    test()
