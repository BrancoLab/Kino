import numpy as np
from typing import List, Tuple
from scipy import stats
import math


def pi_2_pi(theta: float) -> float:
    while theta > math.pi:
        theta -= 2.0 * math.pi

    while theta < -math.pi:
        theta += 2.0 * math.pi

    return theta


def mod2pi(theta: float) -> float:
    return theta - 2.0 * math.pi * math.floor(theta / math.pi / 2.0)


def resample_linear_1d(original: np.ndarray, target_length: int) -> np.ndarray:
    """
        Similar to scipy resample for 1D arrays, but with no aberration, see:
            https://stackoverflow.com/questions/20322079/downsample-a-1d-numpy-array
    """
    original = np.array(original, dtype=np.float)
    index_arr = np.linspace(
        0, len(original) - 1, num=target_length, dtype=np.float
    )
    index_floor = np.array(index_arr, dtype=np.int)  # Round down
    index_ceil = index_floor + 1
    index_rem = index_arr - index_floor  # Remain

    val1 = original[index_floor]
    val2 = original[index_ceil % len(original)]
    interp = val1 * (1.0 - index_rem) + val2 * index_rem
    assert len(interp) == target_length
    return interp


def register_in_time(
    arrays: List[np.ndarray], n_samples: int = None
) -> List[np.ndarray]:
    """
        Given a list of 1d numpy arrays of different length,
        this function returns an array of shape (n_samples, n_trials) so
        that each trial has the same number of samples and can thus be averaged
        nicely
    """
    n_samples = n_samples or np.min([len(x) for x in arrays])
    return [resample_linear_1d(x, n_samples) for x in arrays]


def mean_and_std(arrays: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
        Given a list of 1D arrays of same length, returns the mean
        and std arrays
    """
    X = np.vstack(arrays)
    return np.mean(X, 0), np.mean(X, 1)


def derivative(X: np.ndarray, axis: int = 0, order: int = 1) -> np.ndarray:
    """"
        Takes the derivative of an array X along a given axis
        Arguments:
            X: np.array with data
            axis: int. Axis along which the derivative is to be computed
            order: int. Derivative order
    """

    return np.diff(X, n=order, axis=axis, prepend=0)


def angular_derivative(angles: np.ndarray) -> np.ndarray:
    """
        Takes the deriative of an angular variable (in degrees)
    """
    # convert to radians and take derivative
    rad = np.unwrap(np.deg2rad(angles))
    diff = derivative(rad)
    return np.rad2deg(diff)


def convolve_with_gaussian(
    data: np.ndarray, kernel_width: int = 21
) -> np.ndarray:
    """
        Convolves a 1D array with a gaussian kernel of given width
    """
    # create kernel and normalize area under curve
    norm = stats.norm(0, kernel_width)
    X = np.linspace(norm.ppf(0.0001), norm.ppf(0.9999), kernel_width)

    _kernel = norm.pdf(X)
    kernel = _kernel / np.sum(_kernel)

    return np.convolve(data, kernel, mode="same")


def smooth(data: np.ndarray, window: int = 5) -> np.ndarray:
    """
        Smooth a 1D numpy array by binning the values and taking
        the mean for each bin.
    """
    T = len(data)
    means = []
    for t in np.arange(0, T):
        t_0 = t - window if t > window else 0
        t_1 = t + window if T - t > window else T

        means.append(np.mean(data[t_0:t_1]))
    return np.array(means)
