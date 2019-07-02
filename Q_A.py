import matplotlib.pyplot as plt

from geometry import Point
from geometry import Triangle

if __name__ == '__main__':

    points = []
    triangles = []
    lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
    const = 1000.0

    # Reading points
    with open('points.txt', "r", encoding="utf8") as stringlines:
        next(stringlines)
        for line in stringlines:
            # split the line by comma
            fields = line.split(",")
            points.append(Point(float(fields[1]), float(fields[2]), float(fields[3].replace('\n', '')), int(fields[0])))

    # Reading triangles
    with open('triangulation.txt', "r", encoding="utf8") as stringlines:
        next(stringlines)
        for line in stringlines:
            # split the line by comma
            fields = line.split(",")
            triangles.append(Triangle(points[int(fields[1]) - 1], points[int(fields[2]) - 1],
                                      points[int(fields[3].replace('\n', '')) - 1],
                                      int(fields[0])))
    plt.axes().set_aspect('equal')
    # Plotting both points and triangles (with duplicates)
    for i in range(0, len(points)):
        plt.plot(points[i].x, points[i].y, 'bo--')
    for i in range(0, len(triangles)):
        plt.plot([triangles[i].p1.x, triangles[i].p2.x, triangles[i].p3.x, triangles[i].p1.x],
                 [triangles[i].p1.y, triangles[i].p2.y,
                  triangles[i].p3.y, triangles[i].p1.y], 'b')
    # plt.show()
    axes = plt.axis()

    for i in range(0, len(triangles)):
        for j in range(0, len(triangles)):
            if j == i:
                continue
            if (triangles[i].list_of_points[0] in triangles[j].list_of_points) and (
                    triangles[i].list_of_points[1] in triangles[j].list_of_points):
                triangles[i].t1 = triangles[j]
            if (triangles[i].list_of_points[0] in triangles[j].list_of_points) and (
                    triangles[i].list_of_points[2] in triangles[j].list_of_points):
                triangles[i].t2 = triangles[j]
            if (triangles[i].list_of_points[1] in triangles[j].list_of_points) and (
                    triangles[i].list_of_points[2] in triangles[j].list_of_points):
                triangles[i].t3 = triangles[j]


    def cntoftrg(t: Triangle):  # Solving center of triangle by 3 points (two perpendicular lines)
        def slope(p1: Point, p2: Point):
            return (p2.y - p1.y) / (p2.x - p1.x)

        x_value = (slope(t.p1, t.p2) * slope(t.p2, t.p3) * (t.p1.y - t.p3.y) + slope(t.p2, t.p3) * (
                t.p1.x + t.p2.x) - slope(t.p1, t.p2) * (t.p2.x + t.p3.x)) / (
                          2 * (-slope(t.p1, t.p2) + slope(t.p2, t.p3)))
        y_value = -(x_value - (t.p1.x + t.p2.x) / 2) / (slope(t.p1, t.p2)) + (t.p1.y + t.p2.y) / 2
        return Point(x_value, y_value)


    def infpoint(p1, p2, p3, center):
        def slope(p1: Point, p2: Point):
            if p1.x > p2.x:
                return (p1.y - p2.y) / (p1.x - p2.x)
            else:
                return (p2.y - p1.y) / (p2.x - p1.x)

        def yofprp(p1, p2, p3, some_x):
            return -(some_x - p3.x) / (slope(p1, p2)) + p3.y

        def yofseg(p1, p2, some_x):
            return slope(p1, p2) * (some_x - p1.x) + p1.y

        dx = 0
        dy = 0
        if p1.x > p2.x:
            dx = p1.x - p2.x
            dy = p1.y - p2.y
        else:
            dx = p2.x - p1.x
            dy = p2.y - p1.y

        if ((dx > 0) and (dy < 0)) and p3.y < yofseg(p1, p2, p3.x):
            return Point(const, (-(const - center.x)) / (slope(t.p1, t.p2)) + center.y)

        elif ((dx > 0) and (dy > 0)) and p3.y > yofseg(p1, p2, p3.x):
            return Point(const, (-(const - center.x)) / (slope(t.p1, t.p2)) + center.y)

        elif ((dx > 0) and (dy < 0)) and p3.y > yofseg(p1, p2, p3.x):
            return Point(-const, (-(-const - center.x)) / (slope(t.p1, t.p2)) + center.y)

        elif ((dx > 0) and (dy > 0)) and p3.y < yofseg(p1, p2, p3.x):
            return Point(-const, (-(-const - center.x)) / (slope(t.p1, t.p2)) + center.y)
        else:
            print('bad')


    Voronoi_vertices = []
    Voronoi_edges = []

    for t in triangles:  # Generating edges of Voronoi + vertexes
        if t.t1 == None:
            Voronoi_vertices.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(infpoint(t.p1, t.p2, t.p3, cntoftrg(t)))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t2))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t3))
            continue
        if t.t2 == None:
            Voronoi_vertices.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t1))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(infpoint(t.p1, t.p3, t.p2, cntoftrg(t)))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t3))
            continue
        if t.t3 == None:
            Voronoi_vertices.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t1))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t2))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(infpoint(t.p2, t.p3, t.p1, cntoftrg(t)))
            continue
        else:
            Voronoi_vertices.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t1))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t2))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t3))

    # Plotting both points and triangles (with duplicates)
    for i in range(0, len(Voronoi_vertices)):
        plt.plot(Voronoi_vertices[i].x, Voronoi_vertices[i].y, 'ro--')
    for i in range(0, len(Voronoi_edges), 2):
        plt.plot([Voronoi_edges[i].x, Voronoi_edges[i + 1].x],
                 [Voronoi_edges[i].y, Voronoi_edges[i + 1].y], 'r')

    plt.xlim([axes[0], axes[1]])
    plt.ylim([axes[2], axes[3]])
    plt.show()
    print('Done')
