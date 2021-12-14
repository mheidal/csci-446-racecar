import turtle
from typing import List, Dict, Tuple
from random import random
from os.path import exists

from track import Track
from state import State
from race_car import RaceCar
from enums import CrashType, TransitionType, CellType


class Model:
    """
    A class used to control the motion of the race car across the track.
    """

    def __init__(self, track: Track, crash_type: CrashType = CrashType.RESTART) -> None:
        self.num_transitions = 0
        self.num_wins = 0
        self.average_transitions = 0
        self.record_length = 250
        self.crash_type = crash_type
        self.discount_factor_gamma: float
        self.bellman_error_epsilon: float
        self.track = track
        self.state_space = self.initialize_state_space()
        self.track_state_space = self.initialize_track_state_space()
        self.start_state = track.start_state()  # THE STATE THE CAR STARTS IN
        self.special_state = State(-1, -1, 0, 0)  # A SPECIAL STATE THAT MARKS THAT THE CAR IS DONE
        # print("setting up trans map")
        self.transition_map = self.init_transition_map()
        # print("finished setting up trans map")
        # self.action_space:

    def initialize_state_space(self):
        """
        Creates a dictionary mapping a set of four ints representing a legal state on the board to a State object.
        """
        possible_velocities = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        state_space: Dict[Tuple[int, int, int, int], State] = {}
        for y, row in enumerate(self.track.track):
            for x, cell in enumerate(row):
                for i in possible_velocities:
                    for j in possible_velocities:
                        state_space[(x, y, i, j)] = State(x, y, i, j)
        return state_space

    def initialize_track_state_space(self):
        """
        A duplicate of the above function with extra functionality.
        """
        possible_velocities = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        state_space: Dict[Tuple[int, int, int, int], State] = {}
        for y, row in enumerate(self.track.track):
            for x, cell in enumerate(row):
                for i in possible_velocities:
                    for j in possible_velocities:
                        if (self.track.track[y][x] != CellType.WALL):
                            state_space[(x, y, i, j)] = State(x, y, i, j)
        return state_space

    def init_transition_map(self) -> Dict:
        """
        Helper method used to load a dictionary used to ease the burden of calculating transitions.
        Calculates the results and probability distribution of every state-action pair and stores them in a dictionary.
        Also writes that dictionary to a file on the disk. If that file already exists, it can be parsed and loaded
        as a dict into memory.
        :return:
        """
        transition_file_name = "tracks/" + self.track.track_file + "-transition-map"
        if self.track.track_file == "R-track":
            transition_file_name += "-" + self.crash_type.name.lower()
        if exists(f"{transition_file_name}.txt"):
            return self.read_transition_map_from_file()
        else:
            table = {}

            print(len(self.state_space.values()))
            for i, state in enumerate(self.state_space.values()):
                if i % 100 == 0:
                    print(i)
                for x_acc in [-1, 0, 1]:
                    for y_acc in [-1, 0, 1]:
                        table[(state, x_acc, y_acc)] = self.get_transitions_and_probabilities(state, x_acc, y_acc)
            self.write_transition_map_to_file(table)
        return table

    def write_transition_map_to_file(self, table: Dict):
        """
        Helper method used to write a dictionary into memory.
        :param table: The dictionary to be stored in memory.
        """
        transition_file_name = "tracks/" + self.track.track_file + "-transition-map"
        if self.track.track_file == "R-track":
            transition_file_name += "-" + self.crash_type.name.lower()
        with open(f"{transition_file_name}.txt", 'w') as file:
            for key, value in table.items():
                init_state: State = key[0]
                x_acc: int = key[1]
                y_acc: int = key[2]
                prob_0, final_0, prob_1, final_1 = value[0][0], value[0][1], value[1][0], value[1][1]
                string = f"{init_state.x_pos},{init_state.y_pos},{init_state.x_vel},{init_state.y_vel},{x_acc},{y_acc}:{prob_0},{final_0.x_pos},{final_0.y_pos},{final_0.x_vel},{final_0.y_vel}:{prob_1},{final_1.x_pos},{final_1.y_pos},{final_1.x_vel},{final_1.y_vel}\n"
                file.write(string)
        return

    def read_transition_map_from_file(self) -> Dict:
        """
        Helper method used to read a dictionary from memory.
        :return: The dictionary stored in memory.
        """
        transition_file_name = "tracks/" + self.track.track_file + "-transition-map"
        if self.track.track_file == "R-track":
            transition_file_name += "-" + self.crash_type.name.lower()
        table = {}
        with open(f"{transition_file_name}.txt", 'r') as file:
            line = file.readline()
            while line:
                key, val0, val1 = line.strip("\n").split(":")
                init_x_pos, init_y_pos, init_x_vel, init_y_vel, x_acc, y_acc = key.split(',')
                init_state = State(int(init_x_pos), int(init_y_pos), int(init_x_vel), int(init_y_vel))
                prob_0, final_0_x_pos, final_0_y_pos, final_0_x_vel, final_0_y_vel = val0.split(",")
                prob_1, final_1_x_pos, final_1_y_pos, final_1_x_vel, final_1_y_vel = val1.split(",")

                final_state_0 = State(int(final_0_x_pos), int(final_0_y_pos), int(final_0_x_vel), int(final_0_y_vel))
                final_state_1 = State(int(final_1_x_pos), int(final_1_y_pos), int(final_1_x_vel), int(final_1_y_vel))
                table[(init_state, int(x_acc), int(y_acc))] = (
                (float(prob_0), final_state_0), (float(prob_1), final_state_1))
                line = file.readline()

        return table

    def report_progress_for_q_learn(self):
        """
        A helper method used to print data from execution of Q-learning. Reports how many actions are required for the
        Q-learner to reach the finish line over a particular time span.
        """
        self.num_wins += 1
        self.average_transitions += self.num_transitions
        if self.num_wins % self.record_length == 0:
            print(f"Win {self.num_wins} after {self.num_transitions} actions. Average over the last "
                  f"{self.record_length}:\n\t{self.average_transitions / self.record_length}")
            self.average_transitions = 0
        self.num_transitions = 0,
        if self.track.t is not None:
            self.track.t.clear()
            self.track.display_track_with_turtle()
            self.track.t.stamp()
            self.track.s.update()

    def get_transitions_and_probabilities(self, state: State, x_acc: int, y_acc: int) -> List[Tuple[float, State]]:
        """
        A helper method used to get all possible results of taking an action and the associated probabilities of each
        resultant state.
        :param state: The initial state of the race car.
        :param x_acc: The acceleration in the x-direction of the race car.
        :param y_acc: The acceleration in the y-direction of the race car.
        :return: A list of resultant states and their probabilities.
        """
        return [(0.2, self.transition(state, x_acc, y_acc, success_probability=0)),
                (0.8, self.transition(state, x_acc, y_acc, success_probability=1))]

    def transition(self, state: State, x_acc: int, y_acc: int, *, success_probability: float = 0) -> State:
        """
        The core method of state, used to determine the motion of the race car across the track.
        Implements the randomness inherent in the environment, determining the results of an acceleration action.
        Depending on whether the model is meant to stop the car or reset it to its initial state upon crashing, finds
        the resultant state of the race car's motion.
        :param state: The initial state of the race car.
        :param x_acc: The acceleration in the x-direction of the race car.
        :param y_acc: The acceleration in the y-direction of the race car.
        :param success_probability: the threshold at which the race car will fail to accelerate.
        :return: The resulting state of the action taken by the race car in a particular state.
        """
        self.num_transitions += 1
        x_vel_after: int
        y_vel_after: int

        # oil_slick_prob = 0
        oil_slick_prob = random()

        if oil_slick_prob >= 1 - success_probability:
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
                # self.report_progress_for_q_learn()
                return self.special_state
            elif transition_type == TransitionType.MOVE:
                return self.state_space[(state.x_pos + x_vel_after,
                                         state.y_pos + y_vel_after,
                                         x_vel_after,
                                         y_vel_after)]

        elif self.crash_type == CrashType.STOP:
            transition_type = self.track.get_transition_type(State(state.x_pos, state.y_pos, x_vel_after, y_vel_after))
            if transition_type == TransitionType.CRASH:
                return State(state.x_pos, state.y_pos, 0, 0)
            elif transition_type == TransitionType.WIN:
                # self.report_progress_for_q_learn()
                return self.special_state
            elif transition_type == TransitionType.MOVE:
                return self.state_space[(state.x_pos + x_vel_after,
                                         state.y_pos + y_vel_after,
                                         x_vel_after,
                                         y_vel_after)]

    def reward(self, state: State) -> int:
        """
        Determines the reward for the race car reaching a particular state.
        :param state: The state of the race car.
        :return: -1 if the race car has not crossed the finish line, 0 otherwise.
        """
        return 0 if state == self.special_state else -1

    def average_transition(self) -> float:
        """
        Used in Q_learning to record statistics.
        :return: The average number of transitions over the last record_length number of runs.
        """
        return self.average_transitions / self.record_length

