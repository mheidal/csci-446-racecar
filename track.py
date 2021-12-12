import random
from typing import List, Tuple, Union
from enum import IntEnum
import numpy as np

from race_car import RaceCar
from geometry import Point, LineSegment, detect_if_intersect, find_intersection_point, euclid_dist
from state import State

import turtle

scale_factor: float = 15


class CellType(IntEnum):
    WALL = 0
    START = 1
    FINISH = 2
    TRACK = 3


class TransitionType(IntEnum):
    CRASH = 0
    WIN = 1
    MOVE = 2


class Track:

    def __init__(self, track_file: str = "I-track", *, turt: turtle.Turtle = None, progressive_start_states = False):
        self.start_states: List[State] = []
        self.finish_states: List[State] = []
        self.track = self.parse_file(track_file)
        self.track_file = track_file
        if progressive_start_states:
            self.start_states = self.progressive_start_states(1)
        # else:
        #     self.parse_file(track_file)
        #     self.track_name: str = track_file.split(".")[0]

        self._str: str = ""
        self.t = turt
        if self.t is not None:
            self.display_track_with_turtle()

    def start_state(self) -> State:
        start_state = random.choice(self.start_states)
        if self.t is not None:
            self.t.penup()
            self.t.goto(start_state.x_pos * scale_factor, start_state.y_pos * scale_factor * -1)
            self.t.stamp()
            self.s.update()
        return start_state

    def progressive_start_states(self) -> List[List[State]]:
        alphanums = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        arr = np.full(self.track.shape, '#')
        queue = []
        for y, row in enumerate(self.track):
            for x, cell in enumerate(row):
                if cell == CellType.WALL:
                    arr[y][x] = "."
                elif cell == CellType.FINISH:
                    arr[y][x] = "0"
                    queue.append({'x': x, 'y': y})
        while queue:
            cell = queue.pop(0)
            val = arr[cell['y']][cell['x']]
            if val != "#" and val != ".":
                for x_adj in [-1, 0, 1]:
                    for y_adj in [-1, 0, 1]:
                        if arr[cell['y'] + y_adj][cell['x'] + x_adj] == "#":
                            arr[cell['y'] + y_adj][cell['x'] + x_adj] = alphanums[alphanums.index(val) + 1]
                            queue.append({'x':cell['x'] + x_adj, 'y':cell['y'] + y_adj})
        start_state_sets: List[List[State]] = []
        for i in alphanums:
            if i != '0':
                set = []
                for y, row in enumerate(arr):
                    for x, cell in enumerate(row):
                        if i == cell:
                            set.append(State(x, y, 0, 0))
                        #     for x_vel in range(-5, 6):
                        #         for y_vel in range(-5, 6):
                        #             set.append(State(x, y, x_vel, y_vel))
                if set != []:
                    start_state_sets.append(set)
        string = "    "
        for i in range(len(arr[0])):
            string += alphanums[i] + " "
        string += "\n"
        for y, row in enumerate(arr):
            string += alphanums[y] + " | "
            for cell in row:
                string += cell + " "
            string += "\n"
        print(f"Track is\n{string}")

        return start_state_sets

    def get_boundaries_of_type(self, type: CellType, bounding_box: LineSegment) -> List[Tuple[Tuple[int, int], List[LineSegment]]]:
        cells: List[Tuple[Tuple[int, int], List[LineSegment]]] = []
        for y, row in enumerate(self.track):
            for x, cell in enumerate(row):
                if (
                        bounding_box.p1.y - 1 < y < bounding_box.p2.y + 1 or bounding_box.p1.y + 1 > y > bounding_box.p2.y - 1) \
                        and (
                        bounding_box.p1.x - 1 < x < bounding_box.p2.x + 1 or bounding_box.p1.x + 1 > x > bounding_box.p2.x - 1):
                    if cell == type:
                        boundaries = []
                        boundaries.append(LineSegment(Point(x - 0.5, y - 0.5), Point(x + 0.5, y - 0.5)))  # top
                        boundaries.append(LineSegment(Point(x - 0.5, y - 0.5), Point(x - 0.5, y + 0.5)))  # left
                        boundaries.append(LineSegment(Point(x + 0.5, y - 0.5), Point(x + 0.5, y + 0.5)))  # right
                        boundaries.append(LineSegment(Point(x - 0.5, y + 0.5), Point(x + 0.5, y + 0.5)))  # bottom

                        cells.append(((x, y), boundaries))
        return cells

    def get_transition_type(self, state: State) -> Union[TransitionType, Tuple[TransitionType, Point]]:
        if state.y_vel == 0 and state.x_vel == 0:
            return TransitionType.MOVE
        trajectory: LineSegment = LineSegment(Point(state.x_pos, state.y_pos),
                                              Point(state.x_pos + state.x_vel, state.y_pos + state.y_vel))
        closest_intersection: Tuple[float, TransitionType] = (float('inf'), TransitionType.MOVE)

        last_wall_cell_intersect: Point = None

        wall_cells = self.get_boundaries_of_type(CellType.WALL, trajectory)
        for cell in wall_cells:
            boundaries = cell[1]
            for line_segment in boundaries:
                if detect_if_intersect(trajectory, line_segment):
                    intersection_point = find_intersection_point(line_segment, trajectory)
                    last_wall_cell_intersect = intersection_point
                    if closest_intersection is None:
                        closest_intersection = (euclid_dist(trajectory.p1, intersection_point), TransitionType.CRASH)
                    else:
                        old_dist = closest_intersection[0]
                        new_dist = euclid_dist(trajectory.p1, intersection_point)
                        if new_dist < old_dist:
                            closest_intersection = (new_dist, TransitionType.CRASH)

        finish_cells = self.get_boundaries_of_type(CellType.FINISH, trajectory)
        for cell in finish_cells:
            boundaries = cell[1]
            for line_segment in boundaries:
                if detect_if_intersect(trajectory, line_segment):
                    intersection_point = find_intersection_point(line_segment, trajectory)
                    if closest_intersection is None:
                        closest_intersection = (euclid_dist(trajectory.p1, intersection_point), TransitionType.CRASH)
                    else:
                        old_dist = closest_intersection[0]
                        new_dist = euclid_dist(trajectory.p1, intersection_point)
                        if new_dist < old_dist:
                            closest_intersection = (new_dist, TransitionType.WIN)

        # I'm just gonna comment all this out and simplify how crashing works with crash type "stop". Crashing will
        # now just put you back where you last were with your velocity dead.
        # if closest_intersection[1] == TransitionType.CRASH:
        #     furthest_track_boundary: Tuple[float, Point] = None
        #     driveable_cells = self.get_boundaries_of_type(CellType.TRACK, trajectory) + \
        #                       self.get_boundaries_of_type(CellType.START, trajectory) + \
        #                       self.get_boundaries_of_type(CellType.FINISH, trajectory)
        #     for cell in driveable_cells:
        #         boundaries = cell[1]
        #         for line_segment in boundaries:
        #             if detect_if_intersect(trajectory, line_segment):
        #                 intersection_point = find_intersection_point(line_segment, trajectory)
        #                 if furthest_track_boundary is None and intersection_point != last_wall_cell_intersect:
        #                     furthest_track_boundary = (
        #                     euclid_dist(trajectory.p1, intersection_point), intersection_point)
        #                 else:
        #                     if furthest_track_boundary is not None:
        #                         old_dist = furthest_track_boundary[0]
        #                         new_dist = euclid_dist(trajectory.p1, intersection_point)
        #                         if new_dist > old_dist and intersection_point != last_wall_cell_intersect:
        #                             furthest_track_boundary = (new_dist, intersection_point)
        #
        #     if furthest_track_boundary is None:
        #         return TransitionType.CRASH, Point(state.x_pos, state.y_pos)
        #     else:
        #         for cell in driveable_cells:
        #             x, y = cell[0]
        #             matches = 0
        #             boundaries = cell[1]
        #             for line_segment in boundaries:
        #                 if ((line_segment.p1.x >= furthest_track_boundary[
        #                     1].x >= line_segment.p2.x and line_segment.p1.y == furthest_track_boundary[
        #                          1].y and line_segment.p2.y == furthest_track_boundary[1].y)
        #                     or (line_segment.p1.x <= furthest_track_boundary[
        #                             1].x <= line_segment.p2.x and line_segment.p1.y == furthest_track_boundary[
        #                             1].y and line_segment.p2.y == furthest_track_boundary[1].y)
        #                     or (line_segment.p1.y <= furthest_track_boundary[
        #                             1].y <= line_segment.p2.y and line_segment.p1.x == furthest_track_boundary[
        #                             1].x and line_segment.p2.x == furthest_track_boundary[1].x)
        #                     or (line_segment.p1.y <= furthest_track_boundary[
        #                             1].y <= line_segment.p2.y and line_segment.p1.x == furthest_track_boundary[
        #                             1].x and line_segment.p2.x == furthest_track_boundary[1].x)) \
        #                         or ((
        #                                     line_segment.p1.x >= last_wall_cell_intersect.x >= line_segment.p2.x and line_segment.p1.y == last_wall_cell_intersect.y and line_segment.p2.y == last_wall_cell_intersect.y)
        #                             or (
        #                                     line_segment.p1.x <= last_wall_cell_intersect.x <= line_segment.p2.x and line_segment.p1.y == last_wall_cell_intersect.y and line_segment.p2.y == last_wall_cell_intersect.y)
        #                             or (
        #                                     line_segment.p1.y <= last_wall_cell_intersect.y <= line_segment.p2.y and line_segment.p1.x == last_wall_cell_intersect.x and line_segment.p2.x == last_wall_cell_intersect.x)
        #                             or (
        #                                     line_segment.p1.y <= last_wall_cell_intersect.y <= line_segment.p2.y and line_segment.p1.x == last_wall_cell_intersect.x and line_segment.p2.x == last_wall_cell_intersect.x)):
        #                     matches += 1
        #             if matches > 1:
        #                 return closest_intersection[1], Point(x, y)

        return closest_intersection[1]

    def get_transition_type_without_point(self, state: State):
        transition_data = self.get_transition_type(state)
        return transition_data[0] if type(transition_data) == tuple else transition_data

    # def detect_collision(self, state: State) -> bool:
    #     trajectory: LineSegment = LineSegment(Point(state.x_pos, state.y_pos),
    #                              Point(state.x_pos + state.x_vel, state.y_pos + state.y_vel))
    #     wall_cells: List[List[LineSegment]] = self.get_boundaries_of_type(CellType.WALL)
    #     for cell in wall_cells:
    #         for line_segment in cell:
    #             if detect_if_intersect(trajectory, line_segment):
    #                 return True
    #     return False
    #
    # def detect_finish(self, state: State) -> bool:
    #     trajectory: LineSegment = LineSegment(Point(state.x_pos, state.y_pos),
    #                                           Point(state.x_pos + state.x_vel, state.y_pos + state.y_vel))
    #     finish_cells: List[List[LineSegment]] = self.get_boundaries_of_type(CellType.FINISH)
    #     for cell in finish_cells:
    #         for line_segment in cell:
    #             if detect_if_intersect(trajectory, line_segment):
    #                 return True
    #     return False

    def parse_file(self, track_file: str):
        filename: str = "tracks/" + track_file + ".txt"
        f = open(filename)
        x, y = f.readline().strip('\n').split(',')
        track = np.zeros((int(x), int(y)))
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
                    self.finish_states.append(State(j, i, 0, 0))
                else:
                    type = CellType(3)
                track[i][j] = type
            i += 1
            line = f.readline()
        return track

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

        cells = self.get_boundaries_of_type(CellType.WALL, LineSegment(Point(-1 * float('inf'), -1 * float('inf')),
                                                                       Point(float('inf'), float('inf'))))
        for boundaries in cells:
            for boundary in boundaries[1]:
                self.t.penup()
                self.t.goto(boundary.p1.x * scale_factor, boundary.p1.y * -scale_factor)
                self.t.pendown()
                self.t.goto(boundary.p2.x * scale_factor, boundary.p2.y * -scale_factor)

        for i in range(len(self.track)):
            self.t.color("green")
            self.t.penup()
            self.t.goto(-20, i * -1 * scale_factor - 7.5)
            self.t.write(i)
            # self.t.pendown()
            # self.t.goto(-10, i * -1 * scale_factor)

        for i in range(len(self.track[0])):
            self.t.color("red")
            self.t.penup()
            self.t.goto(i * scale_factor, 20)
            self.t.write(i)
            # self.t.pendown()
            # self.t.goto(i * scale_factor, 10)
        self.s.update()

    def display_transition_with_turtle(self, initial_state: State):
        transition_data = self.get_transition_type(initial_state)
        if type(transition_data) == tuple:
            transition_type = transition_data[0]
            if transition_type == TransitionType.CRASH:
                self.t.color("red")
            elif transition_type == TransitionType.WIN:
                self.t.color("green")
            else:
                self.t.color("blue")
        else:
            transition_type = transition_data
            if transition_type == TransitionType.CRASH:
                self.t.color("red")
            elif transition_type == TransitionType.WIN:
                self.t.color("green")
            else:
                self.t.color("blue")
        self.t.penup()
        self.t.goto(initial_state.x_pos * scale_factor, initial_state.y_pos * -scale_factor)
        self.t.pendown()
        self.t.goto(scale_factor * (initial_state.x_pos + initial_state.x_vel),
                    -scale_factor * (initial_state.y_pos + initial_state.y_vel))
        self.t.stamp()
        self.t.color("black")
        self.s.update()


def test():
    Track("L-track").progressive_start_states()
    Track("R-track").progressive_start_states()
    Track("O-track").progressive_start_states()


if __name__ == "__main__":
    test()
