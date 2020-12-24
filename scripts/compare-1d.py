#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from sodtube1d import solver_analytic
from shocktubecalc import sod


tube_radius = 0.5
tube_length = 1.0
tube_left_x = 0.0
tube_right_x = tube_left_x + tube_length
tube_x_coordinate_shift = 0.5

state_left_rho = 1.0
state_left_u = 0.0
state_left_p = 1.0
state_right_rho = 0.125
state_right_u = 0.0
state_right_p = 0.1

time_moment = 0.2
mesh_points_number = 50


def plot_solution(values_base, values_target, time_moment=None):
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    if time_moment:
        fig.suptitle(f"Time (sec): {time_moment}")

    # plot target
    plt.subplot(231, title="Pressure (target)")
    plt.scatter(values_target["x"], values_target["p"], s=10, c="b", marker="s")
    plt.axis([0, 1, 0, 1.1])

    plt.subplot(232, title="Density (target)")
    plt.scatter(values_target["x"], values_target["rho"], s=10, c="b", marker="s")
    plt.axis([0, 1, 0, 1.1])

    plt.subplot(233, title="Velocity (target)")
    plt.scatter(values_target["x"], values_target["u"], s=10, c="b", marker="s")
    plt.axis([0, 1, 0, 1.1])

    # plot base
    plt.subplot(234, title="Pressure (base)")
    plt.scatter(values_base["x"], values_base["p"], s=10, c="g", marker="8")
    plt.xlabel("x")
    plt.axis([0, 1, 0, 1.1])

    plt.subplot(235, title="Density (base)")
    plt.scatter(values_base["x"], values_base["rho"], s=10, c="g", marker="8")
    plt.xlabel("x")
    plt.axis([0, 1, 0, 1.1])

    plt.subplot(236, title="Velocity (base)")
    plt.scatter(values_base["x"], values_base["u"], s=10, c="g", marker="8")
    plt.xlabel("x")
    plt.axis([0, 1, 0, 1.1])

    plt.show()


# generate the result from shocktube1d package
mesh_x_array = np.linspace(
    tube_left_x - tube_x_coordinate_shift,
    tube_right_x - tube_x_coordinate_shift,
    mesh_points_number,
)
analytic_solver = solver_analytic.Solver()
analytic_solution = analytic_solver.get_analytic_solution(mesh_x_array, t=time_moment)
# convert to shocktubecalc compatible format
ao_rho_list = []
ao_u_list = []
ao_p_list = []

for solution_point in analytic_solution:
    ao_rho_list.append(solution_point[1])
    ao_u_list.append(solution_point[2])
    ao_p_list.append(solution_point[3])

mesh_x_array_on_shocktubecalc = np.linspace(
    tube_left_x,
    tube_right_x,
    mesh_points_number,
)
shocktube1d_sodtube = [
    {"Positions": "NA"},
    {"States": "NA"},
    {
        "x": mesh_x_array_on_shocktubecalc,
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
shocktubecalc_sodtube_values = shocktubecalc_sodtube[2]
plot_solution(
    shocktube1d_sodtube_values, shocktubecalc_sodtube_values, time_moment=time_moment
)
