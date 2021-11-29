
class RaceCar:

    def __init__(self, x_init: int, y_init: int) -> None:
        self.a_x: int = 0
        self.a_y: int = 0
        self.v_x: int = 0
        self.v_y: int = 0
        self.x: int = x_init
        self.y: int = y_init

    def accelerate(self, vertical_acceleration: int = 0, horizontal_acceleration: int = 0) -> None:
        if vertical_acceleration > 0:
            self.a_y += 1
        elif vertical_acceleration < 0:
            self.a_y -= 1
        if horizontal_acceleration > 0:
            self.a_x += 1
        elif horizontal_acceleration < 0:
            self.a_y -= 1
        self.v_x = self.v_x + (self.a_x * 1)
        self.v_y = self.v_y + (self.a_y * 1)

