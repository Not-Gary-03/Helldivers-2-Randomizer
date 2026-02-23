"""Helldivers Equipment Randomizer Classes
Gary Hayden May, 2025/01/10, Personal Project
"""

class Item:
    """data object with a name and list of tags
    only has functions for string representation and equality comparison
    """
    def __init__(self, name: str, tags: list=None, weight=1):
        self.name = name
        if tags:
            self.tags = sorted(tags)
        else:
            self.tags = []
        self.weight = weight

    def __str__(self) -> str:
        # return f"{self.name}, weight: {self.weight}"
        return f"{self.name}, tags: {self.tags}, weight: {self.weight}"

    def __repr__(self) -> str:
        return f"Item({self.name},{self.tags},{self.weight})"

    def __eq__(self, other: 'Item') -> bool:
        return self.name == other.name
