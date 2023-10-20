# Created By: Zachary Hoover
# Created Date: 10/16/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains base classes to create gui objects eaily throughout the program

--+ Classes +-- 


"""
# --------------------------------------------------------------------------------
# External imports
import pygame
from scripts.gameItems import *

# --------------------------------------------------------------------------------

class MenuItem():
    """Simple base class for all menu buttons"""

    def __init__(self, pos, size, scale, events, center = True):
        """Initiazlizes the menu item""" ""

        self.pos = pos   
        self.center_pos = (pos[0]-(size[0]//2), pos[1]-(size[1]))
        self.center = center
        self.size = size
        self.events = events
        self.scale = scale

    def render(self, disp):
        """Renders the menu item"""
        if self.center:
            disp.blit(self.image, self.center_pos)
        else:
            disp.blit(self.image, self.pos)

    def check_events(self):
        """Check the events for the menu item"""
        
class Button(MenuItem):
    """Button menu item"""

    def __init__(self, pos, size, scale, image, text, func):
        """Initializes the button"""
        super().__init__(pos, size, scale, [pygame.MOUSEBUTTONDOWN])
        self.text = text
        self.func = func
        self.image = image

    def check_events(self, event):
        """Checks for clicks on button"""
        s_rect = pygame.Rect(int(self.pos[0] * self.scale[0]), int(self.pos[1] * self.scale[1]), 
                           int(self.size[0] * self.scale[0]), int(self.size[1] * self.scale[1]))

        if event.button == 1:  # Left mouse button.
            # Check if the rect collides with the mouse pos.
            if s_rect.collidepoint(event.pos):
                self.func()

        

class ItemBar(MenuItem):
    """Button menu item"""

    def __init__(self, pos, size, scale, image):
        """Initializes the button"""
        super().__init__(pos, size, scale, [pygame.MOUSEWHEEL])
        self.slot_selected = 0
        self.max_items = 4
        self.icon_size = 16
        self.padding = 4
        self.spacing = 3
        self.font = font = pygame.font.Font('freesansbold.ttf', 32)
        self.items = [Item("Test Item", False)] * self.max_items
        self.image = image

    def check_events(self, event):
        """Checks the event for the element"""
        if event.y > 0 and self.slot_selected < self.max_items:
            self.slot_selected += 1
        elif event.y < 0 and self.slot_selected > 0:
            self.slot_selected -= 1
    
    def add_item(self, item, pos):
        """Adds an item to the bar"""
        if self.items < self.max_items:
            self.items[pos] = item

    def remove_item(self, index):
        """Removes an item from the bar"""
        self.items[index] = None
        
    def render(self, disp):
        super().render(disp)
        
        # Index variabel
        i = 0
        while (i < self.max_items):
            if self.center:
                disp.blit(self.items[i].icon, (self.center_pos[0] + (self.padding + self.icon_size*i + self.spacing*i), self.center_pos[1] + self.padding))
            else:
                disp.blit(self.items[i].icon, (self.pos[0] + (self.padding + self.icon_size*i + self.spacing*i), self.pos[1] + self.padding))
            i += 1
            
        # Display current items name above the item bar
        # text = self.font.render(item.display_name, True, (255, 255, 255))
        # textRect = text.get_rect()