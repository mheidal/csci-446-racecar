import turtle
from typing import List, Dict, Tuple
from enum import IntEnum

from track import Track, TransitionType
from state import State
from race_car import RaceCar
from random import random

class CrashType(IntEnum):
    RESTART = 0,
    STOP = 1

class Model:

    def __init__(self, track: Track, crash_type: CrashType = CrashType.STOP) -> None:
        self.crash_type = crash_type
        self.discount_factor_gamma: float
        self.bellman_error_epsilon: float
        self.track = track
        self.state_space = self.initialize_state_space()

        self.start_state = track.start_state() # THE STATE THE CAR STARTS IN
        self.special_state = State(-1, -1, 0, 0) # A SPECIAL STATE THAT MARKS THAT THE CAR IS DONE
        # self.action_space:

    def initialize_state_space(self):
        possible_velocities = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        state_space: Dict[Tuple[int, int, int, int], State] = {}
        for y, row in enumerate(self.track.track):
            for x, cell in enumerate(row):
                for i in possible_velocities:
                    for j in possible_velocities:
                        state_space[(x, y, i, j)] = State(x, y, i, j)
        return state_space

    def transition(self, state: State, x_acc: int, y_acc: int) -> State:

        x_vel_after: int
        y_vel_after: int

        oil_slick_prob = 0
        # oil_slick_prob = random()

        if oil_slick_prob >= 0.8:
            x_vel_after = state.x_vel
            y_vel_after = state.y_vel
        else:
            x_vel_after = state.x_vel + x_acc if (6 > state.x_vel + x_acc > -6) else state.x_vel
            y_vel_after = state.y_vel + y_acc if (6 > state.y_vel + y_acc > -6) else state.y_vel

        if self.track.t is not None:
            self.track.display_transition_with_turtle(State(state.x_pos, state.y_pos, x_vel_after, y_vel_after))

        if self.crash_type == CrashType.RESTART:
            transition_type = self.track.get_transition_type_without_point(
                State(state.x_pos, state.y_pos, x_vel_after, y_vel_after))
            if transition_type == TransitionType.CRASH:
                return self.start_state
            elif transition_type == TransitionType.WIN:
                return self.special_state
            else:
                return self.state_space[(state.x_pos + x_vel_after,
                                         state.y_pos + y_vel_after,
                                         x_vel_after,
                                         y_vel_after)]

        elif self.crash_type == CrashType.STOP:
            transition_data = self.track.get_transition_type(
                State(state.x_pos, state.y_pos, x_vel_after, y_vel_after))
            if type(transition_data) == tuple:
                transition_type, last_point = transition_data
                return State(last_point.x, last_point.y, 0, 0)
            else:
                if transition_data == TransitionType.WIN:
                    return self.special_state
                else:
                    return self.state_space[(state.x_pos + x_vel_after,
                                         state.y_pos + y_vel_after,
                                         x_vel_after,
                                         y_vel_after)]


    def reward(self, state: State) -> float:
        return 0 if state == self.special_state else -1

def test_model():
    turt: turtle.Turtle = turtle.Turtle()
    track = Track("L-track.txt", turt)
    m = Model(track)

    r = RaceCar(m.start_state)

    def display_r():
        print(r)
        track.s.update()
        print()

    def trans_1():
        r.state = m.transition(r.state, -1, 1)
        display_r()
    def trans_2():
        r.state = m.transition(r.state, 0, 1)
        display_r()
    def trans_3():
        r.state = m.transition(r.state, 1, 1)
        display_r()
    def trans_4():
        r.state = m.transition(r.state, -1, 0)
        display_r()
    def trans_5():
        r.state = m.transition(r.state, 0, 0)
        display_r()
    def trans_6():
        r.state = m.transition(r.state, 1, 0)
        display_r()
    def trans_7():
        r.state = m.transition(r.state, -1, -1)
        display_r()
    def trans_8():
        r.state = m.transition(r.state, 0, -1)
        display_r()
    def trans_9():
        r.state = m.transition(r.state, 1, -1)
        display_r()
    def reset_screen(x, y):
        track.t.clear()
        track.display_track_with_turtle()
        track.t.stamp()
        track.s.update()

    track.s.onkey(trans_1, "1")
    track.s.onkey(trans_2, "2")
    track.s.onkey(trans_3, "3")
    track.s.onkey(trans_4, "4")
    track.s.onkey(trans_5, "5")
    track.s.onkey(trans_6, "6")
    track.s.onkey(trans_7, "7")
    track.s.onkey(trans_8, "8")
    track.s.onkey(trans_9, "9")
    track.s.onscreenclick(reset_screen)

    track.s.listen()
    turtle.mainloop()

if __name__ == "__main__":
    test_model()
