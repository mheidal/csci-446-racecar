from enum import IntEnum


class Orientation(IntEnum):
    COLINEAR = 0
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        if type(other) == Point:
            return self.x == other.x and self.y == other.y
        return False

class LineSegment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return "(" + str(self.p1) + ", " + str(self.p2) + ")"

# Intersection methods: https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def get_orientation(p: Point, q: Point, r: Point) -> Orientation:
    value = ((q.y - p.y) * (r.x - q.x)) - ((q.x - p.x) * (r.y - q.y))
    if value > 0:
        return Orientation.CLOCKWISE
    elif value < 0:
        return Orientation.COUNTERCLOCKWISE
    elif value == 0:
        return Orientation.COLINEAR

def onSegment(p, q, r):
    print("p", p)
    print("q", q)
    print("r", r)
    print()
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def detect_intersection(l1: LineSegment, l2: LineSegment):
    p1 = l1.p1
    q1 = l1.p2
    p2 = l2.p1
    q2 = l2.p2

    o1 = get_orientation(p1, q1, p2)
    o2 = get_orientation(p1, q1, q2)
    o3 = get_orientation(p2, q2, p1)
    o4 = get_orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # one or both line segments define a single point
    if (p1 == q1 or p2 == q2):
        return False

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False


def test():
    print(detect_intersection(LineSegment(Point(0, 0), Point(10, 10)), LineSegment(Point(1, 1), Point(3, 3))))

if __name__ == "__main__":
    test()