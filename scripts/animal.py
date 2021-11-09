import sys

sys.path.append("./")

from rich import print

from myterial import (
    pink,
    pink_darker,
    blue,
    blue_darker,
    blue_grey_light,
    blue_grey_dark,
    blue_grey_darker,
)

from kino.animal import Animal


animal_data = dict(
    name="Mouse",
    paws=("left_fl", "right_fl", "right_hl", "left_hl"),
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
        left_fl=pink,
        right_fl=blue,
        right_hl=blue_darker,
        left_hl=pink_darker,
        snout=blue_grey_light,
        neck=blue_grey_light,
        body=blue_grey_dark,
        tail_base=blue_grey_darker,
    ),
    skeleton=(
        ("body", "left_fl", blue_darker),
        ("body", "right_fl", blue_darker),
        ("body", "right_hl", blue_darker),
        ("body", "left_hl", blue_darker),
        ("snout", "neck", "k"),
        ("neck", "body", "k"),
        ("body", "tail_base", "k"),
    ),
)


# --------------------------- create animal object --------------------------- #

animal = Animal(animal_data)
print(animal)
