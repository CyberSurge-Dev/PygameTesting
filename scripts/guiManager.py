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
# External imports 
import pygame


class GUIManager():
    """Class to manager all menu items"""
    def __init__(self):
        self.menu_items = {}
        self.ignore_events = []
        self.background_tint = False

    def render(self, disp):
        """Render all menu items"""
        if self.background_tint:
            disp.fill((10, 10, 10, 250), special_flags=pygame.BLEND_SUB)
        for key, item in self.menu_items.items():
            if key not in self.ignore_events:
                item.render(disp)

    def check_events(self, event):
        """Check for events"""
        delete = []
        for key, item in self.menu_items.items():
            if item.delete == True:
                delete.append(key)
            if event.type in item.events and key not in self.ignore_events:
                item.check_events(event)

        for key in delete:
            self.remove(key)

    def add(self, key, menu_item):
        """Adds passed in item to menu"""""
        self.menu_items[key] = menu_item

    def remove(self, key):
        """Removes passed in item from menu"""
        try:
            del self.menu_items[key]
        except: pass

    def ignore(self, *keys):
        """Add keys to ignore check_events() list"""
        for key in keys:
            self.ignore_events.append(key)

    def unignore(self, *keys):
        for key in keys:
            try:
                while key in self.ignore_events:
                    self.ignore_events.remove(key)
            except: pass

    def reset_ignore(self):
        """Remove keys from ignore check_events() list"""
        self.ignore_events = []
            
