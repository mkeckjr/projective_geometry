import argparse

import cv2
from matplotlib import pyplot
import numpy

import projective_geometry.visualize


def point_list_to_lines(point_list):
    """Create 4 lines from a set of 4 points

    This function assumes that 4 points are provided as an iterable with 4
    elements, where each element in turn has two elements, each of which should
    be an x (column) and y (row) coordinate in an image. This computes the four
    lines between each point and the one that follows it in the list. It also
    computes the line between the final point and the first point.

    Args:
        point_list: iterable with four elements, each of which should be an (x,y)
            image coordinate

    Returns:
        4x3 numpy array of lines created by the four points
    """

    lines = []
    for i in range(4):
        x1, y1 = point_list[i]
        x2, y2 = point_list[(i+1)%4]

        l_hat = numpy.cross([x1,y1,1], [x2,y2,1])
        l_hat = l_hat / numpy.sqrt((l_hat**2).sum())
        lines.append(l_hat)

    return numpy.array(lines)


def execute(image_filename, is_bgr):
    """Affinely rectify an input image with manual annotation

    This file will read an image, present that image to the user and wait for
    the user to click on 4 corners of a plane in the image. It will then
    automatically affinely rectify the image.

    Args:
        image_filename: a filename of an image
    """
    im = cv2.imread(image_filename)
    if is_bgr:
        im = im[:,:,::-1]

    f = pyplot.figure()
    ax = f.add_subplot(111)
    ax.imshow(im)
    ax.set_title('Please click 4 corners of a planar surface in clockwise order.')
    corners = pyplot.ginput(4)

    pyplot.close(f)

    # first get the four lines that these points create
    homogeneous_points = numpy.array([
        [point[0], point[1], 1]
        for point in corners
    ]).T
    homogeneous_lines = point_list_to_lines(corners)

    # get a plottable version of those lines
    x_min = 0
    y_min = 0
    x_max = im.shape[1]
    y_max = im.shape[0]

    f = pyplot.figure()
    ax = f.add_subplot(111)
    ax.imshow(im)
    ax.set_title('Corners of plane and vanishing lines')

    for hline in homogeneous_lines:
        x1, x2 = projective_geometry.visualize.line_endpoints_2d_plot(
            hline, [x_min, x_max, y_min, y_max])
        ax.plot([x1[0], x2[0]],
                [x1[1], x2[1]],
                'y-')

    ax.plot(homogeneous_points[0,:],
            homogeneous_points[1,:],
            'r+')

    # get images of the two vanishing points
    vp1 = numpy.cross(homogeneous_lines[0,:], homogeneous_lines[2,:])
    vp2 = numpy.cross(homogeneous_lines[1,:], homogeneous_lines[3,:])

    vp1 = vp1 / vp1[2]
    vp2 = vp2 / vp2[2]

    print('Imaged vanishing point 1 (VP1): {}'.format(vp1))
    print('Imaged vanishing point 2 (VP2): {}'.format(vp2))

    # get the image of the line at infinity
    l_infinity = numpy.cross(vp1, vp2)
    l_infinity = l_infinity / numpy.sqrt((l_infinity**2).sum())

    if l_infinity[2] < 0:
        l_infinity *= -1

    print('Imaged line at infinity: {}'.format(l_infinity))

    # make rectifying homography
    H = numpy.eye(3)
    H[2,:] = l_infinity

    # determine output region of warping
    output_points = H.dot(homogeneous_points)
    output_points[0,:] /= output_points[2,:]
    output_points[1,:] /= output_points[2,:]

    rect_vp1 = H.dot(vp1)
    rect_vp2 = H.dot(vp2)
    rect_l_infinity = H.dot(l_infinity)

    print()
    print('Rectified VP1: {}'.format(rect_vp1))
    print('Rectified VP2: {}'.format(rect_vp2))
    print('Rectified Line at infinity: {}'.format(rect_l_infinity))

    out_x_min = int(numpy.floor(output_points[0,:].min()))
    out_x_max = int(numpy.ceil(output_points[0,:].max()))
    out_y_min = int(numpy.floor(output_points[1,:].min()))
    out_y_max = int(numpy.ceil(output_points[1,:].max()))

    # warp the image and show it
    out_im = cv2.warpPerspective(im, H, (im.shape[1], im.shape[0]))
    out_im = out_im[out_y_min:out_y_max+1,
                    out_x_min:out_x_max+1]

    f2 = pyplot.figure()
    ax2 = f2.add_subplot(111)
    ax2.imshow(out_im)
    pyplot.show()


def main():
    parser = argparse.ArgumentParser(
        description=('Load an image, manually click corner points, and '
                     'automatically rectify it.'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('image_filename',
                        action='store',
                        help='The filename of the image to load.')

    parser.add_argument('--bgr',
                        action='store_true',
                        default=False,
                        help='Is the image BGR instead of RGB?')

    args = parser.parse_args()

    execute(args.image_filename, args.bgr)


if __name__ == "__main__":
    main()
