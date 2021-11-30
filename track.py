import random
from typing import List, Tuple
from enum import IntEnum
import numpy as np

from race_car import RaceCar
from geometry import Point, LineSegment, detect_intersection


class CellType(IntEnum):
    WALL = 0
    START = 1
    FINISH = 2
    TRACK = 3


class Track:

    def __init__(self, track_file: str = None):
        self.start_states: List[Tuple[int, int]] = []
        if track_file is None:
            self.parse_file("L-track.txt")
        else:
            self.parse_file(track_file)
        self._str: str = ""
        self.track_name: str = track_file.split(".")[0]


    def start_state(self) -> Tuple[int, int]:
        return random.choice(self.start_states)


    def get_boundaries_of_type(self, type: CellType) -> List[List[LineSegment]]:
        cells: List[List[LineSegment]] = []
        for i, row in enumerate(self.track):
            for j, cell in enumerate(row):
                if cell == type:
                    boundaries = []
                    boundaries.append(LineSegment(Point(i, j), Point(i, j+1)))
                    boundaries.append(LineSegment(Point(i, j), Point(i+1, j)))
                    boundaries.append(LineSegment(Point(i+1, j), Point(i+1, j+1)))
                    boundaries.append(LineSegment(Point(i, j+1), Point(i+1, j+1)))
                    cells.append(boundaries)
        return cells


    def detect_collision(self, race_car: RaceCar) -> bool:
        trajectory: LineSegment = LineSegment(Point(race_car.x, race_car.y),
                                 Point(race_car.x + race_car.v_x, race_car.y + race_car.v_y))
        wall_cells: List[List[LineSegment]] = self.get_boundaries_of_type(CellType.WALL)
        for cell in wall_cells:
            for line_segment in cell:
                if detect_intersection(trajectory, line_segment):
                    return True
        return False

    def detect_finish(self, race_car: RaceCar) -> bool:
        trajectory: LineSegment = LineSegment(Point(race_car.x, race_car.y),
                                              Point(race_car.x + race_car.v_x, race_car.y + race_car.v_y))
        finish_cells: List[List[LineSegment]] = self.get_boundaries_of_type(CellType.FINISH)
        for cell in finish_cells:
            for line_segment in cell:
                if geometry.detect_intersection(trajectory, line_segment):
                    return True
        return False

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
 #   tracks = ['L-track.txt', 'O-track.txt', 'R-track.txt']
#    for track in tracks:
    t = Track("L-track.txt")
    cells = t.get_boundaries_of_type(CellType.START)
    for cell in cells:
        for line_segment in cell:
            print(line_segment)

if __name__ == "__main__":
    test()
