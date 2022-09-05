import numpy as np

from matplotlib.path import Path
from matplotlib.patches import FancyBboxPatch, BoxStyle

c = (4/3)*np.tan(np.pi/8)


vertices = {}
codes = {}

vertices['padlock'] = [
    (1., 0.),
    (1.5, 0.), (2., 0.2),(2., 0.8),
    (2., 0.9), (2., 1.6), (1.7, 1.6),
    (1.2, 1.6), (1.6, 1.3), (1., 1.3),
    (0.4, 1.3), (0.8, 1.6), (0.3, 1.6),
    (0., 1.6), (0., 0.9), (0., 0.8),
    (0., 0.2), (0.5, 0.), (1., 0.),

    (1.05, 0.5),
    (0.95, 0.5),
    (0.95, 0.7),
    (0.8, 0.8), (0.9, 0.95), (1., 0.95),
    (1.1, 0.95), (1.2, 0.8), (1.05, 0.7),
    (1.05, 0.5),

    (0., 0.),
]

codes['padlock'] = [
    Path.MOVETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,

    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.CLOSEPOLY
]

vertices['shackle'] = [
    (1.75, 1.5),
    (1.75, 1.7),
    (1.75, 2.15), (1.5, 2.5), (1., 2.5),
    (0.5, 2.5), (0.25, 2.15), (0.25, 1.7),
    (0.25, 1.5),
    (0.5, 1.5),
    (0.5, 1.9), (0.5, 2.25), (1., 2.25),
    (1.5, 2.25), (1.5, 1.8), (1.5, 1.5),
    (1.5, 1.5),
    (1.75, 1.5),
    (0., 0.)
]

codes['shackle'] = [
    Path.MOVETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY
]

rotation_center = np.array([0.375, 1.5])
rotation_matrix = np.array([[np.cos(np.pi / 8), -np.sin(np.pi / 8)],
                            [np.sin(np.pi / 8), np.cos(np.pi / 8)]])
vertices['shackle-open'] = rotation_center + np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices['shackle'] - rotation_center))
codes['shackle-open'] = codes['shackle']


def _half_circle_points(start_point, radius, angle):
    c = (4/3)*np.tan(np.pi/8)

    start_point = np.array(start_point)
    circle_x = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))])
    circle_y = np.array([-np.sin(np.radians(angle)), np.cos(np.radians(angle))])
    circle_center =start_point + radius*circle_x
    top_point = circle_center + radius*circle_y
    end_point = circle_center + radius*circle_x

    circle_points = []
    circle_points += [start_point + c*radius*circle_y]
    circle_points += [top_point - c*radius*circle_x]
    circle_points += [top_point]
    circle_points += [top_point + c*radius*circle_x]
    circle_points += [end_point + c*radius*circle_y]
    circle_points += [end_point]

    return circle_points


def _card_points(start_point=[0, 0], aspect_ratio=1, radius=0.1):
    h = 1/aspect_ratio

    start_point = np.array(start_point)
    card_points = np.array([
        (radius, 0),
        (1 - radius, 0),
        (1 - c*radius, 0), (1, c*radius), (1, radius),
        (1, h - radius),
        (1, h - c*radius), (1 - c*radius, h), (1 - radius, h),
        (radius, h),
        (c*radius, h), (0, h - c*radius), (0, h - radius),
        (0, radius),
        (0, c*radius), (c*radius, 0), (radius, 0),
        (0, 0)
    ]) + start_point

    return card_points


def _card_side_points(start_point=[0, 0], aspect_ratio=1, radius=0.1, margin=0.2):
    h = 1/aspect_ratio

    start_point = np.array(start_point)
    card_side_points = np.array([
        (radius, 0),
        (margin, 0),
        (margin, h),
        (radius, h),
        (c*radius, h), (0, h - c*radius), (0, h - radius),
        (0, radius),
        (0, c*radius), (c*radius, 0), (radius, 0),
        (0, 0)
    ]) + start_point

    return card_side_points


