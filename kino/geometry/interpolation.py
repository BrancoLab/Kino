from kino.geometry import Vector


def lerp(x0: float, x1: float, p: float) -> float:
    """
        Interplates linearly between two values such that when p=0
        the interpolated value is x0 and at p=1 it's x1
    """
    return (1 - p) * x0 + p * x1


def interpolate_vector_at_frame(
    vector: Vector, frame: int, p: float
) -> Vector:
    """
        Interpolates a 2D vector between two following frames
    """
    v0 = vector[frame]
    v1 = vector[frame + 1]

    return Vector(lerp(v0.x, v1.x, p), lerp(v0.y, v1.y, p))
