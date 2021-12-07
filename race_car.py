from state import State


class RaceCar:

    def __init__(self, initial_state: State) -> None:
        self.state = initial_state

    def __str__(self) -> str:
        return f"RaceCar:\ts\tv\nx:\t\t\t{self.state.x_pos}\t{self.state.x_vel}\ny: \t\t\t{self.state.y_pos}\t{self.state.y_vel}"
    # TODO: accelerate might be deprecated now that Model's transition() is working.
    # def accelerate(self, vertical_acceleration: int = 0, horizontal_acceleration: int = 0) -> None:
    #     max_positive_acceleration: int = 1
    #     max_positive_velocity: int = 5
    #
    #     # update accelerations
    #     if vertical_acceleration > 0:
    #         self.a_y += 1
    #     elif vertical_acceleration < 0:
    #         self.a_y -= 1
    #     if horizontal_acceleration > 0:
    #         self.a_x += 1
    #     elif horizontal_acceleration < 0:
    #         self.a_x -= 1
    #
    #     # constrain to be in +/-1
    #     self.a_x = self.a_x if self.a_x <= max_positive_acceleration else max_positive_acceleration
    #     self.a_x = self.a_x if self.a_x >= -max_positive_acceleration else -max_positive_acceleration
    #
    #     self.a_y = self.a_y if self.a_y <= max_positive_acceleration else max_positive_acceleration
    #     self.a_y = self.a_y if self.a_y >= -max_positive_acceleration else -max_positive_acceleration
    #
    #     # approx. of kinematics for velocity
    #     self.v_x = self.a_x + self.v_x
    #     self.v_y = self.a_y + self.v_y
    #
    #     # constrain vel. to be in +/-5
    #     self.v_x = self.v_x if self.v_x <= max_positive_velocity else max_positive_velocity
    #     self.v_x = self.v_x if self.v_x >= -max_positive_velocity else -max_positive_velocity
    #
    #     self.v_y = self.v_y if self.v_y <= max_positive_velocity else max_positive_velocity
    #     self.v_y = self.v_y if self.v_y >= -max_positive_velocity else -max_positive_velocity
    #
    # # def accelerate(self, direction) -> None:
    # #     if(direction == 'right'):
    # #         self.a_x += 1
    # #     if (direction == 'left'):
    # #         self.a_x -= 1
    # #     if (direction == 'up'):
    # #         self.a_y += 1
    # #     if (direction == 'down'):
    # #         self.a_y -= 1
