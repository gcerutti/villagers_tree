import numpy as np
import scipy.ndimage as nd

import matplotlib.pyplot as plt

from matplotlib.textpath import TextPath
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import imageio

import pandas as pd

from ..cards import draw_villager_card


villagers_data = pd.read_csv('villagers.csv')
villagers_data = villagers_data[villagers_data['Box']=="V"]
suits = villagers_data['Suit'].unique()

villagers = dict(zip(villagers_data['Villager'], [villagers_data.iloc[i].to_dict() for i in range(len(villagers_data))]))
for v in villagers:
    padlock = villagers[v]['Padlock']
    if not pd.isnull(padlock):
        padlock_suit = villagers[padlock]['Suit'] if padlock in villagers else "Wood"
    else:
        padlock_suit = ""
    villagers[v]['Padlock Suit'] = padlock_suit

villager_parent = {}
for v in villagers:
    villager_dict = villagers[v]
    chain = villager_dict['Chain']
    chain_list = chain.split("+")
    i_v = chain_list.index(v)
    if i_v == 0:
        villager_parent[v] = None
    else:
        villager_parent[v] = chain_list[i_v-1]

suit_villagers = {}
for suit in suits:
    suit_villagers[suit] = [v for v in villagers if villagers[v]['Suit']==suit]

figure = plt.figure(figsize=(20, 30))

draw_villager_card(figure.gca(), villagers['Founders'], xy=[0, 2])
draw_villager_card(figure.gca(), villagers['Log Rafter'], xy=[0, 2/3])
draw_villager_card(figure.gca(), villagers['Locksmith'], xy=[0, -2/3])
draw_villager_card(figure.gca(), villagers['Milk Maid'], xy=[0, -2])

figure.gca().set_xlim(-2, 2)
figure.gca().set_ylim(-3, 3)

figure = plt.figure(figsize=(20, 30))

draw_villager_card(figure.gca(), villagers['Cobbler'], xy=[0, 2])
draw_villager_card(figure.gca(), villagers['Freemason'], xy=[0, 2/3])
draw_villager_card(figure.gca(), villagers['Brewer'], xy=[0, -2/3])
draw_villager_card(figure.gca(), villagers['Weaver'], xy=[0, -2])

figure.gca().set_xlim(-2, 2)
figure.gca().set_ylim(-3, 3)

figure = plt.figure(figsize=(21, 9))

for v in villagers:
    figure.clf()
    draw_villager_card(figure.gca(), villagers[v], xy=[0, 0])
    figure.gca().set_xlim(-21*0.075, 21*0.075)
    figure.gca().set_ylim(-9*0.075, 9*0.075)
    figure.gca().axis('off')
    figure.savefig(f"villager_cards/{v}.png")


villager_card_images = {}
for v in villagers:
    card_file = f"villager_cards/{v}.png"
    villager_card_images[v] = imageio.imread(card_file)

#villager_names = list(villagers.keys())[:20]
#villager_names = list(villagers.keys())[:50]
villager_names = [v for suit in suits for v in suit_villagers[suit][::-1]]

roots = [v for v in villager_names if villager_parent[v] is None]

root_children = {r: [v for v in villager_names[::-1] if villager_parent[v]==r] for r in roots}
root_widths = {r: np.maximum(1, len(root_children[r])) for r in roots}
total_width = np.sum(list(root_widths.values()))
print(root_widths, total_width)

villager_depth = {v: 1 for v in roots}
while len(villager_depth) < len(villager_names):
    for v in villager_names:
        if villager_parent[v] in villager_depth:
            villager_depth[v] = villager_depth[villager_parent[v]] + 1
maximum_depth = 4

#radius = total_width/np.pi + maximum_depth*4.2
radius = total_width/np.pi + 1.5*4.2
print(radius)
figure = plt.figure(figsize=(4*radius, 4*radius))

angle = 180-root_widths[roots[0]]*180/total_width
angles = {}
distances = {}
positions = {}

