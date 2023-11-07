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
    def __init__(self, display_name, max_stack, icon, interaction=None, left_button=None, right_button=None, show_when_held=False, meta={}, *attributes):
        """Initialize game Item"""
        self.attributes = attributes
        self.icon = icon
        self.display_name = display_name
        self.l_button = left_button
        self.r_button = right_button
        self.max_stack = max_stack
        self.interaction = interaction
        self.show_when_held = show_when_held
        self.meta = meta

    def update(self):
        """Updates the items attributes (ex: Give holder health boost)."""
        for attribute in self.attributes:
            attribute.update(self)

    def interact(self, *args):
        """Interaction with object (When out of inventory)"""
        if self.interaction != None:
            self.interaction(self, *args)

    def hide(self):
        self.icon = pygame.Surface((0, 0))

    def is_interactable(self):
        return self.interaction != None

    def left_button(self, *args):
        """Handles the event for the left mouse button."""
        print(self.l_button)
        if self.l_button != None:
            self.l_button(self, *args)
        
    def right_button(self, *args):
        """Handles the event for the right mouse button."""
        if self.r_button != None:
            self.r_button(self, *args)
            
    def copy(self):
        return Item(self.display_name, self.max_stack, self.icon, self.interaction, self.l_button, self.r_button, self.show_when_held, self.meta.copy(), *self.attributes)
