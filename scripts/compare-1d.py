#!/usr/bin/env python
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sodtube1d import solver_analytic
from shocktubecalc import sod


TUBE_RADIUS = 0.5
TUBE_LENGTH = 1.0
TUBE_LEFT_X = 0.0
TUBE_RIGHT_X = TUBE_LEFT_X + TUBE_LENGTH
TUBE_X_COORDINATE_SHIFT = 0.5

STATE_LEFT_RHO = 1.0
STATE_LEFT_U = 0.0
STATE_LEFT_P = 1.0
STATE_RIGHT_RHO = 0.125
STATE_RIGHT_U = 0.0
STATE_RIGHT_P = 0.1

TIME_STEP_SIZE = 0.01
TIME_TOTAL_ELAPSE = 2.0
MESH_POINTS_NUMBER = 50

DEVIATION_PRECISION = 0.000000001


def get_shocktube1d_values(time_moment):
    mesh_x_array = np.linspace(
        TUBE_LEFT_X - TUBE_X_COORDINATE_SHIFT,
        TUBE_RIGHT_X - TUBE_X_COORDINATE_SHIFT,
        MESH_POINTS_NUMBER,
    )
    analytic_solver = solver_analytic.Solver()
    analytic_solution = analytic_solver.get_analytic_solution(
        mesh_x_array, t=time_moment
    )
    # convert to shocktubecalc compatible format
    ao_rho_list = []
    ao_u_list = []
    ao_p_list = []

    for solution_point in analytic_solution:
        ao_rho_list.append(solution_point[1])
        ao_u_list.append(solution_point[2])
        ao_p_list.append(solution_point[3])

    mesh_x_array_on_shocktubecalc = np.linspace(
        TUBE_LEFT_X,
        TUBE_RIGHT_X,
        MESH_POINTS_NUMBER,
    )
    shocktube1d_values = [
        {"Positions": "NA"},
        {"States": "NA"},
        {
            "x": mesh_x_array_on_shocktubecalc,
            "rho": ao_rho_list,
            "u": ao_u_list,
            "p": ao_p_list,
        },
    ]

    return shocktube1d_values


def get_shocktubecalc_values(time_moment):
    shocktubecalc_values = sod.solve(
        left_state=(STATE_LEFT_P, STATE_LEFT_RHO, STATE_LEFT_U),
        right_state=(STATE_RIGHT_P, STATE_RIGHT_RHO, STATE_RIGHT_U),
        geometry=(TUBE_LEFT_X, TUBE_RIGHT_X, TUBE_RADIUS),
        t=time_moment,
        gamma=1.4,
        npts=MESH_POINTS_NUMBER,
    )

    return shocktubecalc_values


def get_deviation_values(values_base, values_target, ordered_title):
    values_deviation = {"x": values_target["x"]}

    for key in ordered_title:
        values_deviation_derived = []
        for idx_value in range(len(values_target[key])):
            value_deviation = (
                values_target[key][idx_value] - values_base[key][idx_value]
            )
            values_deviation_derived.append(value_deviation)

            if value_deviation > DEVIATION_PRECISION:
                print(
                    f"{key} deviation {value_deviation} at {values_deviation['x'][idx_value]} "
                    f"is larger than {DEVIATION_PRECISION}"
                )

        values_deviation[key] = values_deviation_derived

    return values_deviation


def plot_solution_single_artist(
    artist, titles_ordered, time_moment, type_name, ax_type, values_type, color, marker
):
    key_idx = 0
    for key in titles_ordered:
        ax = ax_type[key_idx]
        subplot = ax.scatter(
            values_type["x"], values_type[key], s=10, c=color, marker=marker
        )
        if type_name == "deviation":
            ax.set(xlim=[0, 1], ylim=[-0.01, 0.01])
        else:
            ax.set(xlim=[0, 1], ylim=[0, 1.1])
        ax.set_title(titles_ordered[key] + f" ({type_name})")
        text_time = plt.text(
            0.1, 0.08, f"Time: {time_moment:.2f}", transform=ax.transAxes
        )

        artist.append(subplot)
        artist.append(text_time)
        key_idx = key_idx + 1

    return artist


def plot_solution_single_frame(
    values_base, values_target, ax_base, ax_target, ax_deviation, moment
):
    artist = []

    title_items = [
        ("p", "Pressure"),
        ("rho", "Density"),
        ("u", "Velocity"),
    ]
    titles_ordered = collections.OrderedDict(title_items)

    values_deviation = get_deviation_values(values_base, values_target, titles_ordered)

    plot_solution_single_artist(
        artist, titles_ordered, moment, "target", ax_target, values_target, "b", "s"
    )
    plot_solution_single_artist(
        artist, titles_ordered, moment, "base", ax_base, values_base, "g", "8"
    )
    plot_solution_single_artist(
        artist,
        titles_ordered,
        moment,
        "deviation",
        ax_deviation,
        values_deviation,
        "r",
        "o",
    )

    return artist


def plot_solution_video_frames(
    time_step, time_total_elapse, ax_base, ax_target, ax_deviation
):
    artist_frames = []
    time_total_steps = int(time_total_elapse / time_step)
    for idx_step in range(0, time_total_steps):
        moment = TIME_STEP_SIZE * idx_step
        # generate the result from shocktube1d package
        shocktube1d_sodtube = get_shocktube1d_values(moment)

        # generate the result from shocktubecalc package
        shocktubecalc_sodtube = get_shocktubecalc_values(moment)

        shocktube1d_sodtube_values = shocktube1d_sodtube[2]
        shocktubecalc_sodtube_values = shocktubecalc_sodtube[2]

        artist_frames.append(
            plot_solution_single_frame(
                shocktube1d_sodtube_values,
                shocktubecalc_sodtube_values,
                ax_base,
                ax_target,
                ax_deviation,
                moment,
            )
        )

    return artist_frames


# Output video
#
# Set up formatting for the movie files
Writer = animation.writers["ffmpeg"]
writer = Writer(fps=15, metadata=dict(artist="Me"), bitrate=1800)
my_dpi = 96
fig4video, (axis_target, axis_base, axis_deviation) = plt.subplots(
    3, 3, figsize=(1600 / my_dpi, 1000 / my_dpi), dpi=my_dpi
)
fig4video.subplots_adjust(hspace=0.4, wspace=0.4)
frame_seq = plot_solution_video_frames(
    TIME_STEP_SIZE, TIME_TOTAL_ELAPSE, axis_base, axis_target, axis_deviation
)

ani = animation.ArtistAnimation(
    fig4video, frame_seq, interval=25, repeat_delay=300, blit=True
)
ani.save("1d-sod-tube.mp4", writer=writer)
