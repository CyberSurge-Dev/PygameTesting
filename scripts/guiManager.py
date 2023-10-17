# Created By: Zachary Hoover
# Created Date: 10/16/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains base classes to create gui objects eaily throughout the program

--+ Classes +-- 


"""
# --------------------------------------------------------------------------------

class GUIManager():
    """Class to manager all menu items"""
    def __init__(self):
        self.menu_items = {}

    def render(self, disp):
        """Render all menu items"""
        for item in self.menu_items.values():
            item.render(disp)

    def check_events(self, event):
        """Check for events"""
        for item in self.menu_items.values():
            item.check_events()

    def add(self, key, menu_item):
        """Adds passed in item to menu"""""
        self.menu_items[key] = menu_item

    def remove(self, key):
        """Removes passed in item from menu"""
        del self.menu_items[key]

            
