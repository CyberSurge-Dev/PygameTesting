# Created By: Zachary Hoover
# Created Date: 9/26/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains the classes for game items such as weapons, tools, consumables, accessories, etc.

--+ Classes +-- 
Item(display_name, stackable, *attributes) - Simple class to store all attributes of a Item 

"""
# --------------------------------------------------------------------------------

from scripts.assetMap import AssetMap
from scripts.utils import load_image


class Item():
    """Simple class to store all attributes of a Item"""
    def __init__(self, display_name, stackable, *attributes):
        """Initialize game Item"""
        self.attributes = attributes
        self.icon = load_image('items/test/sample.png')
        self.display_name = display_name
        self.stackable = stackable

    def update(self):
        """Updates and check events"""

        for attribute in self.attributes:
            attribute.update()


