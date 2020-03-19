from matplotlib import pyplot
import numpy

from projective_geometry.visualize import line_endpoints_2d_plot

if __name__ == '__main__':
    x1 = numpy.array([1,3,1])
    x2 = numpy.array([4,1,1])

    x_min = min(x1[0],x2[0]) - 1
    x_max = max(x1[0],x2[0]) + 1
    y_min = min(x1[1],x2[1]) - 1
    y_max = max(x1[1],x2[1]) + 1

    # get the line
    l = numpy.cross(x1,x2)
    print(l)

    intercept1, intercept2 = line_endpoints_2d_plot(
        l,
        [x_min, x_max, y_min, y_max]
    )

    # get the axes of the plot
    f = pyplot.figure()
    ax = f.add_subplot(111)
    ax.plot(x1[0], x1[1], 'ko')
    ax.plot(x2[0], x2[1], 'ko')

    blue_line_x = [intercept1[0], intercept2[0]]
    blue_line_y = [intercept1[1], intercept2[1]]

    ax.plot(blue_line_x, blue_line_y, 'b-')
    # print(dir(ax))
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))

    pyplot.show()
