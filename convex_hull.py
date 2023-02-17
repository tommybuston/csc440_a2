import math
import sys
from tkinter import RIGHT
from tkinter.constants import NONE
from typing import List
from typing import Tuple

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]


def y_intercept(p1: Point, p2: Point, x: int) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    return y1 + (x - x1) * slope


def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Given three points a,b,c,
    computes and returns the area defined by the triangle a,b,c.
    Note that this area will be negative if a,b,c represents a clockwise sequence,
    positive if it is counter-clockwise,
    and zero if the points are collinear.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return ((cx - bx) * (by - ay) - (bx - ax) * (cy - by)) / 2


def is_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) < -EPSILON


def is_counter_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a counter-clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) > EPSILON


def collinear(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c are collinear
    (subject to floating-point precision)
    """
    return abs(triangle_area(a, b, c)) <= EPSILON


def clockwise_sort(points: List[Point]):
    """
    Given a list of points, sorts those points in clockwise order about their centroid.
    Note: this function modifies its argument.
    """
    # get mean x coord, mean y coord
    x_mean = sum(p[0] for p in points) / len(points)
    y_mean = sum(p[1] for p in points) / len(points)

    def angle(point: Point):
        return (math.atan2(point[1] - y_mean, point[0] - x_mean) + 2 * math.pi) % (2 * math.pi)

    points.sort(key=angle)
    return


def base_case_hull(points: List[Point]) -> List[Point]:
    """ Base case of the recursive algorithm.
        (The naive method)
    """
    # TODO: You need to implement this function.
    # TODO: HANDLE A POSSIBLE VERTICAL LINE!!!!!
    # clockwise_sort(points)
    if len(points) <=3:
        return points

    hull_points = []
    for idx1, point1 in enumerate(points):
        on_hull = False

        for idx2, point2 in enumerate(points):
            if idx1 == idx2: continue
            good_line = 0
            if point1[0] == point2[0]:
                good_line = check_line_UNdefined(points, point1, point2)
            else:
                good_line = check_line_defined(points, point1, point2)

            if good_line: 
                on_hull = True
                break

        if on_hull:
            hull_points.append(point1)
    clockwise_sort(hull_points)
    return hull_points

def check_line_defined(points, point1, point2):
    above = False
    for i in range(len(points)):
        if collinear(point1, point2, points[i]): continue
        if y_intercept(point1, point2, points[i][0]) > points[i][1]:
            above = True
            break

    good_line = True
    for k in points:
        y_int = y_intercept(point1, point2, k[0])
        if (y_int >= k[1]) and above:
            continue
        elif (y_int <= k[1]) and (not above):
            continue
        else:
            good_line = False
            break
    return good_line

def check_line_UNdefined(points, point1, point2):
    right = False
    x_val = point1[0]
    for i in range(len(points)):
        if collinear(point1, point2, points[i]): continue

        if points[i][0] > x_val:
            right = True
            break

    good_line = True
    for k in points:
        if (k[0] >= x_val) and right :
            continue
        elif (k[0] <= x_val) and (not right):
            continue
        else:
            good_line = False
            break
    return good_line

def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    # TODO: Implement a correct computation of the convex hull
    #  using the divide-and-conquer algorithm
    # TODO: Document your Initialization, Maintenance and Termination invariants.

    if len(points) < 7:
        print("Base Case")
        return base_case_hull(points)

    clockwise_sort(points)
    print(points)
    # points.sort()
    # pseudo_middle = len(points)//2;
    #
    # #TODO: handle the left list being empty
    # while(points[pseudo_middle] == points[pseudo_middle+1]):
    #     pseudo_middle+=1
    #     if pseudo_middle == (len(points)-1):
    #         return base_case_hull(points)
    # print("Midline:", pseudo_middle)
    # side_A = points[0:pseudo_middle]
    # side_B = points[pseudo_middle:]
    #
    # hull_A = compute_hull(side_A)
    # hull_B = compute_hull(side_B)
    #
    # ######## MERGE ########
    # i = hull_A.index(max(hull_A))
    # j = hull_B.index(min(hull_B))
    # k = i
    # l = j
    #
    # midline = (hull_A[i][0]+hull_B[j][0])//2
    # up_tan=[hull_A[i], hull_B[j]]
    # ##### Top Tangent #####
    # while(True):
    #     print("Stuck1")
    #     y_int = y_intercept(up_tan[0], up_tan[1], int(midline))
    #
    #     if y_intercept(hull_A[(i-1)%len(hull_A)], hull_B[j], int(midline)) > y_int:
    #         i = (i-1)%len(hull_A)
    #         up_tan[0] = hull_A[i]
    #     elif y_intercept(hull_A[i], hull_B[(j+1)%len(hull_B)], int(midline)) > y_int:
    #         j = (j+1)%len(hull_B)
    #         up_tan[1] = hull_B[j]
    #     else:
    #         break
    #
    # ##### Bottom Tangent #####
    # low_tan=[hull_A[k], hull_B[l]]
    # while(True):
    #     print("Stuck2")
    #     y_int = y_intercept(low_tan[0], low_tan[1], int(midline))
    #
    #     if y_intercept(hull_A[(k+1)%len(hull_A)], hull_B[l], int(midline)) < y_int:
    #         k = (k+1)%len(hull_A)
    #         low_tan[0] = hull_A[k]
    #
    #     elif y_intercept(hull_A[k], hull_B[(l-1)%len(hull_B)], int(midline)) < y_int:
    #         l = (l-1)%len(hull_B)
    #         low_tan[1] = hull_B[j]
    #     else:
    #         break
    #
    # hull = []
    # counter = hull_A.index(low_tan[0])
    # while(True):
    #     print("second")
    #     hull.append(hull_A[counter%len(hull_A)])
    #     if hull_A[counter%len(hull_A)] == up_tan[0]:
    #         break
    #     counter += 1
    #
    # counter = hull_B.index(up_tan[1])
    # while(True):
    #     print("Third")
    #     hull.append(hull_B[counter%len(hull_B)])
    #     if hull_B[counter%len(hull_B)] == low_tan[1]:
    #         break
    #     counter += 1
    #  
    # print("Returned")
    # clockwise_sort(hull)
    # return hull        
    return points
