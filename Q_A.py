import matplotlib.pyplot as plt

from geometry import Point
from geometry import Triangle

if __name__ == '__main__':

    points = []
    triangles = []
    lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]

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

    # Plotting both points and triangles (with duplicates)
    for i in range(0, len(points)):
        plt.plot(points[i].x, points[i].y, 'bo--')
    for i in range(0, len(triangles)):
        plt.plot([triangles[i].p1.x, triangles[i].p2.x, triangles[i].p3.x, triangles[i].p1.x],
                 [triangles[i].p1.y, triangles[i].p2.y,
                  triangles[i].p3.y, triangles[i].p1.y], 'r')
    plt.show()

    # c = np.array([(0, 0, 1, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
    #
    # lc = mc.LineCollection(lines, colors=c, linewidths=2)
    # fig, ax = pl.subplots()
    # ax.add_collection(lc)
    # ax.autoscale()
    # ax.margins(0.1)
    # fig.show()