for v in roots:
    root_angle = angle + root_widths[v]*180/total_width
    angles[v] = root_angle
    distances[v] = radius

    extent_points = np.array([[-2.1, -0.9], [2.1, -0.9], [2.1, 0.9], [-2.1, 0.9]])
    extent_points += np.array([distances[v], 0])

    rotation_matrix = np.array([[np.cos(np.radians(angles[v])), -np.sin(np.radians(angles[v]))],
                                [np.sin(np.radians(angles[v])), np.cos(np.radians(angles[v]))]])
    rotated_extent_points = np.einsum("...ij,...j->...i", rotation_matrix, extent_points)
    positions[v] = rotated_extent_points.mean(axis=0)

    villager_img = nd.rotate(villager_card_images[v], angle=180+root_angle)
    extent = (
        rotated_extent_points[:,0].min(),
        rotated_extent_points[:,0].max(),
        rotated_extent_points[:,1].min(),
        rotated_extent_points[:,1].max()
    )
    figure.gca().imshow(villager_img, extent=extent)

    for i, c in enumerate(root_children[v]):
        angles[c] = angle + (i + 0.5)*360/total_width
        distances[c] = radius - 4.2*(villager_depth[c]-1)

        extent_points = np.array([[-2.1, -0.9], [2.1, -0.9], [2.1, 0.9], [-2.1, 0.9]])
        extent_points += np.array([distances[c], 0])
        rotation_matrix = np.array([[np.cos(np.radians(angles[c])), -np.sin(np.radians(angles[c]))],
                                    [np.sin(np.radians(angles[c])), np.cos(np.radians(angles[c]))]])
        rotated_extent_points = np.einsum("...ij,...j->...i", rotation_matrix, extent_points)

        positions[c] = rotated_extent_points.mean(axis=0)

        villager_img = nd.rotate(villager_card_images[c], angle=180+angles[c])
        extent = (
            rotated_extent_points[:,0].min(),
            rotated_extent_points[:,0].max(),
            rotated_extent_points[:,1].min(),
            rotated_extent_points[:,1].max()
        )
        figure.gca().imshow(villager_img, extent=extent)

    angle += root_widths[v]*360/total_width

non_placed_villagers = [v for v in villager_names if not v in positions]
while len(non_placed_villagers) > 0:
    for v in villager_names:
        if not v in positions and villager_parent[v] in positions:
            angles[v] = angles[villager_parent[v]]
            distances[v] = radius - 4.2*(villager_depth[v]-1)

            extent_points = np.array([[-2.1, -0.9], [2.1, -0.9], [2.1, 0.9], [-2.1, 0.9]])
            extent_points += np.array([distances[v], 0])

            rotation_matrix = np.array([[np.cos(np.radians(angles[v])), -np.sin(np.radians(angles[v]))],
                                        [np.sin(np.radians(angles[v])), np.cos(np.radians(angles[v]))]])
            rotated_extent_points = np.einsum("...ij,...j->...i", rotation_matrix, extent_points)

            positions[v] = rotated_extent_points.mean(axis=0)

            villager_img = nd.rotate(villager_card_images[v], angle=180+angles[v])
            extent = (
                rotated_extent_points[:,0].min(),
                rotated_extent_points[:,0].max(),
                rotated_extent_points[:,1].min(),
                rotated_extent_points[:,1].max()
            )
            figure.gca().imshow(villager_img, extent=extent, zorder=5)
    non_placed_villagers = [v for v in villager_names if not v in positions]

for v in villager_names:
    if villager_parent[v] is not None:
        p = villager_parent[v]
        if v in positions and p in positions:
            v_vector = [np.cos(np.radians(angles[v])), np.sin(np.radians(angles[v]))]
            p_vector = [np.cos(np.radians(angles[p])), np.sin(np.radians(angles[p]))]

            if  np.isclose(angles[v], angles[p], atol=0.01):
                arc_points = []
            else:
                arc_angles = angles[p] + np.linspace(0, ((angles[v]-angles[p]+180)%360) - 180, 11)
                arc_points = (distances[p] - 2.1)*np.transpose([np.cos(np.radians(arc_angles)), np.sin(np.radians(arc_angles))])

            vertices = [
                           (positions[p][0] - 1.55*p_vector[0], positions[p][1] - 1.55*p_vector[1])
                       ] + list(arc_points) + [
                           (positions[v][0] + 1.45*v_vector[0], positions[v][1] + 1.45*v_vector[1])
                       ]
            codes = [
                        Path.MOVETO
                    ] + [Path.LINETO for _ in arc_points] + [
                        Path.LINETO
                    ]
            patch = PathPatch(Path(vertices, codes), fc='none', ec=suit_color[villagers[v]['Suit']], linewidth=2)
            figure.gca().add_artist(patch)

    l = villagers[v]['Padlock']
    if not pd.isnull(l):
        if v in positions and l in positions:
            v_vector = [np.cos(np.radians(angles[v])), np.sin(np.radians(angles[v]))]
            l_vector = [np.cos(np.radians(angles[l])), np.sin(np.radians(angles[l]))]
            vertices = [
                (positions[l][0] - 1.55*l_vector[0], positions[l][1] - 1.55*l_vector[1]),
                #(positions[l][0]/4 , positions[l][1]/4),
                #(positions[l][0] - 8.85*l_vector[0], positions[l][1] - 8.85*l_vector[1]),
                (-4.2*l_vector[0], -4.2*l_vector[1]),
                #(0, 0),
                #(0, 0),
                (positions[v][0] - 1.65*v_vector[0] - 1.65*v_vector[1], positions[v][1] - 1.65*v_vector[1] + 1.65*v_vector[0]),
                #(positions[v][0] - 2.45*v_vector[1], positions[v][1] + 2.45*v_vector[0]),
                (positions[v][0] - 0.65*v_vector[1], positions[v][1] + 0.65*v_vector[0])
                #(positions[v][0] - 1.55*v_vector[0] - 0.95*v_vector[1], positions[v][1] - 1.55*v_vector[1] + 0.95*v_vector[0])
            ]
            codes = [
                Path.MOVETO,
                #Path.CURVE3,
                #Path.CURVE3
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4
            ]
            patch = PathPatch(Path(vertices, codes), fc='none', ec=suit_color[villagers[l]['Suit']], linewidth=2, alpha=0.5, linestyle='--', zorder=0)
            figure.gca().add_artist(patch)

            '''vertices = [
                (positions[v][0] - 1.55*v_vector[0] - 0.95*v_vector[1], positions[v][1] - 1.55*v_vector[1] + 0.95*v_vector[0]),
                #(positions[v][0] - 0.95*v_vector[0] - 0.95*v_vector[1], positions[v][1] - 0.95*v_vector[1] + 0.95*v_vector[0]),
                (positions[v][0] - 0.95*v_vector[1], positions[v][1] + 0.95*v_vector[0]),
                (positions[v][0] - 0.65*v_vector[1], positions[v][1] + 0.65*v_vector[0]),
            ]
            codes = [
                Path.MOVETO,
                #Path.CURVE4,
                Path.CURVE3,
                Path.CURVE3
            ]
            patch = PathPatch(Path(vertices, codes), fc='none', ec=suit_color[villagers[l]['Suit']], linewidth=1, alpha=0.5, linestyle='--', zorder=0)
            figure.gca().add_artist(patch)'''


