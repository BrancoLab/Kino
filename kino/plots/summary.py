# import matplotlib.pyplot as plt

# from kino.draw import colors
# from kino.animal import Animal


# def draw_locomotion_sequence(animal: Animal):
#     f = plt.figure(figsize=(12, 8))

#     axes = f.subplot_mosaic(
#         """
#             AABBB
#             AACCC
#         """
#     )

#     # plot the trajectory in 2D
#     axes["A"].plot(
#         animal.body.x,
#         animal.body.y,
#         color=animal.body.color,
#         lw=2,
#         label="body",
#     )

#     for paw in animal.paws:
#         axes["A"].plot(
#             animal[paw].x,
#             animal[paw].y,
#             color=animal[paw].color,
#             lw=0.5,
#             label=paw,
#         )

#     # plot body velocities and paws speeds
#     axes["B"].plot(
#         animal.body.time,
#         animal.body.speed,
#         color=colors.velocity,
#         label="body velocity",
#     )
#     axes["C"].plot(
#         animal.body.time,
#         animal.body.thetadot,
#         color=colors.thetadot,
#         label="angular velocity",
#     )

#     axes["A"].legend()
#     axes["A"].set(xlabel="cm", ylabel="cm")

#     axes["B"].legend()
#     axes["B"].set(ylabel="cm/s")
#     axes["C"].legend()
#     axes["C"].set(ylabel="deg/s")
