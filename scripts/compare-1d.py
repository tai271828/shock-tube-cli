#!/usr/bin/env python
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

time_total = 0.2
mesh_points_number = 500


analytic_solver = solver_analytic.Solver()
analytic_solution = analytic_solver.get_analytic_solution()

shocktubecalc_sodtube = sod.solve(left_state=(state_left_p, state_left_rho, state_left_u),
                                  right_state=(state_right_p, state_right_rho, state_right_u),
                                  geometry=(tube_left_x, tube_right_x, tube_radius),
                                  t=time_total,
                                  gamma=1.4,
                                  npts=mesh_points_number)

print('Positions:')
for desc, vals in shocktubecalc_sodtube[0].items():
    print('{0:10} : {1}'.format(desc, vals))

print('States:')
for desc, vals in shocktubecalc_sodtube[1].items():
    print('{0:10} : {1}'.format(desc, vals))


