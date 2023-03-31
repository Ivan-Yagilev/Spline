from math import cos, sin, pi
from main import np


def osc_4(x):
    return 10000*cos(10*x) + x*sin(x)/3 - (4/3)*cos(x)


def main_4(x):
    return x*sin(x)/3 - (4/3)*cos(x)


x = np.linspace(0, pi, 1000)
M_osc = max([osc_4(i) for i in x])
print(M_osc)

M_main = max([main_4(i) for i in x])
print(M_main)
