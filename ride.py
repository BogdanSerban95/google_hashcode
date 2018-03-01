from math import fabs
from point import Point


class Ride(object):
    def __init__(self, ride_string):
        split_string = ride_string.split(' ')
        self.start_point = Point(int(split_string[0]), int(split_string[1]))
        self.end_point = Point(int(split_string[2]), int(split_string[3]))
        self.earliest_start = int(split_string[4])
        self.latest_finish = int(split_string[5])
        self.length = fabs(self.start_point.x - self.end_point.x) + fabs(self.start_point.y - self.end_point.y)
