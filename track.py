import random
from typing import List, Tuple
from enum import IntEnum
import numpy as np

from race_car import RaceCar
from geometry import Point, LineSegment, detect_intersection
from state import State

import turtle

class CellType(IntEnum):
    WALL = 0
    START = 1
    FINISH = 2
    TRACK = 3


class Track:

    def __init__(self, track_file: str = None):
        self.start_states: List[State] = []
        if track_file is None:
            self.parse_file("L-track.txt")
        else:
            self.parse_file(track_file)
            self.track_name: str = track_file.split(".")[0]
        self._str: str = ""

    def start_state(self) -> State:
        return random.choice(self.start_states)


    def get_boundaries_of_type(self, type: CellType) -> List[List[LineSegment]]:
        cells: List[List[LineSegment]] = []
        for y, row in enumerate(self.track):
            for x, cell in enumerate(row):
                if cell == type:
                    boundaries = []
                    boundaries.append(LineSegment(Point(x-0.5, y-0.5), Point(x+0.5, y-0.5))) # top
                    boundaries.append(LineSegment(Point(x-0.5, y-0.5), Point(x-0.5, y+0.5))) # left
                    boundaries.append(LineSegment(Point(x+0.5, y-0.5), Point(x+0.5, y+0.5))) # right
                    boundaries.append(LineSegment(Point(x-0.5, y+0.5), Point(x+0.5, y+0.5))) # bottom

                    cells.append(boundaries)
        return cells

    def detect_collision(self, state: State) -> bool:
        trajectory: LineSegment = LineSegment(Point(state.x_pos, state.y_pos),
                                 Point(state.x_pos + state.x_vel, state.y_pos + state.y_vel))
        wall_cells: List[List[LineSegment]] = self.get_boundaries_of_type(CellType.WALL)
        for cell in wall_cells:
            for line_segment in cell:
                if detect_intersection(trajectory, line_segment):
                    return True
        return False

    def detect_finish(self, state: State) -> bool:
        trajectory: LineSegment = LineSegment(Point(state.x_pos, state.y_pos),
                                              Point(state.x_pos + state.x_vel, state.y_pos + state.y_vel))
        finish_cells: List[List[LineSegment]] = self.get_boundaries_of_type(CellType.FINISH)
        for cell in finish_cells:
            for line_segment in cell:
                if detect_intersection(trajectory, line_segment):
                    return True
        return False

    def parse_file(self, track_file: str) -> None:
        filename: str = "tracks/" + track_file
        f = open(filename)
        x, y = f.readline().strip('\n').split(',')
        self.track = np.zeros((int(x), int(y)))
        line = f.readline()
        i: int = 0  # this is y
        j: int = 0  # this is x
        while line:
            for j, cell in enumerate(line.strip("\n")):
                type: CellType = None
                if cell == "#":
                    type = CellType(0)
                elif cell == "S":
                    type = CellType(1)
                    self.start_states.append(State(j, i, 0, 0))
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
    track = Track("L-track.txt")
    s = turtle.getscreen()
    t = turtle.Turtle()
    s.tracer(0)
    t.hideturtle()
    turtle.hideturtle()

    cells = track.get_boundaries_of_type(CellType.WALL)
    for boundaries in cells:
        for boundary in boundaries:
            t.penup()
            t.goto(boundary.p1.x * 10, boundary.p1.y * 10)
            t.pendown()
            t.goto(boundary.p2.x * 10, boundary.p2.y * 10)

    coll = track.detect_collision(State(2,6, 0, 1))
    if coll:
        t.color('red')
    else:
        t.color('green')


    t.penup()
    t.goto(2*10,6*10)
    print(" asdf")
    t.pendown()
    t.goto(2*10, 7*10)
    s.update()

    turtle.mainloop()


if __name__ == "__main__":
    test()
