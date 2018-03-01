from ride import Ride


class Solver(object):
    def __init__(self, input_file):
        self.R, self.C, self.F, self.N, self.B, self.T, self.rides = self.load_problem(input_file)

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
                rides.append(Ride(lines[i]))

            return R, C, F, N, B, T, rides

