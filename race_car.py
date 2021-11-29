
class RaceCar:

    def __init__(self, x_init: int, y_init: int) -> None:
        self.a_x: int = 0
        self.a_y: int = 0
        self.v_x: int = 0
        self.v_y: int = 0
        self.x: int = x_init
        self.y: int = y_init
        pass

    def accelerate(self) -> None:
        # update accelerations here
        self.v_x = self.v_x + (self.a_x * 1)
        self.v_y = self.v_y + (self.a_y * 1)
        pass

