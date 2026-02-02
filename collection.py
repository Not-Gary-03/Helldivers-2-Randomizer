"""Helldivers Equipment Randomizer Classes
Gary Hayden May, 2025/01/10, Personal Project
"""

import random
from item import Item

class Collection(Item):
    """data object that contains item objects
    FIXME separate functions that operate on items into a manager class
    """

    def __init__(self, name: str, tags: list, weight=1.0, items=None):
        super().__init__(name, tags, weight)
        if not items:
            self.items = []
        else:
            assert all(isinstance(item, Item) for item in items),\
                "error: Collection can only hold Item objects"
            self.items = items
        self.refresh_weight()

    def __str__(self) -> str:
        """delegates to the str function of Item"""
        return_str = f"""[]//[]//[] {self.name} Collection with weight {self.weight} and tags: {self.tags}. Items:\n"""
        items_str = "\n".join(str(item) for item in self.items)
        return_str += items_str
        return_str += '\n'
        return return_str

    def __repr__(self) -> str:
        return f"Collection({self.name},{self.tags},{self.weight},{self.items})"
    
    def copy(self) -> 'Collection':
        """returns copy of Collection"""
        return Collection(self.name,self.tags,self.weight,self.items)

    def give_names(self) -> list:
        """returns a list of all Item names"""
        return_list = []
        for item in self.items:
            return_list.append(item.name)
        return return_list

    def give_tags(self) -> list:
        """returns a list of all Item tags"""
        return_list = []
        for item in self.items:
            return_list.append(item.tags)
        return return_list

    def give_weights(self) -> list:
        """returns a list of all Item weights"""
        return_list = []
        for item in self.items:
            return_list.append(item.weight)
        return return_list
    
    def refresh_weight(self):
        """sets collection weight to sum of item weights"""
        self.weight = sum(item.weight for item in self.items)
    
    def set_weights(self, new_weight=1):
        """sets all item weights to new_weight"""
        for item in self.items:
            item.weight = new_weight
        self.refresh_weight()

    def isempty(self) -> bool:
        """returns true if items list is empty"""
        return len(self.items) == 0
    
    def isempty_weight(self) -> bool:
        """returns true if weight is zero, indicating all items have zero weight"""
        return self.weight == 0

    def rand_select_item(self) -> 'Item':
        """randomly selects an Item from the list of items"""
        self.refresh_weight()
        if self.weight == 0:
            return random.choice(self.items)
            # if all weights are zero, ignore weighted selection and choose completely randomly
        else:
            return random.choices(self.items,weights=self.give_weights(),k=1)[0]
            # weighted random selection using random.choices, k=1 to return single item in list

    def aggregate_or(self, target: list, recursive=False) -> 'Collection':
        """returns a collection of items that have at least one or more target tag(s)"""
        return_list = []
        if recursive:
            for item in self.items:
                if any(tag in item.tags for tag in target):
                    if isinstance(item, Collection):
                        temp_col = item.aggregate_or(target, recursive=True)
                        return_list.extend(temp_col.items)
                    else:
                        return_list.append(item)
        else:
            for item in self.items:
                if any(tag in item.tags for tag in target):
                    return_list.append(item)
        return_col = Collection(self.name, self.tags, self.weight, return_list)
        return_col.refresh_weight()
        return return_col
    
    def aggregate_and(self, target: list, recursive=False) -> 'Collection':
        """returns a collection of items that have at least one or more target tag(s)"""
        return_list = []
        if recursive:
            for item in self.items:
                if all(tag in item.tags for tag in target):
                    if isinstance(item, Collection):
                        temp_col = item.aggregate_or(target, recursive=True)
                        return_list.extend(temp_col.items)
                    else:
                        return_list.append(item)
        else:
            for item in self.items:
                if all(tag in item.tags for tag in target):
                    return_list.append(item)
        return_col = Collection(self.name, self.tags, self.weight, return_list)
        return_col.refresh_weight()
        return return_col
    
    def remove_i(self, target: int | str | Item):
        """removes Item object at index or with first matching name/object"""

        if isinstance(target, int):  # Remove by index
            assert 0 <= target < len(self.items), "Index out of range"
            del self.items[target]

        elif isinstance(target, str):  # Remove by name
            for item in self.items:
                if item.name == target:
                    self.items.remove(item)
                    return
            print(f"No item found with name '{target}'!")

        elif isinstance(target, Item):  # Remove by object reference
            try:
                self.items.remove(target)
            except ValueError:
                print("Item not found in collection!")

        else:
            print("Invalid input type for remove_i!")

    def remove_i_weight(self, target: int | str | Item):
        """removes Item object at index or with first matching name/object"""

        if isinstance(target, int):  # Remove by index
            assert 0 <= target < len(self.items), "Index out of range"
            self.items[target].weight = 0
            self.refresh_weight()

        elif isinstance(target, str):  # Remove by name
            for item in self.items:
                if item.name == target:
                    item.weight = 0
                    self.refresh_weight()
                    return
            print(f"No item found with name '{target}'!")

        elif isinstance(target, Item):  # Remove by object reference
            try:
                # self.items.remove(target)
                target.weight = 0
                self.refresh_weight()
            except ValueError:
                print("Item not found in collection!")

        else:
            print("Invalid input type for remove_i!")
