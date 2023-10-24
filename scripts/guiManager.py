# Created By: Zachary Hoover
# Created Date: 10/16/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains base classes to create gui objects eaily throughout the program

--+ Classes +-- 
GUIManager() - Gui object, acts as a way to group GUI objects together

"""
# --------------------------------------------------------------------------------

class GUIManager():
    """Class to manager all menu items"""
    def __init__(self):
        self.menu_items = {}
        self.ignore_events = []

    def render(self, disp):
        """Render all menu items"""
        for item in self.menu_items.values():
            item.render(disp)

    def check_events(self, event):
        """Check for events"""
        for key, item in self.menu_items.items():
            if event.type in item.events and key not in self.ignore_events:
                item.check_events(event)

    def add(self, key, menu_item):
        """Adds passed in item to menu"""""
        self.menu_items[key] = menu_item

    def remove(self, key):
        """Removes passed in item from menu"""
        del self.menu_items[key]

    def ignore(self, *keys):
        """Add keys to ignore check_events() list"""
        self.ignore_events.append(keys)

    def reset_ignore(self):
        """Remove keys from ignore check_events() list"""
        self.ignore_events = []
            
