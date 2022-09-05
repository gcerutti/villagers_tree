import os

import numpy as np

from matplotlib.path import Path
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch, Circle
from matplotlib import patheffects

from matplotlib.font_manager import fontManager, findSystemFonts

from imageio.v2 import imread

import villagers_tree
from .paths import vertices as path_vertices
from .paths import codes as path_codes

font_files = [f for f in findSystemFonts(fontpaths=None, fontext='ttf') if 'Brandon' in f]
font_list = [fontManager.addfont(f) for f in font_files]


def draw_villagers_text(ax, xy, text, size=1, color='k', ha='center', va='center', bold=False, alpha=1):
    prop = {"family":f'Brandon Grotesque{" Bold" if bold else ""}'}
    path = TextPath((0, 0), text.upper(), size=size, prop=prop)
    bbox = path.get_extents()

    path_center = [0, 0]
    if ha == 'center':
        path_center[0] = (bbox.x0 + bbox.x1)/2
    elif ha == 'left':
        path_center[0] = bbox.x0
    if va == 'center':
        path_center[1] = (bbox.y0 + bbox.y1)/2

    path = Path(path.vertices + xy - np.array(path_center), path.codes)
    patch = PathPatch(path, fc=color, ec='none', alpha=alpha)
    ax.add_patch(patch)

    return path


suit_color = {}
suit_color['Grains'] = "#6ac9bd"
suit_color['Hay'] = "#6a3a8b"
suit_color['Wood'] = "#6eb261"
suit_color['Ore'] = "#0a0b0c"
suit_color['Grapes'] = "#ed54a1"
suit_color['Wool'] = "#4798cf"
suit_color['Leather'] = "#f5c25a"
suit_color['Solitary'] = "#775533"

suit_images = {}
def _load_suit_image(suit):

    module_dir = villagers_tree.__path__[0]
    data_dir = os.path.abspath(f"{module_dir}/../../data/")

    logo_file = f"{data_dir}/suit_logos/{suit}.png"
    if os.path.exists(logo_file):
        suit_images[suit] = imread(logo_file)
    else:
        suit_images[suit] = np.zeros((150, 150, 4), np.uint8)


def draw_suit_symbol(ax, suit, xy=[0,0], size=1, center=True):
    if suit not in suit_images:
        _load_suit_image(suit)

    if center:
        extent = (xy[0]-size/2, xy[0]+size/2, xy[1]-size/2, xy[1]+size/2)
        circle_center = xy
    else:
        extent = (xy[0], xy[0]+size, xy[1], xy[1]+size)
        circle_center = (xy[0]+size/2, xy[1]+size/2)

    circle = Circle(xy=circle_center, radius=size/2, color="w", zorder=5)
    ax.add_artist(circle)
    ax.imshow(suit_images[suit], extent=extent, zorder=5)


def draw_padlock(ax, xy=[0,0], size=1., color='k', angle=0, ec='none', linewidth=1, open_lock=False, center=False):
    path_list = ['padlock', 'shackle', 'shackle-open']
    vertices = {p: path_vertices[p] for p in path_list}
    codes = {p: path_codes[p] for p in path_list}

    if center:
        for p in vertices:
            vertices[p] = np.array(vertices[p]) - np.array([1, 1.25])
        rotation_center = np.array([0., 0])
    else:
        rotation_center = np.array([1., 2/3])
    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

    for p in vertices:
        vertices[p] = rotation_center + np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices[p] - rotation_center))
        vertices[p] = np.array(vertices[p])/2.

    if open_lock:
        shackle_path = Path(np.array(xy) + size*np.array(vertices['shackle-open']), codes['shackle-open'])
    else:
        shackle_path = Path(np.array(xy) + size*np.array(vertices['shackle']), codes['shackle'])
    patch = PathPatch(shackle_path, fc=color, ec='none', path_effects=[patheffects.withStroke(linewidth=linewidth,foreground=ec)], alpha=1)
    ax.add_patch(patch)

    path = Path(np.array(xy) + size*np.array(vertices['padlock']), codes['padlock'])
    patch = PathPatch(path, fc=color, ec='none', path_effects=[patheffects.withStroke(linewidth=linewidth,foreground=ec)], alpha=1)
    ax.add_patch(patch)

    patch = PathPatch(shackle_path, fc=color, ec='none', alpha=1)
    ax.add_patch(patch)


def draw_food_symbol(ax, xy=[0,0], size=1, center=True, angle=0):
    path_list = ['plate', 'spoon']
    vertices = {p: path_vertices[p] for p in path_list}
    codes = {p: path_codes[p] for p in path_list}

    if center:
        for p in vertices:
            vertices[p] = np.array(vertices[p]) - np.array([0.5, 0.5])

    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

    for p in vertices:
        vertices[p] = np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices[p]))

        path = Path(np.array(xy) + size*np.array(vertices[p]), codes[p])
        patch = PathPatch(path, fc='#d93b3b', ec='none', alpha=1)
        ax.add_patch(patch)


