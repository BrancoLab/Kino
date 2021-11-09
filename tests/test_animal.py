import pandas as pd

from kino.animal import Animal
from kino.animal.bodypart import BodyPart
from kino.animal.bone import Bone
from kino.draw import draw

tracking = pd.read_hdf("scripts/example_tracking.h5")


animal_data = dict(
    name="Mouse",
    bodyparts=(
        "left_fl",
        "right_fl",
        "body",
        "right_hl",
        "left_hl",
        "snout",
        "neck",
        "tail_base",
    ),
    colors=dict(
        left_fl="k",
        right_fl="k",
        right_hl="k",
        left_hl="k",
        snout="k",
        neck="k",
        body="k",
        tail_base="k",
    ),
    skeleton=(
        ("body", "left_fl", "r"),
        ("body", "right_fl", "r"),
        ("body", "right_hl", "r"),
        ("body", "left_hl", "r"),
    ),
)


def test_animal_creation():

    animal = Animal(animal_data, tracking, fps=60)
    print(animal)

    # check body parts work correctly
    print(animal.body)
    assert isinstance(animal.body, BodyPart)
    assert isinstance(animal.bones[0], Bone)

    assert (
        len(animal.bodyparts)
        == len(animal.bodyparts_names)
        == len(animal.bodyparts)
    )
    assert len(animal.bones) == len(animal_data["skeleton"])

    bone = animal.get_bone(animal.body, animal.left_fl)
    assert isinstance(bone, Bone)

    draw(animal)

    # get animal tracking at a frame
    at_frame = animal.at(10)

    assert isinstance(at_frame.body.x, float)
    assert isinstance(at_frame.bones[0].bp1.x, float)
