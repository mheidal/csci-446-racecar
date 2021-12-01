from state import State

class RaceCar:

    def __init__(self, initial_state: State) -> None:
        self.state = initial_state

    def __str__(self) -> str:
        return f"RaceCar:\ts\tv\ta\nx:\t\t\t{self.state.x_pos}\t{self.state.x_vel}\ny: \t\t\t{self.state.y_pos}\t{self.state.y_vel}"

    def accelerate(self, vertical_acceleration: int = 0, horizontal_acceleration: int = 0) -> None:
        pass