figure.gca().set_xlim(-radius-2.1, radius+2.1)
figure.gca().set_ylim(-radius-2.1, radius+2.1)

figure.gca().axis('off')
figure.tight_layout()

figure.savefig(f"Villagers_Tree.png")

for suit in suits:
    roots = [v for v in suit_villagers[suit][::-1] if villager_parent[v] is None]

    root_children = {r: [v for v in suit_villagers[suit][::-1] if villager_parent[v]==r] for r in roots}
    root_heights = {r: np.maximum(1, len(root_children[r])) for r in roots}
    total_height = np.sum(list(root_heights.values()))

    villager_depth = {v: 1 for v in roots}
    while len(villager_depth) < len(suit_villagers[suit]):
        for v in suit_villagers[suit]:
            if villager_parent[v] in villager_depth:
                villager_depth[v] = villager_depth[villager_parent[v]] + 1
    maximum_depth = 4

    figure = plt.figure(figsize=(20*maximum_depth, 10*total_height))

    positions = {}
    offset = 0
    for r in roots:
        xy = [2, offset + 2*root_heights[r]/2]
        draw_villager_card(figure.gca(), villagers[r], xy=xy)
        positions[r] = xy

        for i, v in enumerate(root_children[r]):
            xy = [-2 + 4*villager_depth[v], offset + 2*(i + 0.5)]
            draw_villager_card(figure.gca(), villagers[v], xy=xy)
            positions[v] = xy

        offset += 2*root_heights[r]

    non_placed_villagers = [v for v in suit_villagers[suit] if not v in positions]
    while len(non_placed_villagers) > 0:
        for v in suit_villagers[suit]:
            if not v in positions:
                xy = [-2 + 4*villager_depth[v], positions[villager_parent[v]][1]]
                draw_villager_card(figure.gca(), villagers[v], xy=xy)
                positions[v] = xy
        non_placed_villagers = [v for v in suit_villagers[suit] if not v in positions]

    for v in suit_villagers[suit]:
        if villager_parent[v] is not None:
            p = villager_parent[v]
            vertices = [
                (positions[p][0]+1.5, positions[p][1]),
                (positions[p][0]+2., positions[p][1]),
                #(positions[p][0]+2.25, positions[p][1]),
                (positions[v][0]-2., positions[v][1]),
                #(positions[v][0]-2.25, positions[v][1]),
                (positions[v][0]-1.5, positions[v][1])
            ]
            codes = [
                Path.MOVETO,
                Path.LINETO, Path.LINETO, Path.LINETO
                #Path.CURVE4, Path.CURVE4, Path.CURVE4
            ]
            patch = PathPatch(Path(vertices, codes), fc='none', ec=suit_color[suit], linewidth=3)
            figure.gca().add_artist(patch)

    figure.gca().set_xlim(0, maximum_depth*4)
    figure.gca().set_ylim(0, total_height*2)

    figure.gca().axis('off')
    figure.tight_layout()
    figure.savefig(f"Villagers_{suit}_Tree.png")
