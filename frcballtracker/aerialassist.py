import functools

import cv2
import numpy as np

from frcballtracker.util import one2three, circle_perimeter_points

# Test footage
video = 'FRC Team 2090 Raw GoPro Footage 2014-nmvbX3W5-Mo.mp4'

# Configuration
ctr_sides_min = 5  # Circle has more than these amount of sides
ctr_area_min = 150  # Minimum contour area
ctr_ratio_min = 0.45  # Minimum contour-to-circle ratio
cir_perimeter_ratio = 0.7  # Minimum contour perimeter points to circle perimeter points

# Variables
se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))


def circle_area_test(contour):
    """
    Test contour based on its area vs. min circle area.
    :param contour: Contour to test
    :return: True if ratio is greater than minimum
    """
    polygon = cv2.approxPolyDP(contour, epsilon=2, closed=True)
    (x, y), radius = cv2.minEnclosingCircle(polygon)
    circle_area = np.math.pi * radius ** 2
    contour_area = cv2.contourArea(contour)
    ratio = contour_area / circle_area
    return ctr_ratio_min < ratio


def circle_perimeter_test(contour):
    """
    Test contour based on points that should exist on the perimeter of the circle, vs. what actually exists.
    :param contour: Contour to test
    :return: True if contour points ratio passes minimum
    """
    TEST_POINTS = 100
    passed = 0
    center, radius = cv2.minEnclosingCircle(contour)
    for pt in circle_perimeter_points(center, radius, TEST_POINTS):
        dist = cv2.pointPolygonTest(contour, pt, measureDist=False)
        if dist >= 0:
            passed += 1

    return passed / TEST_POINTS > cir_perimeter_ratio


contour_filters = {
    'area': lambda contour: cv2.contourArea(contour) > ctr_area_min,
    'sides': lambda contour: cv2.approxPolyDP(contour, epsilon=2, closed=True).shape[0] >= ctr_sides_min,
    'anti-bumper': circle_area_test,
    'circle': circle_perimeter_test,
}


def find_largest(contours: list):
    # Remove contours that do not pass tests
    for name, f in contour_filters.items():
        contours = filter(f, contours)
    # Return the largest remaining contour
    return functools.reduce(lambda c1, c2: c1 if cv2.contourArea(c1) > cv2.contourArea(c2) else c2,
                            contours, np.ndarray(shape=(0, 1, 2), dtype=np.int))


def process_image(image: np.ndarray):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # HSV thresholds for Red ball
    upper_thresh = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
    lower_thresh = cv2.inRange(hsv, (160, 100, 100), (179, 255, 255))
    thresh = cv2.addWeighted(upper_thresh, 1, lower_thresh, 1, 0)
    # Remove noise and connections to background
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, se2)

    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    contour = find_largest(contours)
    if contour.shape[0] > 0:
        # Draw resulting contour
        cv2.drawContours(image, [contour], 0, (0, 255, 0))
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(image, center=center, radius=radius, color=(255, 0, 0))

    return np.hstack([image, one2three(image, mask)])
