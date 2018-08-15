"""
Analysis of changes  to IE.
"""
import numpy as np
import matplotlib.pyplot as plt


def create_plot(old_numbers, new_numbers, xaxis, xlabel, ylabel, title):
    old_plot, = plt.plot(xaxis, old_numbers, label="Pre 8.11")
    new_plot, = plt.plot(xaxis, new_numbers, label="8.11")
    plt.grid()
    plt.title(title)
    plt.legend(handles=[old_plot, new_plot])
    plt.xticks(np.arange(0, 1.1, step=0.10), np.arange(0, 110, step= 10))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def same_ad_crit():
    crit_chance = 0.3
    armor_damage_reduction = 1 - np.arange(0, 1, 0.01)

    old_ie = 2.5 * armor_damage_reduction * crit_chance + \
             1 * armor_damage_reduction * (1 - crit_chance)

    new_ie = (1.70 * armor_damage_reduction + 0.30) * (2 * crit_chance) + \
             1 * armor_damage_reduction * (1 - 2 * crit_chance)

    create_plot(old_ie, new_ie, armor_damage_reduction,
                "Percent Physical Damage Dealt (After Armor)", "Damage Per AD",
                "IE Comparison: 30% Crit (One Zeal Item)")

    return


def item_set_comparison():
    armor_damage_reduction = 1 - np.arange(0, 1, 0.01)

    # Old Item Set: ER, Shiv, IE (Old)
    old_ad = 70 + 70
    old_crit =  0.20 + 0.30 + 0.20
    # New Item Set: Stormrazor, Shiv, IE (New)
    new_ad = 70 + 80
    new_crit = 0.30 * 2

    # dpa: damager per auto
    old_dpa = old_ad * (2.5 * armor_damage_reduction * old_crit + \
             1 * armor_damage_reduction * (1 - old_crit))

    new_dpa = new_ad * ((1.70 * armor_damage_reduction + 0.30) * (2 * new_crit) + \
             1 * armor_damage_reduction * (1 - 2 * new_crit))

    create_plot(old_dpa, new_dpa, armor_damage_reduction,
                "Percent Physical Damage Dealt (After Armor)",
                "Damage Per Attack",
                "Item Comparison: ER, Shiv, Old IE vs. Stormrazor, Shiv, New IE")

    return


def main():
    # same_ad_crit()
    item_set_comparison()
    return


if __name__ == '__main__':
    main()
