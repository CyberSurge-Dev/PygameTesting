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

# Internal imports
from scripts.utils import blit

# --------------------------------------------------------------------------------


class MenuItem():
    """Simple base class for all menu buttons"""

    def __init__(self, pos, size, scale, events, center=True):
        """Initiazlizes the menu item""" ""

        self.pos = pos
        self.center_pos = (pos[0] - (size[0] // 2), pos[1] - (size[1]))
        self.center = center
        self.size = size
        self.events = events
        self.scale = scale

    def render(self, disp):
        """Renders the menu item"""
        if self.center:
            blit(disp, self.image, self.center_pos)
        else:
            blit(disp, self.image, self.pos)

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
        s_rect = pygame.Rect(int(self.pos[0] * self.scale[0]),
                             int(self.pos[1] * self.scale[1]),
                             int(self.size[0] * self.scale[0]),
                             int(self.size[1] * self.scale[1]))

        if event.button == 1:  # Left mouse button.
            # Check if the rect collides with the mouse pos.
            if s_rect.collidepoint(event.pos):
                self.func()


class ItemBar(MenuItem):
    """Button menu item"""

    def __init__(self, pos, size, scale, image, selected_image):
        """Initializes the ItemBar"""
        super().__init__(pos, size, scale, [pygame.MOUSEWHEEL, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        self.slot_selected = 0
        self.max_items = 4
        self.icon_size = 16
        self.padding = 4
        self.spacing = 3
        self.font = pygame.font.Font('freesansbold.ttf', 8)
        self.items = [None] * self.max_items
        self.image = image
        self.selected_image = selected_image
        if self.items[self.slot_selected] != None:
            self.text = self.font.render(self.items[self.slot_selected].display_name, True, (255, 250, 250))

    def check_events(self, event):
        """Checks the event for the element"""
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0 and self.slot_selected < self.max_items - 1:
                self.slot_selected += 1
            elif event.y < 0 and self.slot_selected > 0:
                self.slot_selected -= 1

        elif event.type == pygame.KEYDOWN:
            # Check if max items is less than 10
            if self.max_items > 10:
                raise ValueError("Max items cannot be greater than 10")
            else:
                # Check each number key 0-9 to select slot
                for index in range(1, self.max_items + 1):
                    if event.key == getattr(pygame.locals, f"K_{index}"):
                        self.slot_selected = index - 1

        if self.items[self.slot_selected] != None:
            self.text = self.font.render(self.items[self.slot_selected].display_name, True, (255, 250, 250))

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
            if self.items[i] != None:
                if self.center:
                    disp.blit(
                        self.items[i].icon,
                        (self.center_pos[0] +
                         (self.padding + self.icon_size * i + self.spacing * i),
                         self.center_pos[1] + self.padding))
                else:
                    disp.blit(
                        self.items[i].icon,
                        (self.pos[0] +
                         (self.padding + self.icon_size * i + self.spacing * i),
                         self.pos[1] + self.padding))
            i += 1

            # Display selected icon
            disp.blit(
                self.selected_image,
                (self.center_pos[0] +
                 (self.padding - 1 + self.icon_size * self.slot_selected +
                  self.spacing * self.slot_selected),
                 self.center_pos[1] + self.padding - 1))

        # Display current items name above the item bar
        if self.items[self.slot_selected] != None:
            disp.blit(self.text, ((self.center_pos[0]+(self.size[0]/2))-self.text.get_width()/2, self.center_pos[1]-self.text.get_height()))