"""
Below is a set of methods which can be used to navigate the race car around the track manually. Used in development
to debug geometry and transition methods.
Race car can be operated using the numpad keys to indicate directional acceleration. The state of the game is displayed
using the turtle module.

To use, run the test_model method.
"""
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
        print("Transition 1")
        r.state = m.transition(r.state, -1, 1)
        display_r()

    def trans_2():
        print("Transition 2")
        r.state = m.transition(r.state, 0, 1)
        display_r()

    def trans_3():
        print("Transition 3")
        r.state = m.transition(r.state, 1, 1)
        display_r()

    def trans_4():
        print("Transition 4")
        r.state = m.transition(r.state, -1, 0)
        display_r()

    def trans_5():
        print("Transition 5")
        r.state = m.transition(r.state, 0, 0)
        display_r()

    def trans_6():
        print("Transition 6")
        r.state = m.transition(r.state, 1, 0)
        display_r()

    def trans_7():
        print("Transition 7")
        r.state = m.transition(r.state, -1, -1)
        display_r()

    def trans_8():
        print("Transition 8")
        r.state = m.transition(r.state, 0, -1)
        display_r()

    def trans_9():
        print("Transition 9")
        r.state = m.transition(r.state, 1, -1)
        display_r()

    def reset_screen(x, y):
        track.t.clear()
        track.display_track_with_turtle()
        track.t.stamp()
        track.s.update()

    def go_to_start():
        r.state = track.start_state()

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
    track.s.onkey(go_to_start(), "r")

    track.s.listen()
    turtle.mainloop()

if __name__ == "__main__":
    test_model()
