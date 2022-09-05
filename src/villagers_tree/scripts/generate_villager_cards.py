import os

import pandas as pd
import matplotlib.pyplot as plt

import villagers_tree
from villagers_tree.cards import draw_villager_card

def main():
    module_dir = villagers_tree.__path__[0]
    data_dir = os.path.abspath(f"{module_dir}/../../data/")
    output_dir = os.path.abspath(f"{module_dir}/../../output/")

    villagers_data = pd.read_csv(f"{data_dir}/villagers.csv")
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

    if not os.path.exists(f"{output_dir}/villager_cards/"):
        os.makedirs(f"{output_dir}/villager_cards")
    for v in villagers:
        figure.clf()
        draw_villager_card(figure.gca(), villagers[v], xy=[0, 0])
        figure.gca().set_xlim(-21*0.075, 21*0.075)
        figure.gca().set_ylim(-9*0.075, 9*0.075)
        figure.gca().axis('off')
        figure.savefig(f"{output_dir}/villager_cards/{v}.png")


if __name__ == '__main__':
    main()
