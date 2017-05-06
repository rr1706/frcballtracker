import numpy as np


def one2three(img: np.ndarray, gray: np.ndarray):
    """
    Rearrange single channel image as 3-channel image, for display purposes.
    :param img: Original image, for shape information.
    :param gray: Single-channel image to copy.
    :return: 3-channel image.
    """
    img2 = np.zeros_like(img)
    img2[:, :, 0] = gray
    img2[:, :, 1] = gray
    img2[:, :, 2] = gray
    return img2


def circle_perimeter_points(center: tuple, radius: float, test_points: int = 100, tolerance_ratio: float = 0.2):
    """
    Generate points that would exist on the perimeter of a circle.
    :param center: Center of circle (x, y)
    :param radius: Radius of circle
    :param test_points: Amount of points to generate
    :param tolerance_ratio: Amount each generated point should be inset, as a percentage of radius
    """
    tolerance = tolerance_ratio * radius
    for i in np.linspace(0, 2 * np.pi, test_points):
        x = (radius-tolerance) * np.cos(i) + center[0]
        y = (radius-tolerance) * np.sin(i) + center[1]
        yield (x, y)