vertices['card'] = _card_points()

codes['card'] = [
    Path.MOVETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CLOSEPOLY
]

vertices['card-side'] = _card_side_points()

codes['card-side'] = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CLOSEPOLY
]


vertices['plate'] = [
    (0, 0.5),
    (0, 0.5 - c*0.5), (0.5 - c*0.5, 0), (0.5, 0),
    (0.5 + c*0.5, 0), (1, 0.5 - c*0.5), (1, 0.5),
    (1, 0.5 + c*0.5), (0.5 + c*0.5, 1), (0.5, 1),
    (0.5 - c*0.5, 1), (0, 0.5 + c*0.5), (0, 0.5),
    (0.1, 0.55),
    (0.1, 0.55 + c*0.35), (0.5 - c*0.4, 0.9), (0.5, 0.9),
    (0.5 + c*0.4, 0.9), (0.9, 0.55 + c*0.35), (0.9, 0.55),
    (0.9, 0.55 - c*0.35), (0.5 + c*0.4, 0.2), (0.5, 0.2),
    (0.5 - c*0.4, 0.2), (0.1, 0.55 - c*0.35), (0.1, 0.55),
    (0, 0)
]

codes['plate'] = [
    Path.MOVETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.MOVETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CLOSEPOLY
]

vertices['spoon'] = [
    (0, 0.),
    (0, -0.03*c), (0.03*(1-c), -0.03), (0.03, -0.03),
    (0.55, -0.02),
    (0.5, 0.),
    (0.5, -0.1*c), (0.65-0.15*c, -0.1), (0.65, -0.1),
    (0.65+0.15*c, -0.1), (0.8, -0.1*c), (0.8, 0.),
    (0.8, 0.1*c), (0.65+0.15*c, 0.1), (0.65, 0.1),
    (0.65-0.15*c, 0.1), (0.5, 0.1*c), (0.5, 0.),
    (0.55, 0.02),
    (0.03, 0.03),
    (0.03*(1-c), 0.03), (0, 0.03*c), (0., 0.),
    (0, 0)
]

rotation_center = np.array([0., 0.])
rotation_matrix = np.array([[np.cos(np.pi / 4), -np.sin(np.pi / 4)],
                            [np.sin(np.pi / 4), np.cos(np.pi / 4)]])
spoon_scale = 1.25
vertices['spoon'] = rotation_center + spoon_scale*np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices['spoon'] - rotation_center))


codes['spoon'] = [
    Path.MOVETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CLOSEPOLY
]


card_rect = FancyBboxPatch([-0.22, -0.4], 0.44, 0.8, boxstyle=BoxStyle("Round", pad=0.1))
vertices['small-card'] = card_rect.get_path().vertices
codes['small-card'] = card_rect.get_path().codes

top_rect = FancyBboxPatch([-0.22, 0.35], 0.44, 0.05, boxstyle=BoxStyle("Round", pad=0.1))
vertices['small-card-top'] = top_rect.get_path().vertices
vertices['small-card-top'] = [[v[0], np.maximum(0.35, v[1])] for v in vertices['small-card-top']]
codes['small-card-top'] = top_rect.get_path().codes


key_center = np.array([0.32, -0.22])
vertices['key-circle'] = [
    (0, 0.5),
    (0, 0.5 - c*0.5), (0.5 - c*0.5, 0), (0.5, 0),
    (0.5 + c*0.5, 0), (1, 0.5 - c*0.5), (1, 0.5),
    (1, 0.5 + c*0.5), (0.5 + c*0.5, 1), (0.5, 1),
    (0.5 - c*0.5, 1), (0, 0.5 + c*0.5), (0, 0.5),
    (0, 0)
]
codes['key-circle'] = [
    Path.MOVETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CLOSEPOLY
]
vertices['key-circle'] = key_center + 0.2*(np.array(vertices['key-circle']) - np.array([0.5, 0.5]))

