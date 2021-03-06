# MIT 6.034 Lab 0: Getting Started
# Written by jb16, jmn, dxh, and past 6.034 staff

from point_api import Point

#### Multiple Choice ###########################################################

# These are multiple choice questions. You answer by replacing
# the symbol 'None' with a letter (or True or False), corresponding 
# to your answer.

# True or False: Our code supports both Python 2 and Python 3
# Fill in your answer in the next line of code (True or False):
ANSWER_1 = False

# What version(s) of Python do we *recommend* for this course?
#   A. Python v2.3
#   B. Python V2.5 through v2.7
#   C. Python v3.2 or v3.3
#   D. Python v3.4 or higher
# Fill in your answer in the next line of code ("A", "B", "C", or "D"):
ANSWER_2 = "D"


################################################################################
# Note: Each function we require you to fill in has brief documentation        # 
# describing what the function should input and output. For more detailed      # 
# instructions, check out the lab 0 wiki page!                                 #
################################################################################


#### Warmup ####################################################################

def is_even(x):
    """If x is even, returns True; otherwise returns False"""
    if x % 2 == 0:
        return True
    else:
        return False


def decrement(x):
    """Given a number x, returns x - 1 unless that would be less than
    zero, in which case returns 0."""
    if x <= 0:
        return 0
    else:
        return x - 1


def cube(x):
    """Given a number x, returns its cube (x^3)"""
    return x ** 3


#### Iteration #################################################################

def is_prime(x):
    """Given a number x, returns True if it is prime; otherwise returns False"""
    if x == 2 or x == 3: return True
    if x < 2 or x % 2 == 0: return False
    for i in range(3, int(x ** 0.5) + 1, 2):
        if x % i == 0:
            return False
    return True


def primes_up_to(x):
    """Given a number x, returns an in-order list of all primes up to and including x"""
    num = []
    if x <= 1:
        return num
    for i in range(2, int(x) + 1):
        if is_prime(i):
            num.append(i)
    return num


#### Recursion #################################################################

def fibonacci(n):
    """Given a positive int n, uses recursion to return the nth Fibonacci number."""
    if n < 0:
        raise ValueError("fibonacci: input must not be negative")
    if n == 0:
        return 0
    a = 0
    b = 1
    if n <= 2:
        return 1
    else:
        for i in range(2, n + 1):
            c = a + b
            a = b
            b = c
        return b


def expression_depth(expr):
    """Given an expression expressed as Python lists, uses recursion to return
    the depth of the expression, where depth is defined by the maximum number of
    nested operations."""
    if not isinstance(expr, list):
        return 0
    return max(map(expression_depth, expr)) + 1


#### Built-in data types #######################################################

def remove_from_string(s, letters):
    """Given an original string and a string of letters, returns a new string
    which is the same as the old one except all occurrences of those letters
    have been removed from it."""
    for c in letters:
        s = s.replace(c, "")
    return s


def compute_string_properties(string):
    """Given a string of lowercase letters, returns a tuple containing the
    following three elements:
        0. The length of the string
        1. A list of all the characters in the string (including duplicates, if
           any), sorted in REVERSE alphabetical order
        2. The number of distinct characters in the string (hint: use a set)
    """
    return len(string), list(''.join(sorted(string, reverse=True))), len(set(string))


def tally_letters(string):
    """Given a string of lowercase letters, returns a dictionary mapping each
    letter to the number of times it occurs in the string."""
    r = {}
    for c in string:
        try:
            r[c] = r[c] + 1
        except:
            r[c] = 1
    return r


#### Functions that return functions ###########################################

def create_multiplier_function(m):
    """Given a multiplier m, returns a function that multiplies its input by m."""

    def multiplier(x):
        return m * x

    return multiplier


def create_length_comparer_function(check_equal):
    """Returns a function that takes as input two lists. If check_equal == True,
    this function will check if the lists are of equal lengths. If
    check_equal == False, this function will check if the lists are of different
    lengths."""
    if check_equal:
        def return_func(list1, list2):
            return len(list1) == len(list2)

        return return_func
    else:
        def return_func(list1, list2):
            return len(list1) != len(list2)

        return return_func


#### Objects and APIs: Copying and modifying objects ############################

def sum_of_coordinates(point):
    """Given a 2D point (represented as a Point object), returns the sum
    of its X- and Y-coordinates."""
    return point.getX() + point.getY()


def get_neighbors(point):
    """Given a 2D point (represented as a Point object), returns a list of the
    four points that neighbor it in the four coordinate directions. Uses the
    "copy" method to avoid modifying the original point."""
    return [point.copy().setX(point.getX() + 1).setY(point.getY()),
            point.copy().setX(point.getX()).setY(point.getY() + 1),
            point.copy().setX(point.getX() - 1).setY(point.getY()),
            point.copy().setX(point.getX()).setY(point.getY() - 1)]


#### Using the "key" argument ##################################################

def sort_points_by_Y(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "sorted"
    with the "key" argument to create and return a list of the SAME (not copied)
    points sorted in decreasing order based on their Y coordinates, without
    modifying the original list."""
    return sorted(list_of_points, key=lambda point: point.getY(), reverse=True)


def furthest_right_point(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "max" with
    the "key" argument to return the point that is furthest to the right (that
    is, the point with the largest X coordinate)."""
    return max(list_of_points, key=lambda point: point.getX())