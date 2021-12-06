import random
from typing import List, Tuple
from enum import IntEnum
import numpy as np

from race_car import RaceCar
from geometry import Point, LineSegment, detect_intersection
from state import State

import turtle

scale_factor: float = 10

class CellType(IntEnum):
    WALL = 0
    START = 1
    FINISH = 2
    TRACK = 3


class Track:

    def __init__(self, track_file: str = None, turt: turtle.Turtle = None):
        self.start_states: List[State] = []
        if track_file is None:
            self.parse_file("L-track.txt")
        else:
            self.parse_file(track_file)
            self.track_name: str = track_file.split(".")[0]
        self._str: str = ""
        self.t = turt
        if self.t is not None:
            self.display_track_with_turtle()

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

    def display_track_with_turtle(self):
        self.s = turtle.getscreen()
        self.s.tracer(0)
        self.t = turtle.Turtle()
        turtle.hideturtle()
        self.t.hideturtle()
        self.t.shape("circle")
        self.t.resizemode("user")
        self.t.turtlesize(0.1, 0.1, 0.1)

        cells = self.get_boundaries_of_type(CellType.WALL)
        for boundaries in cells:
            for boundary in boundaries:
                self.t.penup()
                self.t.goto(boundary.p1.x * scale_factor, boundary.p1.y * -scale_factor)
                self.t.pendown()
                self.t.goto(boundary.p2.x * scale_factor, boundary.p2.y * -scale_factor)
        self.s.update()

    def display_transition_with_turtle(self, initial_state: State):
        if self.detect_collision(initial_state):
            self.t.color("red")
        elif self.detect_finish(initial_state):
            self.t.color("green")
        else:
            self.t.color("blue")
        self.t.penup()
        self.t.goto(initial_state.x_pos * scale_factor, initial_state.y_pos * -scale_factor)
        self.t.pendown()
        self.t.goto(scale_factor * (initial_state.x_pos + initial_state.x_vel), -scale_factor * (initial_state.y_pos + initial_state.y_vel))
        self.t.stamp()
        self.t.color("black")
        self.s.update()


def test():
    track = Track("L-track.txt", True)

if __name__ == "__main__":
    test()
