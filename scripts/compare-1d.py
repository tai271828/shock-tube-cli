#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from sodtube1d import solver_analytic
from shocktubecalc import sod


tube_radius = 0.5
tube_length = 1.0
tube_left_x = 0.0
tube_right_x = tube_left_x + tube_length

state_left_rho = 1.0
state_left_u = 0.0
state_left_p = 1.0
state_right_rho = 0.125
state_right_u = 0.0
state_right_p = 0.1

time_moment = 0.2
mesh_points_number = 500


def plot_solution(values, figure_numbers):
    plt.figure(figure_numbers[0])
    plt.plot(values['x'], values['p'], linewidth=1.5, color='b')
    plt.ylabel('pressure')
    plt.xlabel('x')
    plt.axis([0, 1, 0, 1.1])

    plt.figure(figure_numbers[1])
    plt.plot(values['x'], values['rho'], linewidth=1.5, color='r')
    plt.ylabel('density')
    plt.xlabel('x')
    plt.axis([0, 1, 0, 1.1])

    plt.figure(figure_numbers[2])
    plt.plot(values['x'], values['u'], linewidth=1.5, color='g')
    plt.ylabel('velocity')
    plt.xlabel('x')

    plt.show()

# generate the result from shocktube1d package
mesh_x_arr = np.linspace(tube_left_x, tube_right_x, mesh_points_number)
analytic_solver = solver_analytic.Solver()
analytic_solution = analytic_solver.get_analytic_solution(mesh_x_arr, t=time_moment)
# convert to shocktubecalc compatible format
ao_rho_list = []
ao_u_list = []
ao_p_list = []

for solution_point in analytic_solution:
    ao_rho_list.append(solution_point[0])
    ao_u_list.append(solution_point[1])
    ao_p_list.append(solution_point[2])

shocktube1d_sodtube = [
    {"Positions": "NA"},
    {"States": "NA"},
    {
        "x": mesh_x_arr,
        "rho": ao_rho_list,
        "u": ao_u_list,
        "p": ao_p_list,
    },
]


# generate the result from shocktubecalc package
shocktubecalc_sodtube = sod.solve(
    left_state=(state_left_p, state_left_rho, state_left_u),
    right_state=(state_right_p, state_right_rho, state_right_u),
    geometry=(tube_left_x, tube_right_x, tube_radius),
    t=time_moment,
    gamma=1.4,
    npts=mesh_points_number,
)

print("Positions:")
for desc, vals in shocktubecalc_sodtube[0].items():
    print("{0:10} : {1}".format(desc, vals))

print("States:")
for desc, vals in shocktubecalc_sodtube[1].items():
    print("{0:10} : {1}".format(desc, vals))


shocktube1d_sodtube_values = shocktube1d_sodtube[2]
plot_solution(shocktube1d_sodtube_values, [1, 2, 3])

shocktubecalc_sodtube_values = shocktubecalc_sodtube[2]
plot_solution(shocktubecalc_sodtube_values, [4, 5, 6])