vertices['key'] = [
    (0.1*np.sqrt(3)/2, - 0.1*1/2),
    (0.3*np.sqrt(3)/2, - 0.3*1/2),
    (0.3*np.sqrt(3)/2 + 0.07*1/2, - 0.3*1/2 + 0.07*np.sqrt(3)/2),
    (0.25*np.sqrt(3)/2, - 0.25*1/2),
    (0.25*np.sqrt(3)/2 + 0.07*1/2, - 0.25*1/2 + 0.07*np.sqrt(3)/2)
]
codes['key'] = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.MOVETO,
    Path.LINETO,
]
vertices['key'] = key_center + (np.array(vertices['key']))



vertices['house'] = [
    (0.15, 0.15),
    (0.15, 0.55),
    (0.5, 1),
    (0.85, 0.55),
    (0.85, 0.15),
    (0.75, 0.15),
    (0.75, 0),
    (0.25, 0),
    (0.25, 0.15),
    (0, 0)
]
codes['house'] = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY
]

vertices['chimney'] = [
    (0.7, 0.5),
    (0.7, 0.9),
    (0.75, 0.9),
    (0.75, 0.5),
    (0, 0)
]
codes['chimney'] = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY
]


vertices['coin_top'] = [
    (0., 0.5),
    (0., 0.5 + c*0.25), (0.5 - c*0.5, 0.75), (0.5, 0.75),
    (0.5 + c*0.5, 0.75), (1.0, 0.5 + c*0.25), (1.0, 0.5),
    (1.0, 0.5 - c*0.25), (0.5 + c*0.5, 0.25), (0.5, 0.25),
    (0.5 - c*0.5, 0.25), (0., 0.5 - c*0.25), (0., 0.5),
    (0, 0)
]

codes['coin_top'] = [
    Path.MOVETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CLOSEPOLY
]

vertices['coin_side'] = [
    (0., 0.5),
    (0., 0.5 + c*0.25), (0.5 - c*0.5, 0.75), (0.5, 0.75),
    (0.5 + c*0.5, 0.75), (1.0, 0.5 + c*0.25), (1.0, 0.5),
    (1.0, 0.4),
    (1.0, 0.4 - c*0.25), (0.5 + c*0.5, 0.15), (0.5, 0.15),
    (0.5 - c*0.5, 0.15), (0., 0.4 - c*0.25), (0., 0.4),
    (0, 0.5),
    (0, 0)
]

codes['coin_side'] = [
    Path.MOVETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.CLOSEPOLY
]


finger_width = 0.1

finger_angles = {}
finger_angles[0] = 30
finger_angles[1] = 10
finger_angles[2] = 0
finger_angles[3] = -10
finger_angles[4] = -20

finger_lengths = {}
finger_lengths[0] = 0.2

vertices['hand'] = [
    (0.9, -0.2),
    (0.35, -0.2),
    (0.0, 0.4)
] + _half_circle_points((0.0, 0.4), finger_width, finger_angles[0]) + [
    (0.35, 0.25),
    (0.3, 0.95)
] + _half_circle_points((0.3, 0.95), 0.9*finger_width, finger_angles[1]) + [
    (0.55, 0.5),
    (0.55, 1.05)
] + _half_circle_points((0.55, 1.05), 0.9*finger_width, finger_angles[2]) + [
    (0.75, 0.5),
    (0.8, 0.95)
] + _half_circle_points((0.8, 0.95), 0.9*finger_width, finger_angles[3]) + [
    (0.95, 0.45),
    (1.05, 0.7)
] + _half_circle_points((1.05, 0.7), 0.8*finger_width, finger_angles[4]) + [
    (1.1, 0.3),
    (1., 0.),
    (0, 0)
]

codes['hand'] = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.CURVE4, Path.CURVE4, Path.CURVE4,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY
]