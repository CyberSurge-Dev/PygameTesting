from scripts.attributes import *

class Item():
    """Simple class to store all attributes of a Item"""
    def __init__(self, display_name, stackable, *attrubtes):
        """Initialize game Item"""
        self.attributes = attributes
        self.display_name = display_name
        self.stackable = stackable

    def update(self):
        """Updates and check events"""

        for attribute in self.attributes:
            attribute.update()


