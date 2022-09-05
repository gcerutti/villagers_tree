import numpy as np
import pandas as pd

from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle, Arc, RegularPolygon

from .paths import _card_points, _card_side_points
from .paths import vertices as path_vertices
from .paths import codes as path_codes

from .symbols import draw_villagers_text, draw_suit_symbol, draw_food_symbol, draw_builder_symbol, draw_tilted_card, \
draw_padlock, draw_unlocks_symbol, draw_coins_symbol, draw_hand
from .symbols import suit_color


def draw_card(ax, xy=[0,0], size=1., color='g', ec='k', radius=0.1, aspect_ratio=4/3., margin=0.2, center=True):
    path_list = ['card', 'card-side']
    vertices = {p: path_vertices[p] for p in path_list}
    codes = {p: path_codes[p] for p in path_list}

    vertices['card'] = _card_points(radius=radius, aspect_ratio=aspect_ratio)
    vertices['card-side'] = _card_side_points(radius=radius, aspect_ratio=aspect_ratio, margin=margin)

    if center:
        h = 1/aspect_ratio
        for p in vertices:
            vertices[p] = np.array(vertices[p]) - np.array([0.5, h/2])

    path = Path(np.array(xy) + size*np.array(vertices['card']), codes['card'])
    patch = PathPatch(path, fc='w', ec=ec, alpha=1, linewidth=3)
    ax.add_patch(patch)

    path = Path(np.array(xy) + size*np.array(vertices['card-side']), codes['card-side'])
    patch = PathPatch(path, fc=color, ec='none', alpha=1)
    ax.add_patch(patch)


def draw_villager_gold(ax, xy=[0,0], size=1, value=None):
    gold_circle = Circle(xy=xy, radius=size/2, color="#f1e962")
    ax.add_artist(gold_circle)

    if value is not None:
        draw_villagers_text(ax, [xy[0], xy[1]], str(int(value)), color='k', size=size/2, alpha=0.66, bold=False)


def draw_villager_silver_bronze(ax, xy=[0,0], size=1, value=None, condition="", suit="", bronze=False):
    condition_height = 1
    if condition in ["Food", "Builder", "Padlock", "Gold on Wood", "Gold on Leather", "Coins on Villager", "Card in Hand"]:
        condition_height = 1.2
    if condition in ["2 Ore", "2 Hay", "2 Solitary", "2 Gold"]:
        condition_height = 2

    silver_size = (1.5 + condition_height)*size
    circle_xy = [xy[0], xy[1] + silver_size/2 - 0.5*size]
    if bronze:
        bronze_circle = Circle(xy=circle_xy, radius=size/2, color="#f48b53")
        ax.add_artist(bronze_circle)
        arc = Arc(circle_xy, 3*size/4, 3*size/4, angle=0, theta1=0, theta2=90, capstyle='round', lw=2, color='w')
        ax.add_patch(arc)
        arrow = RegularPolygon((circle_xy[0]+3*size/8, circle_xy[1]), 3, size/20, np.pi, color='w')
        ax.add_patch(arrow)

        arc = Arc(circle_xy, 3*size/4, 3*size/4, angle=180, theta1=0, theta2=90, capstyle='round', lw=2, color='w')
        ax.add_patch(arc)
        arrow = RegularPolygon((circle_xy[0]-3*size/8, circle_xy[1]), 3, size/20, 0, color='w')
        ax.add_patch(arrow)
    else:
        silver_circle = Circle(xy=circle_xy, radius=size/2, color="#c5c5c5")
        ax.add_artist(silver_circle)

    if value is not None:
        draw_villagers_text(ax, [circle_xy[0], circle_xy[1]], str(int(value)), color='k', size=size/2, alpha=0.66, bold=False)

    if condition in ["Wood", "Grains"]:
        draw_suit_symbol(ax, condition, [xy[0], xy[1] - silver_size/2 + 0.5*size], size=size, center=True)
    elif condition in ["Gold"]:
        draw_villager_gold(ax, [xy[0], xy[1] - silver_size/2 + 0.5*size], size=0.9*size)
    elif condition in ["Food", "Builder", "Padlock", "Coins on Villager", "Card in Hand"]:
        draw_tilted_card(ax, [xy[0], xy[1] - silver_size/2 + 0.6*size], size=size, center=True)
        if condition == "Food":
            draw_food_symbol(ax, [xy[0], xy[1] - silver_size/2 + 0.6*size], size=0.5*size, angle=-20)
        elif condition == "Builder":
            draw_builder_symbol(ax, [xy[0], xy[1] - silver_size/2 + 0.6*size], size=0.5*size, angle=-20)
        elif condition == "Padlock":
            draw_padlock(ax, [xy[0], xy[1] - silver_size/2 + 0.6*size], size=0.4*size, angle=-20, center=True)
        elif condition == "Coins on Villager":
            draw_coins_symbol(ax, [xy[0], xy[1] - silver_size/2 + 0.6*size], size=0.5*size)
        elif condition == "Card in Hand":
            draw_hand(ax, [xy[0]-0.25*size, xy[1] - silver_size/2 + 0.4*size], size=0.6*size, angle=-40)
    elif condition in ["Gold on Wood", "Gold on Leather"]:
        draw_tilted_card(ax, [xy[0], xy[1] - silver_size/2 + 0.6*size], suit=condition[8:], size=size, center=True)
        draw_villager_gold(ax, [xy[0], xy[1] - silver_size/2 + 0.6*size], size=0.35*size)
    elif condition in ["2 Ore", "2 Hay", "2 Solitary"]:
        draw_suit_symbol(ax, condition[2:], [xy[0], xy[1] - silver_size/2 + 1.5*size], size=size, center=True)
        draw_suit_symbol(ax, condition[2:], [xy[0], xy[1] - silver_size/2 + 0.5*size], size=size, center=True)
    elif condition in ["2 Gold"]:
        draw_villager_gold(ax, [xy[0], xy[1] - silver_size/2 + 1.5*size], size=0.9*size)
        draw_villager_gold(ax, [xy[0], xy[1] - silver_size/2 + 0.5*size], size=0.9*size)
    draw_villagers_text(ax, [xy[0], xy[1] + silver_size/2 - 1.3*size], "x", color=suit_color.get(suit, 'k'), size=0.33*size, alpha=1, bold=True)


