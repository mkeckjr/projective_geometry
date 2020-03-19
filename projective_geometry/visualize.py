import numpy

def line_endpoints_2d_plot(line_homogeneous, plot_limits):
    """Compute a pair of line enpoints for plotting a line on a 2D grid

    Args:
        line_homogeneous: a 3-vector defining a line in projective 2-space
        plot_limits: a 4-vector of the form [xmin, xmax, ymin, ymax]

    Returns:
        x1: 2-vector of the first endpoint of the line
        x2: 2-vector of the second endpoint of the line
    """

    intersections = []

    x_min, x_max, y_min, y_max = plot_limits

    left_intersection = numpy.cross(line_homogeneous, [1,0,-x_min])
    left_intersection = left_intersection / left_intersection[2]
    if left_intersection[1] <= y_max and left_intersection[1] >= y_min:
        intersections.append(left_intersection)

    right_intersection = numpy.cross(line_homogeneous, [1,0,-x_max])
    right_intersection = right_intersection / right_intersection[2]
    if right_intersection[1] <= y_max and right_intersection[1] >= y_min:
        intersections.append(right_intersection)

    top_intersection = numpy.cross(line_homogeneous, [0,1,-y_max])
    top_intersection = top_intersection / top_intersection[2]
    if top_intersection[0] <= x_max and top_intersection[0] >= x_min:
        intersections.append(top_intersection)

    bottom_intersection = numpy.cross(line_homogeneous, [0,1,-y_min])
    bottom_intersection = bottom_intersection / bottom_intersection[2]
    if bottom_intersection[0] <= x_max and bottom_intersection[0] >= x_min:
        intersections.append(bottom_intersection)

    # there should be two intersection points
    if len(intersections) != 2:
        raise ValueError('More than two intersection points.')

    intercept1, intercept2 = intersections
    return intercept1, intercept2
