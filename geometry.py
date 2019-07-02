class Point:  # Class of Point with option to have ID
    def __init__(self, x, y, z, sid=None):
        self.x = x
        self.y = y
        self.z = z
        self.id = sid


class Triangle:  # Class of triangle with option to have ID
    def __init__(self, p1: Point, p2: Point, p3: Point, sid=None, t1=None, t2=None, t3=None):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.id = sid
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.list_of_points = [p1.id, p2.id, p3.id]
