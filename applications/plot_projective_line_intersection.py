from matplotlib import pyplot
import numpy

from ..visualize import line_endpoints_2d_plot

if __name__ == '__main__':
    l1 = numpy.array([1,-1,2])
    l2 = numpy.array([1,-1,3]) # [-0.5,-1,4])

    x = numpy.cross(l1,l2)
    print(x)
    # x = x/x[2]
    # print(x)

    x_min = x[0] - 3
    x_max = x[0] + 3
    y_min = x[1] - 3
    y_max = x[1] + 3

    l1_x1, l1_x2 = line_endpoints_2d_plot(
        l1,
        [x_min, x_max, y_min, y_max]
    )

    l2_x1, l2_x2 = line_endpoints_2d_plot(
        l2,
        [x_min, x_max, y_min, y_max]
    )

    # get the axes of the plot
    f = pyplot.figure()
    ax = f.add_subplot(111)

    l1_xs = [l1_x1[0], l1_x2[0]]
    l1_ys = [l1_x1[1], l1_x2[1]]

    l2_xs = [l2_x1[0], l2_x2[0]]
    l2_ys = [l2_x1[1], l2_x2[1]]

    ax.plot(l1_xs, l1_ys, 'b-')
    ax.plot(l2_xs, l2_ys, 'g-')
    # ax.plot(x[0], x[1], 'ko')
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))

    pyplot.show()
