class State:
    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel

    def __str__(self) -> str:
        return f"x:{self.x_pos} y:{self.y_pos} v_x:{self.x_vel} v_y:{self.y_vel}"

    def __key(self):
        """
        Generates the key for the hash of this State
        :return: key for this State for the Hash
        """
        return self.x_pos, self.y_pos, self.x_vel, self.y_vel

    def __hash__(self) -> hash:
        """
        Hashes this State
        :return: Hash of this State.
        """
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        """
        Evaluates the equality of this State with other objects.
        :param other: An object to equate with this State
        :return: bool representing the equality of this State to other.
        """
        if isinstance(other, State):
            return self.__key() == other.__key()
        return False
