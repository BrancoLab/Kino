import numpy as np

from kino.geometry import Trajectory


def test_trajectory_long_lat_acceleration():
    x = np.linspace(0, 3 * np.pi, 200)
    y = np.cos(x)

    traj = Trajectory(x, y, fps=60, smoothing_window=1)

    # check that longitudinal/normal accelerations can recover the averall acceleration
    # the abs is there because normally acceleartion is not signed
    delta = traj.acceleration_mag - (
        np.abs(traj.longitudinal_acceleration)
        + np.abs(traj.normal_acceleration)
    )
    if not np.allclose(delta, 0, atol=5e-3):
        raise ValueError(
            "Longitudinal and normal acceleration dont match acceleration magnitude"
        )

    # check that the longitudinal acceleration can be used to recover the speed
    recovered_speed = np.cumsum(traj.longitudinal_acceleration)
    delta = traj.speed - recovered_speed
    if not np.allclose(delta, 0, atol=1):
        raise ValueError(
            "Longitudinal acceleration did not recover the original speed"
        )
