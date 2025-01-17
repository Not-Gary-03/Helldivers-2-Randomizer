"""Helldivers Equipment Randomizer Classes
Gary Hayden May, 2025/01/09, Personal Project
"""

import random

class Possessions:
    """class representing the content an individual owns"""

    def __init__(self, name: str, content: list, strat_content: list, primaries: list,\
                 secondaries: list, throwables: list, stratagems: list,\
                 boosters: list, armor: list, capes: list):
        """gather content"""
        self.name = name
        self.content = content
        nums = len(content)
        self.primaries, self.secondaries, self.throwables, self.stratagems,\
            self.boosters, self.armor, self.capes = [], [], [], [], [], [], []
        for i in range(nums):
            self.primaries.extend(primaries[content[i]])
        for i in range(nums):
            self.secondaries.extend(secondaries[content[i]])
        for i in range(nums):
            self.throwables.extend(throwables[content[i]])
        for i in range(nums):
            self.boosters.extend(boosters[content[i]])
        for i in range(nums):
            self.armor.extend(armor[content[i]])
        for i in range(nums):
            self.capes.extend(capes[content[i]])

        self.stratagems.extend(stratagems[:5])
        self.strat_content = [0,1,2,3,4,5]
        self.strat_content.extend(strat_content)
        for _, strat in enumerate(strat_content):
            self.stratagems.extend(stratagems[strat])


    def __str__(self) -> str:
        """Show content owned"""
        string = f"{self.name}'s Primaries::: "
        string += str(self.primaries)
        string += "\nSecondaries::: "
        string += str(self.secondaries)
        string += "\nThrowables::: "
        string += str(self.throwables)
        string += "\nStratagems::: "
        string += str(self.stratagems)
        return string

    def randomize_primaries_single(self) -> str:
        """Returns a single randomly selected primary as a string"""
        return str(self.primaries[random.randint(0, len(self.primaries) - 1)])

    def randomize_secondaries_single(self) -> str:
        """Returns a single randomly selected secondary as a string"""
        return str(self.secondaries[random.randint(0, len(self.secondaries) - 1)])

    def randomize_throwables_single(self) -> str:
        """Returns a single randomly selected throwable as a string"""
        return str(self.throwables[random.randint(0, len(self.throwables) - 1)])

    def randomize_boosters_single(self) -> str:
        """Returns a single randomly selected booster as a string"""
        return str(self.boosters[random.randint(0, len(self.boosters) - 1)])

    def randomize_armor_single(self) -> str:
        """Returns a single randomly selected armor as a string"""
        return str(self.armor[random.randint(0, len(self.armor) - 1)])

    def randomize_capes_single(self) -> str:
        """Returns a single randomly selected cape as a string"""
        return str(self.capes[random.randint(0, len(self.capes) - 1)])

    def randomize_loadout_weapons(self) -> str:
        """Generates a random selection of primary, secondary, and throwable, and
            returns it as a string
        """
        string = f"{self.name}'s Loadout: ["
        string += str(self.primaries[random.randint(0, len(self.primaries) - 1)])
        string += "], ["
        string += str(self.secondaries[random.randint(0, len(self.secondaries) - 1)])
        string += "], ["
        string += str(self.throwables[random.randint(0, len(self.throwables) - 1)])
        string += "], Booster: ["
        string += str(self.boosters[random.randint(0, len(self.boosters) - 1)])
        string += "]"
        return string

    def randomize_loadout_other(self) -> str:
        """Generates a random selection of primary, secondary, and throwable, and
            returns it as a string
        """
        string = f"{self.name}'s Armor: ["
        string += str(self.armor[random.randint(0, len(self.armor) - 1)])
        string += "], Helmet: ["
        string += str(self.armor[random.randint(0, len(self.armor) - 1)])
        string += "], Cape: ["
        string += str(self.capes[random.randint(0, len(self.capes) - 1)])
        string += "]"
        return string

    def test_single_randomization(self, count: int, func):
        """takes one of this classes' randomize_x_single functions and tests how
            many times each result is received when ran an arbitrary number of times.
        """
        count_dict = {}
        for _ in range(count):
            result = func()
            if result in count_dict:
                count_dict[result] += 1
            else:
                count_dict[result] = 1
        print(count_dict)