def draw_tilted_card(ax, xy=[0,0], size=1, suit=None, center=True, angle=-20):
    path_list = ['small-card']
    if suit is not None:
        path_list += ['small-card-top']
    vertices = {p: path_vertices[p] for p in path_list}
    codes = {p: path_codes[p] for p in path_list}

    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

    for p in vertices:
        vertices[p] = np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices[p]))

        path = Path(np.array(xy) + size*np.array(vertices[p]), codes[p])
        if p == 'card-top':
            patch = PathPatch(path, fc=suit_color.get(suit, 'k'), ec='none', alpha=1)
        else:
            patch = PathPatch(path, fc='none', ec=suit_color.get(suit, 'k'), linewidth=2, alpha=1)
        ax.add_artist(patch)


def draw_unlocks_symbol(ax, xy=[0,0], size=1, value=2, angle=-20):

    path_list = ['small-card', 'key-circle', 'key']
    vertices = {p: path_vertices[p] for p in path_list}
    codes = {p: path_codes[p] for p in path_list}

    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

    for p in vertices:
        vertices[p] = np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices[p]))

        path = Path(np.array(xy) + size*np.array(vertices[p]), codes[p])
        patch = PathPatch(path, fc='none', ec='k', linewidth=2, alpha=1)
        ax.add_artist(patch)

    draw_villagers_text(ax, [xy[0], xy[1]], str(value), color='k', size=size/2, alpha=1, bold=False)


def draw_builder_symbol(ax, xy=[0,0], size=1, center=True, angle=0):
    path_list = ['house', 'chimney']
    vertices = {p: path_vertices[p] for p in path_list}
    codes = {p: path_codes[p] for p in path_list}

    if center:
        for p in vertices:
            vertices[p] = np.array(vertices[p]) - np.array([0.5, 0.5])

    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

    for p in vertices:
        vertices[p] = np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices[p]))

        path = Path(np.array(xy) + size*np.array(vertices[p]), codes[p])
        patch = PathPatch(path, fc='k', alpha=1)
        ax.add_artist(patch)


def draw_coins_symbol(ax, xy=[0,0], size=1, center=True, angle=0):
    vertices = {}
    codes = {}
    codes['top_coin_top'] = path_codes['coin_top']
    vertices['top_coin_top'] = np.array(path_vertices['coin_top']) + np.array([0.05, 0.1])
    codes['top_coin_top'] = path_codes['coin_top']
    vertices['top_coin_side'] = np.array(path_vertices['coin_side']) + np.array([0.05, 0.1])
    codes['top_coin_side'] = path_codes['coin_side']
    vertices['top_coin_circle'] = 0.75*(np.array(path_vertices['coin_top']) - np.array([0.5, 0.5])) + np.array([0.55, 0.6])
    codes['top_coin_circle'] = path_codes['coin_top']
    vertices['bottom_coin_top'] = np.array(path_vertices['coin_top']) + np.array([-0.05, -0.1])
    codes['bottom_coin_top'] = path_codes['coin_top']
    vertices['bottom_coin_side'] = np.array(path_vertices['coin_side']) + np.array([-0.05, -0.1])
    codes['bottom_coin_side'] = path_codes['coin_side']
    vertices['bottom_coin_circle'] = 0.75*(np.array(path_vertices['coin_top']) - np.array([0.5, 0.5])) + np.array([0.45, 0.4])
    codes['bottom_coin_circle'] = path_codes['coin_top']

    if center:
        for p in vertices:
            vertices[p] = np.array(vertices[p]) - np.array([0.5, 0.5])

    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

    for p in ['bottom_coin_side', 'bottom_coin_top', 'bottom_coin_circle', 'top_coin_side', 'top_coin_top', 'top_coin_circle']:
        vertices[p] = np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices[p]))

        path = Path(np.array(xy) + (size/1.2)*np.array(vertices[p]), codes[p])
        if 'side' in p :
            patch = PathPatch(path, fc='#f3eeee', ec='none', alpha=1)
        elif 'circle' in p:
            patch = PathPatch(path, fc='none', ec='#873226', alpha=1)
        else:
            patch = PathPatch(path, fc='#c9833f', ec='none', alpha=1)
        ax.add_artist(patch)


def draw_hand(ax, xy=[0,0], size=1, center=True, angle=0):
    path_list = ['hand']
    vertices = {p: path_vertices[p] for p in path_list}
    codes = {p: path_codes[p] for p in path_list}

    if center:
        for p in vertices:
            vertices[p] = np.array(vertices[p]) - np.array([0.5, 0.4])

    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

    for p in vertices:
        vertices[p] = np.einsum("...ij,...j->...i", rotation_matrix, np.array(vertices[p]))
        path = Path(np.array(xy) + (size/1.2)*np.array(vertices[p]), codes[p])
        patch = PathPatch(path, fc='k', ec='none', alpha=1)
        ax.add_artist(patch)
