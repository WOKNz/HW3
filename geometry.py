class Point:  # Class of Point with option to have ID
    def __init__(self, x, y, z, sid=None):
        self.x = x
        self.y = y
        self.z = z
        self.id = sid


class Triangle:  # Class of triangle with option to have ID
    def __init__(self, p1: Point, p2: Point, p3: Point, sid=None):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.id = sid
