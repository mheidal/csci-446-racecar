from typing import Tuple, List, Dict

from racecar.simulator import Simulator


class QLearner:

    def __init__(self) -> None:
        self.simulator: Simulator = Simulator()
        self.q: Dict[Tuple[State, List[int]], int] = {}  # make a dict of w/ key of Tuple(state, action), value: Reward. Implement the comparable and hashable methods to pass in State as an key
        self.gamma: float = 1
        pass

    def init_q(self) -> None:
        # we may just want to use the __init__() for this
        pass

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
