import numpy as np
import csv

def gen_thrust_curve(file_name):
    f15ThrustCurve = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in csv_reader:
            if first_line:
                first_line = False
                continue
            f15ThrustCurve.append(row)
    return f15ThrustCurve


def create_thrust(currentThrust):
    pass
