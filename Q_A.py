import matplotlib.pyplot as plt
import numpy as np

from geometry import Point
from geometry import Triangle

if __name__ == '__main__':

    points = []
    triangles = []
    const = 1000000.0  # Constant used to calculate infinity far points of Voronoi

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
    axes = plt.axis()  # Saving ratio of plot axes

    # Adding closest Triangles to each Triangle
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


    # Solving center of triangle by 3 points (two perpendicular lines)
    def cntoftrg(t: Triangle):
        def slope(p1: Point, p2: Point):
            return (p2.y - p1.y) / (p2.x - p1.x)

        x_value = (slope(t.p1, t.p2) * slope(t.p2, t.p3) * (t.p1.y - t.p3.y) + slope(t.p2, t.p3) * (
                t.p1.x + t.p2.x) - slope(t.p1, t.p2) * (t.p2.x + t.p3.x)) / (
                          2 * (-slope(t.p1, t.p2) + slope(t.p2, t.p3)))
        y_value = -(x_value - (t.p1.x + t.p2.x) / 2) / (slope(t.p1, t.p2)) + (t.p1.y + t.p2.y) / 2
        return Point(x_value, y_value)


    # Returning Point of orthogonal line that goes to infinity (depends on const variable)
    def infpoint(p1, p2, p3, center):
        # Calculating slope
        def slope(p1: Point, p2: Point):
            if p1.x > p2.x:
                return (p1.y - p2.y) / (p1.x - p2.x)
            else:
                return (p2.y - p1.y) / (p2.x - p1.x)

        def yofprp(p1, p2, p3, some_x):
            return -(some_x - p3.x) / (slope(p1, p2)) + p3.y

        def yofseg(p1, p2, some_x):
            return slope(p1, p2) * (some_x - p1.x) + p1.y

        # Calculating shifts for easier comparison
        dx = 0
        dy = 0
        if p1.x > p2.x:
            dx = p1.x - p2.x
            dy = p1.y - p2.y
        else:
            dx = p2.x - p1.x
            dy = p2.y - p1.y

        #
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

    for i, t in enumerate(triangles):  # Generating edges of Voronoi + vertexes
        if t.t1 == None:
            Voronoi_vertices.append([cntoftrg(t), i])
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(infpoint(t.p1, t.p2, t.p3, cntoftrg(t)))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t2))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t3))
            continue
        if t.t2 == None:
            Voronoi_vertices.append([cntoftrg(t), i])
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t1))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(infpoint(t.p1, t.p3, t.p2, cntoftrg(t)))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t3))
            continue
        if t.t3 == None:
            Voronoi_vertices.append([cntoftrg(t), i])
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t1))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t2))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(infpoint(t.p2, t.p3, t.p1, cntoftrg(t)))
            continue
        else:
            Voronoi_vertices.append([cntoftrg(t), i])
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t1))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t2))
            Voronoi_edges.append(cntoftrg(t))
            Voronoi_edges.append(cntoftrg(t.t3))

    # Plotting both points and triangles (with duplicates)
    for i in range(0, len(Voronoi_vertices)):
        plt.plot(Voronoi_vertices[i][0].x, Voronoi_vertices[i][0].y, 'ro--')
    for i in range(0, len(Voronoi_edges), 2):
        plt.plot([Voronoi_edges[i].x, Voronoi_edges[i + 1].x],
                 [Voronoi_edges[i].y, Voronoi_edges[i + 1].y], 'r')

    plt.xlim([axes[0], axes[1]])
    plt.ylim([axes[2], axes[3]])
    plt.show()
    print('Done part 1, Starting Part 2 (interpolation)')

    print('Please input the value of X:')
    input_x = float(input())
    print('Please input the value of Y:')
    input_y = float(input())
    newpoint = Point(input_x, input_y)
    print('Point P(', newpoint.x, ',', newpoint.y, ') Created')
    type_intr = 0
    while True:
        if (type_intr == 1) or (type_intr == 2) or (type_intr == 3) or (type_intr == 4):
            break
        print('Please choose type of interpolation: NB - 1, IDW - 2, Area - 3, Plane - 4')
        type_intr = int(input())
    print('Your choose:', type_intr)


    def distance(p1, p2):
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


    if type_intr == 1:  # Case 1 Nearest Neighbor
        temp_dist = const
        temp_trgl_id = None
        for cell in Voronoi_vertices:  # Look to which cell new point is closer
            if temp_dist > distance(newpoint, cell[0]):
                temp_dist = distance(newpoint, cell[0])
                temp_trgl_id = cell[1]
        temp_dist = const
        if temp_dist > distance(newpoint, triangles[temp_trgl_id].p1):  # Checking each point in triangle that we found
            temp_dist = distance(newpoint, triangles[temp_trgl_id].p1)
            newpoint.z = triangles[temp_trgl_id].p1.z
        if temp_dist > distance(newpoint, triangles[temp_trgl_id].p2):  # Checking each point in triangle that we found
            temp_dist = distance(newpoint, triangles[temp_trgl_id].p1)
            newpoint.z = triangles[temp_trgl_id].p2.z
        if temp_dist > distance(newpoint, triangles[temp_trgl_id].p3):  # Checking each point in triangle that we found
            temp_dist = distance(newpoint, triangles[temp_trgl_id].p1)
            newpoint.z = triangles[temp_trgl_id].p3.z

    if type_intr == 2:  # Case 2 IDW
        temp_dist = const
        temp_trgl_id = None
        for cell in Voronoi_vertices:  # Look to which cell new point is closer
            if temp_dist > distance(newpoint, cell[0]):
                temp_dist = distance(newpoint, cell[0])
                temp_trgl_id = cell[1]
        newpoint.z = (distance(newpoint, triangles[temp_trgl_id].p1) * triangles[temp_trgl_id].p1.z + distance(newpoint,
                                                                                                               triangles[
                                                                                                                   temp_trgl_id].p2) *
                      triangles[temp_trgl_id].p2.z + distance(newpoint, triangles[temp_trgl_id].p3) * triangles[
                          temp_trgl_id].p3.z) / (distance(newpoint, triangles[temp_trgl_id].p1) + distance(newpoint,
                                                                                                           triangles[
                                                                                                               temp_trgl_id].p2)
                                                 + distance(newpoint, triangles[temp_trgl_id].p3))
    if type_intr == 3:  # AutoCad solution!
        print('Manual solution')
    if type_intr == 4:  # Case 4 Plane
        temp_dist = const
        tti = None  # Temp triangle id
        for cell in Voronoi_vertices:  # Look to which cell new point is closer
            if temp_dist > distance(newpoint, cell[0]):
                temp_dist = distance(newpoint, cell[0])
                tti = cell[1]
        p1p2 = np.array([triangles[tti].p2.x - triangles[tti].p1.x, triangles[tti].p2.y - triangles[tti].p1.y,
                         triangles[tti].p2.z - triangles[tti].p1.z])
        p1p3 = np.array([triangles[tti].p3.x - triangles[tti].p1.x, triangles[tti].p3.y - triangles[tti].p1.y,
                         triangles[tti].p3.z - triangles[tti].p1.z])
        abc = p1p2 * p1p3  # Creating a b c of plane
        d = -(abc[0] * triangles[tti].p1.x + abc[1] * triangles[tti].p1.y + abc[2] * triangles[tti].p1.z)  # d of plane
        newpoint.z = -(abc[0] * newpoint.x + abc[1] * newpoint.y + d) / (abc[2])  # Inserting new point into function of plane

    print('The interpolation result is:', newpoint.z)