def draw_founders_symbols(ax, xy=[0,0], size=1):
    draw_villager_gold(ax, [xy[0], xy[1]+size], value=2, size=size)
    draw_food_symbol(ax, [xy[0], xy[1]-size], size=size)

    arc = Arc([xy[0]-size/4, xy[1]], size/2, size/2, angle=-180, theta1=-135, theta2=90, capstyle='round', lw=2, color=suit_color['Grains'])
    ax.add_patch(arc)
    arrow = RegularPolygon((xy[0]-size/4, xy[1]-size/4), 3, size/16, np.pi/6, color=suit_color['Grains'])
    ax.add_patch(arrow)

    draw_tilted_card(ax, [xy[0]+size/4, xy[1]], angle=-20, size=3*size/4, suit='Grains')


def draw_villager_card(ax, villager_dict, xy=[0,0]):
    name = villager_dict['Villager']
    chain = villager_dict['Chain']
    suit = villager_dict['Suit']
    padlock = villager_dict['Padlock']

    food = villager_dict['Food']
    builder = villager_dict['Builder']
    gold = villager_dict['Gold']
    unlocks = villager_dict['Unlocks']


    silver = villager_dict['Silver']
    bronze = villager_dict['Bronze']
    condition = villager_dict['Condition']

    suit_symbols = villager_dict['Symbols']

    draw_card(ax, xy, size=3, margin=0.15, color=suit_color[suit], ec=suit_color[suit], aspect_ratio=21/9, radius=0.05, center=True)
    draw_villagers_text(ax, [xy[0]+0.05, xy[1]], name, color=suit_color[suit], size=0.25, bold=True)

    chain_list = chain.split("+")
    if len(chain_list) > 1:
        for i, c in enumerate(chain_list[::-1]):
            draw_villagers_text(ax, [xy[0]+0.05, xy[1]+0.25+i*0.1], c, color=suit_color[suit], size=0.1 + 0.01*(c==name), bold=(c==name))

    for i in range(suit_symbols):
        draw_suit_symbol(ax, suit, [xy[0]-1.05, xy[1]-i*0.35+(suit_symbols-1)*0.0], size=0.33, center=True)

    if name == 'Founders':
        draw_founders_symbols(ax, [xy[0]+1.25, xy[1]], size=0.33)
    else:
        n_symbols = 0
        if not pd.isnull(food):
            n_symbols += int(food)
        if not pd.isnull(builder):
            n_symbols += int(builder)
        if not pd.isnull(gold):
            n_symbols += 1
        if not pd.isnull(unlocks):
            n_symbols += 1

        i_symbol = 0
        if not pd.isnull(food):
            for i in range(int(food)):
                draw_food_symbol(ax, [xy[0]+1.25, xy[1] - (i_symbol-(n_symbols-1)/2)*0.4], size=0.33)
                i_symbol += 1
        if not pd.isnull(builder):
            for i in range(int(builder)):
                draw_builder_symbol(ax, [xy[0]+1.25, xy[1] - (i_symbol-(n_symbols-1)/2)*0.4], size=0.33)
                i_symbol += 1
        if not pd.isnull(gold):
            draw_villager_gold(ax, [xy[0]+1.25, xy[1] - (i_symbol-(n_symbols-1)/2)*0.4], size=0.33, value=int(gold))
            i_symbol += 1
        if not pd.isnull(unlocks):
            draw_unlocks_symbol(ax, [xy[0]+1.25, xy[1] - (i_symbol-(n_symbols-1)/2)*0.4], size=0.33, value=int(unlocks))
            i_symbol += 1

        if not pd.isnull(silver) or not pd.isnull(bronze):
            is_bronze = not pd.isnull(bronze)
            value = int(bronze) if is_bronze else int(silver)
            draw_villager_silver_bronze(ax, [xy[0]+1.25, xy[1]], size=0.33, value=value, condition=condition, bronze=is_bronze, suit=suit)

    if not pd.isnull(padlock):
        padlock_suit = villager_dict['Padlock Suit']
        if not pd.isnull(padlock_suit):
            path = draw_villagers_text(ax, [xy[0]+0.1, xy[1]-0.25], padlock, color=suit_color[padlock_suit], size=0.1, bold=False)
            bbox = path.get_extents()
            draw_padlock(ax, xy=(bbox.bounds[0]-0.15, bbox.bounds[1]-0.02), size=0.1, color=suit_color[padlock_suit], angle=20, open_lock=True)
            draw_padlock(ax, xy=[xy[0]-1.15, xy[1]+0.3], size=0.2, angle=0, color=suit_color[padlock_suit], ec='w', linewidth=8, open_lock=False)


