from typing import Dict, Tuple


class State:
    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel

    def __str__(self) -> str:
        return f"x:{self.x_pos} y:{self.y_pos} v_x:{self.x_vel} v_y:{self.y_vel}"

    def __key(self):
        return self.x_pos, self.y_pos, self.x_vel, self.y_vel

    def __hash__(self) -> hash:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, State):
            return self.__key() == other.__key()
        return False
