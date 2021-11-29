import numpy as np
from enum import IntEnum

class CellType(IntEnum):
    WALL = 0
    START = 1
    FINISH = 2
    TRACK = 3

class Track:

    def __init__(self, track_file: str = None):
        if track_file is None:
            self.parse_file("L-track.txt")
        else:
            self.parse_file(track_file)

    def parse_file(self, track_file: str):
        filename: str = "tracks/" + track_file
        f = open(filename)
        x, y = f.readline().strip('\n').split(',')
        self.track = np.zeros((int(x), int(y)))
        line = f.readline()
        i: int = 0
        j: int = 0
        while line:
            for j, cell in enumerate(line.strip("\n")):
                type: CellType = None
                if cell == "#":
                    type = CellType(0)
                elif cell == "S":
                    type = CellType(1)
                elif cell == "F":
                    type = CellType(2)
                else:
                    type = CellType(3)
                self.track[i][j] = type
            i += 1
            line = f.readline()

    def __str__(self):
        string = ""
        for row in self.track:
            for cell in row:
                if cell == CellType.WALL:
                    string += "#"
                elif cell == CellType.START:
                    string += "S"
                elif cell == CellType.FINISH:
                    string += "F"
                else:
                    string += "."
                string += " "
            string += "\n"
        return string



def test():
    tracks = ['L-track.txt', 'O-track.txt', 'R-track.txt']
    for track in tracks:
        t = Track(track)
        print(t)

if __name__ == "__main__":
    test()