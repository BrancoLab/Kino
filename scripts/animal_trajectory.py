# import sys

# sys.path.append("./")

# import pandas as pd
# import matplotlib.pyplot as plt

# from myterial import (
#     pink,
#     pink_darker,
#     blue,
#     blue_darker,
#     blue_grey_light,
#     blue_grey_dark,
#     blue_grey_darker,
# )

# from kino.animal import Animal
# from kino.geometry import Trajectory
# from kino.draw import draw

# # --------------------------- create animal object --------------------------- #
# animal_data = dict(
#     name="Mouse",
#     bodyparts=(
#         "left_fl",
#         "right_fl",
#         "body",
#         "right_hl",
#         "left_hl",
#         "snout",
#         "neck",
#         "tail_base",
#     ),
#     colors=dict(
#         left_fl=pink,
#         right_fl=blue,
#         right_hl=blue_darker,
#         left_hl=pink_darker,
#         snout=blue_grey_light,
#         neck=blue_grey_light,
#         body=blue_grey_dark,
#         tail_base=blue_grey_darker,
#     ),
#     skeleton=(
#         ("left_fl", "body", blue_darker),
#         ("right_fl", "body", blue_darker),
#         ("right_hl", "body", blue_darker),
#         ("left_hl", "body", blue_darker),
#     ),
# )

# animal = Animal(animal_data)

# # -------------------- get tracking for each body part -------------------- #
# tracking = pd.read_hdf("scripts/example_tracking.h5")

# for bp in animal_data["bodyparts"]:
#     animal[bp].add_tracking(tracking[f"{bp}_x"], tracking[f"{bp}_y"])

# # ----------------------------------- plot ----------------------------------- #

# draw(animal.left_fl.tracking)
# draw(animal.right_fl.tracking)
# draw(animal.left_hl.tracking)
# draw(animal.right_hl.tracking)
# draw(animal.body.tracking, lw=2)

# # draw(animal.at(0))


# plt.show()
