import matplotlib.pyplot as plt
from typing import Union, List

from kino.locomotion import Locomotion
from kino.geometry import Trajectory, AnchoredTrajectory
from kino.animal import Animal
from kino.draw import gliphs
from kino.geometry import interpolation


class DrawBodyPart:
    @classmethod
    def scatter(
        cls,
        bodypart: Trajectory,
        ax: plt.Axes,
        s: int = 25,
        ec: Union[str, List] = [0.2, 0.2, 0.2],
        lw: float = 0.2,
        **kwargs,
    ):
        """
            draws the position of a body parts as scatter dots
        """
        if len(bodypart) == 1:
            gliphs.Dot(
                bodypart.x,
                bodypart.y,
                ax,
                color=bodypart.color,
                s=s,
                ec=ec,
                lw=lw,
                zorder=100,
                **kwargs,
            )
        else:
            gliphs.Dots(
                bodypart.x,
                bodypart.y,
                ax,
                color=bodypart.color,
                s=s,
                ec=ec,
                lw=lw,
                zorder=100,
                **kwargs,
            )


class DrawBone:
    """
        draws a single bone as a directed arrow(s)
    """

    def __init__(self, bone: AnchoredTrajectory, ax: plt.Axes, **kwargs):
        gliphs.Arrow(
            bone.x,
            bone.y,
            bone.vector.angle,
            head_width=0,
            L=bone.vector.magnitude,
            color=bone.color,
            ax=ax,
            **kwargs,
        )


class DrawAnimal:
    """
        Draws an animal by marking:
            - position of the paws
            - position of the center of mass
            - main body axis
            - head axis
    """

    def __init__(self, animal: Animal):
        # TODO draw stuff
        return

    @classmethod
    def draw(cls, animal: Animal, locomotion: Locomotion, ax: plt.Axes):
        """
            Draws animal posture based on locomotion trajectory data
        """
        # scatter the paws
        for paw_name in animal.paws:
            paw = locomotion[paw_name]
            DrawBodyPart.scatter(paw, ax, s=25)

        # mark CoM
        DrawBodyPart.scatter(locomotion["com"], ax, s=25)

        # draw body axis and head
        DrawBone(locomotion.body_axis, ax)
        DrawBone(locomotion.head, ax)

    @classmethod
    def at_frame(
        cls,
        animal: Animal,
        locomotion: Locomotion,
        frame: Union[int, List[int]],
        ax: plt.Axes,
    ):
        """
            Given a Locomotion object with the body posture of an Animal at a 
            frame, it draws the animal (paws and body axis + head).
        """
        if isinstance(frame, int):
            frames = [frame]
        else:
            frames = frame

        for frame in frames:
            locomotion_at_frame = locomotion @ frame
            DrawAnimal.draw(animal, locomotion_at_frame, ax)

    @classmethod
    def at_frame_interpolated(
        cls,
        animal: Animal,
        locomotion: Locomotion,
        frame: int,
        p: float,
        ax: plt.Axes,
    ):
        """
            Draws the posture of an animal at a frame, interpolating with the following frame
        """
        # interpolate locomotion at the selected frame
        locomotion = interpolation.interpolate_at_frame(locomotion, frame, p)

        # draw
        DrawAnimal.draw(animal, locomotion, ax)
