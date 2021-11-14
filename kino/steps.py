import numpy as np

# from loguru import logger

from kino.math import convolve_with_gaussian
from kino.geometry import Trajectory


class Paw:
    def __init__(
        self, name: str, trajectory: Trajectory, com: Trajectory,
    ):
        self.name = name
        self.trajectory = trajectory
        self.com = com

        self.normalized_speed = convolve_with_gaussian(
            trajectory.speed - convolve_with_gaussian(com.speed),
            kernel_width=6,
        )

        self.speed_th = -8 if "hl" in name else -5
        self.detect_swing()

    def detect_swing(self):
        """
            Detects when the paws is in a swing movement
            compared to when it's stationary (stance phase)

            The normalized_speed trace is centered to be 0 when it matches
            the animal's speed (more or less). So when it's negative
            that means that the paw is stationary.
        """
        # create an array of 1s for swing 0s for stance
        self.is_swing = np.zeros_like(self.normalized_speed)
        self.is_swing[self.normalized_speed > self.speed_th] = 1

        # get onset/offset of swing phase
        starts = np.where(np.diff(self.is_swing) > 0)[0]
        ends = np.where(np.diff(self.is_swing) < 0)[0] + 1
        ends = [end for end in ends if end > starts[0]]

        # check that steps meet min/max duration and distance requirements
        self.swings_start, self.swings_end, self.swings_duration = [], [], []
        for start, end in zip(starts, ends):
            if self.com.speed[start] < 20:
                continue

            dur = (end - start) / self.trajectory.fps
            # dist = (
            #     np.sum(self.trajectory.speed[start:end]) / self.trajectory.fps
            # )

            # if dur > 0.01 and dur < 0.5 and dist > 2 and dist < 10:
            #     if len(self.swings_end) and start < self.swings_end[-1]:
            #         continue  # start before previous step ends
            self.swings_start.append(start)
            self.swings_end.append(end)
            self.swings_duration.append(dur)
        # logger.debug(
        #     f'Paw "{self.name}" detect {len(starts)} potential steps, kept {len(self.swings_start)}'
        # )
