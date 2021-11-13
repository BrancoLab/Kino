import matplotlib.cm as cm_mpl
import numpy as np
from typing import Union, List, Optional
import typing

from myterial import blue, pink, salmon, teal, teal_darker


velocity = blue
acceleration = pink
normal = salmon
thetadot = teal
thetadotdot = teal_darker


@typing.no_type_check
def map_color(
    value: Union[float, List, np.ndarray],
    name: str = "jet",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
) -> Union[str, List]:
    """Map a real value in range [vmin, vmax] to a (r,g,b) color scale.
    :param value: scalar value to transform into a color
    :type value: float, list
    :param name: color map name (Default value = "jet")
    :type name: str, matplotlib.colors.LinearSegmentedColorMap
    :param vmin:  (Default value = None)
    :param vmax:  (Default value = None)
    :returns: return: (r,g,b) color, or a list of (r,g,b) colors.
    """

    def map_value(value: float, mp):
        value -= vmin
        value /= vmax - vmin
        if value > 0.999:
            value = 0.999
        elif value < 0:
            value = 0
        return mp(value)[0:3]

    mp = cm_mpl.get_cmap(name=name)

    if not isinstance(value, (np.ndarray, list)):
        return map_value(value, mp)
    else:
        vmin = vmin or np.min(value)
        vmax = vmax or np.max(value)
        return [map_value(val, mp) for val in value]
