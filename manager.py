"""Helldivers Equipment Randomizer Classes
Gary Hayden May, 2025/12/18, Personal Project
"""

import random
from item import Item
from collection import Collection

class Manager:
    """manager class that operates on Collection objects"""

    def __init__(self):
        pass
    
    def testmethod(self, col: Collection) -> Collection:
        """returns collection with first three items in input collection"""
        return Collection(col.name, col.tags, col.weight, col.items[:3])
    
    def aggregate_or(self, col: Collection, target: list) -> 'Collection':
        """returns a collection of items that have at least one or more target tag(s)"""
        return_list = []
        for item in col.items:
            if any(tag in item.tags for tag in target):
                return_list.append(item)
        return_col = Collection(col.name, col.tags, col.weight, return_list)
        return return_col

    def aggregate_and(self, col: Collection, target: list) -> 'Collection':
        """returns a collection of items that have all target tags"""
        return_list = []
        for item in col.items:
            if all(tag in item.tags for tag in target):
                return_list.append(item)
        return_col = Collection(col.name, col.tags, col.weight, return_list)
        return return_col

    def aggregate_nor(self, col: Collection, target: list) -> 'Collection':
        """returns a collection of items that have none of the target tags"""
        return_list = []
        for item in col.items:
            if not any(tag in item.tags for tag in target):
                return_list.append(item)
        return_col = Collection(col.name, col.tags, col.weight, return_list)
        return return_col

    def aggregate_nand(self, col: Collection, target: list) -> 'Collection':
        """returns a collection of items that do not have all target tags"""
        return_list = []
        for item in col.items:
            if not all(tag in item.tags for tag in target):
                return_list.append(item)
        return_col = Collection(col.name, col.tags, col.weight, return_list)
        return return_col

    def aggregate_xor(self, col: Collection, target:list, x: int) -> 'Collection':
        """returns a collection of items that have exactly 'x' of the target tags"""
        return_list = []
        for item in col.items:
            if len(set(target) & set(item.tags)) == x:
                return_list.append(item)
        return_col = Collection(col.name, col.tags, col.weight, return_list)
        return return_col

    def remove_i(self, col: Collection, target: int | str | Item):
        """removes Item object at index or with first matching name/object"""

        if isinstance(target, int):  # Remove by index
            assert 0 <= target < len(col.items), "Index out of range"
            del col.items[target]

        elif isinstance(target, str):  # Remove by name
            for item in col.items:
                if item.name == target:
                    col.items.remove(item)
                    return
            print(f"No item found with name '{target}'!")

        elif isinstance(target, Item):  # Remove by object reference
            try:
                col.items.remove(target)
            except ValueError:
                print("Item not found in collection!")

        else:
            print("Invalid input type for remove_i!")