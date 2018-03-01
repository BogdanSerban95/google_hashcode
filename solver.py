from ride import Ride
from vehicle import Vehicle
import numpy as np
import utils


class Solver(object):
    def __init__(self, input_file):
        self.file_name = input_file
        self.R, self.C, self.F, self.N, self.B, self.T, self.rides = self.load_problem(input_file)
        self.vehicles = np.array([Vehicle() for i in range(self.F)])
        self.satisfied_vehicles_count = 0

    def solve_problem(self):
        while self.satisfied_vehicles_count <= self.F and len(self.rides) != 0:
            for vehicle in self.vehicles:
                ret = self.get_best_ride(vehicle)
                if ret is not None:
                    vehicle.add_ride(ret)
        self.print_results()

    def print_results(self):
        out_file = self.file_name.split('.')[0] + '.out'
        with open(out_file, 'w') as output_file:
            for vehicle in self.vehicles:
                res = str(len(vehicle.rides)) + ' '
                for ride in vehicle.rides:
                    res += str(ride.idx) + ' '
                output_file.write(res + '\n')

    def get_best_ride(self, vehicle):
        las_position = vehicle.get_last_position()

        smallest_dist = 200000
        winners = []
        for ride in self.rides:
            dist = utils.point_dist(las_position, ride.start_point)
            if dist < smallest_dist:
                winners = [ride]
                smallest_dist = dist
            elif dist == smallest_dist:
                winners.append(ride)
        if len(winners) == 0:
            self.satisfied_vehicles_count += 1
            return None

        max_length = 0
        length_winners = []
        for ride in winners:
            if ride.length + vehicle.ride_distance <= ride.latest_finish:
                if ride.length > max_length:
                    length_winners = [ride]
                    max_length = ride.length
                elif ride.length == max_length:
                    length_winners.append(ride)
        if len(length_winners) == 0:
            self.satisfied_vehicles_count += 1
            return None

        min_start = 200000
        start_winners = []
        for ride in length_winners:
            if ride.length + vehicle.ride_distance <= ride.latest_finish:
                if ride.earliest_start < min_start:
                    start_winners = [ride]
                    min_start = ride.earliest_start
                elif ride.earliest_start == min_start:
                    start_winners.append(ride)
        if len(start_winners) == 0:
            self.satisfied_vehicles_count += 1
            return None

        min_finish = 200000
        finish_winners = []
        for ride in start_winners:
            if ride.length + vehicle.ride_distance <= ride.latest_finish:
                if min_finish >= ride.latest_finish:
                    finish_winners = [ride]
                    min_finish = ride.latest_finish
                elif ride.latest_finish == min_finish:
                    finish_winners.append(ride)

        if len(finish_winners):
            winner = finish_winners[0]
            self.rides.remove(winner)
            return winner
        self.satisfied_vehicles_count += 1
        return None

    def load_problem(self, file_name):
        with open(file_name, 'r') as input_file:
            lines = input_file.readlines()
            split_line = lines[0].split(' ')
            R = int(split_line[0])
            C = int(split_line[1])
            F = int(split_line[2])
            N = int(split_line[3])
            B = int(split_line[4])
            T = int(split_line[5])
            rides = []

            for i in range(1, len(lines)):
                rides.append(Ride(i - 1, lines[i]))

            return R, C, F, N, B, T, rides
