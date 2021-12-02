from typing import Tuple, List, Dict

from track import CellType
from simulator import Simulator
from state import State


class QLearner:

    def __init__(self) -> None:
        self.simulator: Simulator = Simulator()
        self.q: Dict[Tuple[State, Tuple[int, int]]] = {}  # make a dict of w/ key of Tuple(state, action), value: Reward. Implement the comparable and hashable methods to pass in State as an key
        self.gamma: float = 1
        self.init_q()
        pass

    def init_q(self) -> None:
        rows, columns = self.simulator.model.track.track.shape
        for x_position in range(columns):
            for y_position in range(rows):
                if self.simulator.model.track.track[y_position][x_position] is CellType(0):
                    continue
                for x_velocity in range(-5, 5):
                    for y_velocity in range(-5, 5):
                        for x_acceleration in [-1, 0, 1]:
                            for y_acceleration in [-1, 0, 1]:
                                self.q[(State(x_position, y_position, x_velocity, y_velocity), (x_acceleration, y_acceleration))] = 0
        entries: int = 0
        for key in self.q:
            print(f"key: {str(key[0]), key[1]} value:{self.q.get(key)}")
            entries += 1
        print(entries)


    def q_learn(self) -> None:
        # init all Q(s, a) arbitrarily
        # for all episodes do the following
        #   initialize s
        #   repeat
        #       choose a using policy derived from Q
        #       apply action a
        #       observe Reward(s, a) and successor state s'
        #       Q(s, a) <-- Q(s, a) + alpha( Reward(s, a)) + [gamma * max_a' * Q(s', a')] - Q(s, a) )
        #       s <-- s'
        #   until s is terminal state: if x,y is a finish state... detect_finish() from Track maybe?
        # end for loop

        pass

    def calculate_policy(self) -> None:
        pass

    def step_simulation(self) -> None:
        pass

if __name__ == "__main__":
    q_learner: QLearner = QLearner()
    pass
