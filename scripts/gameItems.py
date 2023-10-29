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
# External imports
import pygame

class Item():
    """Simple class to store all attributes of a Item"""
    def __init__(self, display_name, max_stack, icon, interaction=lambda x,y: None, *attributes):
        """Initialize game Item"""
        self.attributes = attributes
        self.icon = icon
        self.display_name = display_name
        self.max_stack = max_stack
        self.interaction = interaction

    def update(self):
        """Updates the items attributes (ex: Give holder health boost)."""
        for attribute in self.attributes:
            attribute.update(self)

    def hide(self):
        self.icon = pygame.Surface((0, 0))

    def left_button(self, event):
        """Handles the event for the left mouse button."""

    def right_button(self, event):
        """Handles the event for the right mouse button."""

    def copy(self):
        return Item(self.display_name, self.max_stack, self.icon, self.interaction, *self.attributes)

class Weapon(Item):
    """Base class for creating a weapon"""
    def __init__(self, display_name, max_stack, icon, cls, *attributes):
        super().__init__(display_name, max_stack, icon, *attributes)

