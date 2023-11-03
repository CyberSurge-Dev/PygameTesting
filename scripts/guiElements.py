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
from scripts.utils import blit, render_font

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
        self.image = None
        self.delete = False

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
        if self.center:
            s_rect = pygame.Rect(int(self.center_pos[0] * self.scale[0]),
                                int(self.center_pos[1] * self.scale[1]),
                                int(self.size[0] * self.scale[0]),
                                int(self.size[1] * self.scale[1]))
        else:
            s_rect = pygame.Rect(int(self.center_pos[0] * self.scale[0]),
                                int(self.center_pos[1] * self.scale[1]),
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
        self.counts = []
        self.font = pygame.font.Font('freesansbold.ttf', 8)
        self.font_small = pygame.font.Font('freesansbold.ttf', 4)
        self.items = [(None, 0)] * self.max_items
        self.image = image
        self.selected_image = selected_image
        for i in range(0, self.max_items):
            self.counts.append(self.font_small.render("", True, (255, 250, 250)))
        if self.items[self.slot_selected][0] != None:
            self.text = self.font.render(self.items[self.slot_selected][0].display_name, True, (255, 250, 250))
        else:
            self.text = self.font.render("", True, (255, 250, 250))

    def update_counts(self):
        for i in range(0, self.max_items):
            self.counts[i] = self.font_small.render(str(self.items[i][1]), True, (255, 250, 250))

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

        if self.items[self.slot_selected][0] != None:
            self.text = self.font.render(self.items[self.slot_selected][0].display_name, True, (255, 250, 250))
        self.update_counts()

    def add_item(self, item, pos):
        """Adds an item to the bar"""
        if self.items < self.max_items:
            self.items[pos] = item

    def remove_item(self, index):
        """Removes an item from the bar"""
        self.items[index] = (None, 0)

    def render(self, disp):
        super().render(disp)

        # Index variabel
        i = 0
        while (i < self.max_items):
            if self.items[i][0] != None:
                if self.center:
                    pos = (self.center_pos[0] +
                         (self.padding + self.icon_size * i + self.spacing * i),
                         self.center_pos[1] + self.padding)
                    blit(disp, self.items[i][0].icon, pos)
                    blit(disp, self.counts[i], pos)
                    
                else:
                    disp.blit(
                        self.items[i][0].icon,
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
        if self.items[self.slot_selected][0] != None:
            disp.blit(self.text, ((self.center_pos[0]+(self.size[0]/2))-self.text.get_width()/2, self.center_pos[1]-self.text.get_height()))

class TextBox(MenuItem):
    """Class to create a text-box on the screen"""
    def __init__(self, pos, scale, image, text, center=True):
        super().__init__(pos, (160, 40), scale, [], center)
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        self.padding = 4
        self.text = []
        self.image = image
        for t in text:
            self.text.append(self.font.render(t, True, (255, 250, 250)))

    def render(self, disp):
        super().render(disp)
        if self.center:
            temp_pos = [self.center_pos[0]+self.padding, self.center_pos[1]+self.padding]
            for font in self.text:
                render_font(font, self.scale, temp_pos)
                temp_pos[1] += self.font.get_height()

class ClosableTextBox(MenuItem):
    """Class to create a text-box on the screen"""
    def __init__(self, pos, scale, box_image, button_image, text, center=True):
        super().__init__(pos, (box_image.get_width(), box_image.get_height()), scale, [pygame.MOUSEBUTTONDOWN], center)
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        self.padding = 2
        self.image = box_image
        self.text = []
        if self.center:
            self.button = Button((self.center_pos[0] + self.image.get_width()+self.padding*2, self.center_pos[1]+button_image.get_height()), (button_image.get_width(), button_image.get_height()), scale, button_image, "", self.close)
        for t in text:
            self.text.append(self.font.render(t, True, (255, 250, 250)))
        
    def close(self):
        self.delete = True
        print("removed.")

    def check_events(self, event):
        self.button.check_events(event)

    def render(self, disp):
        super().render(disp)
        if self.center:
            temp_pos = [self.center_pos[0]+self.padding*4, self.center_pos[1]+self.padding]
            for font in self.text:
                render_font(font, self.scale, temp_pos)
                temp_pos[1] += self.font.get_height()-4
        self.button.render(disp)
                
            
class Inventory(MenuItem):
    def __init__(self, pos, size, scale,  inventory_image, selected_image, itembar, game, center=True):
        super().__init__(pos, size, scale, [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP], center=True)
        self.image = inventory_image
        self.selected_image = selected_image
        self.font_title = pygame.font.Font('freesansbold.ttf', 8)
        self.font_count = pygame.font.Font('freesansbold.ttf', 4)
        self.columns = 4
        self.rows = 3
        self.padding = 3
        self.spacing = 3
        self.icon_size = 16
        self.inventory = {}
        self.held = False
        self.counts = {}
        self.itembar = itembar
        self.game = game
        self.mouse_pos = (0,0)
        for x in range(0, self.columns):
            for y in range(0, self.rows):
                self.inventory[(x,y)] = (None, 0)
        for x in range(0, self.columns):
            for y in range(0, self.rows):
                self.counts[(x,y)] = self.font_count.render("", True, (255, 250, 250))
        self.selcted = None        

    def update_count_fonts(self):
        for loc in self.inventory:
            self.counts[loc] = self.font_count.render(str(self.inventory[loc][1]), True, (255, 250, 250))

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.held = True

            if self.center:
                # Check for inventory click
                for loc in self.inventory:
                    rect = pygame.Rect((int((self.center_pos[0]+self.padding+loc[0]*(self.icon_size+2)+loc[0])*self.scale[0]), int((self.center_pos[1]+11+loc[1]*(self.icon_size+2)+loc[1])*self.scale[1])), 
                                       (int(18*self.scale[0]), int(18*self.scale[1])))
                    if rect.collidepoint(event.pos):
                        self.selcted = (loc, 'inventory', self.inventory.get(loc, None))
                for loc in range(0, self.itembar.max_items):
                    rect = pygame.Rect((int((self.center_pos[0]+self.padding+loc*(self.icon_size+2)+loc)*self.scale[0]),
                                        int((self.center_pos[1]+74)*self.scale[1])
                                        ), (int(18*self.scale[0]), int(18*self.scale[1])))
                    if rect.collidepoint(event.pos):
                        self.selcted = (loc, 'itembar', self.itembar.items[loc])
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.held = False
            # Check for inventory click
            for loc in self.inventory:
                rect = pygame.Rect((int((self.center_pos[0]+self.padding+loc[0]*(self.icon_size+2)+loc[0])*self.scale[0]), int((self.center_pos[1]+11+loc[1]*(self.icon_size+2)+loc[1])*self.scale[1])), 
                                       (int(18*self.scale[0]), int(18*self.scale[1])))
                if rect.collidepoint(event.pos):
                    if self.selcted[1] == 'inventory':
                        self.inventory[self.selcted[0]] = self.inventory[loc]
                        self.inventory[loc] = self.selcted[2]
                    else:
                        self.itembar.items[self.selcted[0]] = self.inventory[loc]
                        self.inventory[loc] = self.selcted[2]
                    self.selcted = (loc, 'inventory', self.inventory.get(loc, None))

            for loc in range(0, self.itembar.max_items):
                rect = pygame.Rect((int((self.center_pos[0]+self.padding+loc*(self.icon_size+2)+loc)*self.scale[0]),
                                        int((self.center_pos[1]+74)*self.scale[1])
                                        ), (int(18*self.scale[0]), int(18*self.scale[1])))
                if rect.collidepoint(event.pos):
                    if self.selcted[1] == 'inventory':
                        self.inventory[self.selcted[0]] = self.itembar.items[loc]
                        self.itembar.items[loc] = self.selcted[2]
                    else:
                        self.itembar.items[self.selcted[0]] = self.itembar.items[loc]
                        self.itembar.items[loc] = self.selcted[2]
                    self.selcted = (loc, 'itembar', self.itembar.items[loc])
        self.update_count_fonts()
                        
    def render(self, disp):
        super().render(disp)

        # Render selected image
        if self.selcted != None and self.selcted[1] == 'inventory':
            blit(disp, self.selected_image, (
                self.center_pos[0]+self.padding+self.selcted[0][0]*(self.icon_size+2)+self.selcted[0][0],
                self.center_pos[1]+11+self.selcted[0][1]*(self.icon_size+2)+self.selcted[0][1]
            ))
        elif self.selcted != None and self.selcted[1] == 'itembar':
            blit(disp, self.selected_image, (
                self.center_pos[0]+self.padding+self.selcted[0]*(self.icon_size+2)+self.selcted[0],
                self.center_pos[1]+74
            ))

        # Render inventory items
        for loc in self.inventory:
            if self.inventory[loc][0] != None:
                pos = (
                    self.center_pos[0]+self.padding+loc[0]*(self.icon_size+2)+loc[0]+1,
                    self.center_pos[1]+11+loc[1]*(self.icon_size+2)+loc[1]+1
                )
                blit(disp, self.inventory[loc][0].icon, pos)
                blit(disp, self.counts[loc], pos)
        # Render ItemBar items
        for loc in range(0, self.itembar.max_items):
            if self.itembar.items[loc][0] != None:
                pos = (
                    self.center_pos[0]+self.padding+loc*(self.icon_size+2)+loc+1,
                    self.center_pos[1]+75
                )
                blit(disp, self.itembar.items[loc][0].icon, pos)
                blit(disp, self.itembar.counts[loc], pos)
        
        if self.held and self.selcted != None and self.selcted[2][0] != None:
            mx, my = pygame.mouse.get_pos()
            icon = self.selcted[2][0].icon
            blit(disp, icon, (mx/self.scale[0]-int(icon.get_width()//2), 
                              my/self.scale[1]-int(icon.get_height()//2)))

    def add(self, item):
        for i in range(0, len(self.itembar.items)):
            if self.itembar.items[i][0] == None or (self.itembar.items[i][0].display_name == item.display_name and self.itembar.items[i][1] < item.max_stack):
                self.itembar.items[i] = (item, self.itembar.items[i][1]+1)
                return
        for x in self.inventory:
            if self.inventory[x][0] == None or (self.inventory[x][0].display_name == item.display_name and self.inventory[x][1] < item.max_stack):
                self.inventory[x] = (item, self.inventory[x][1]+1)
                return

class HealthBar(MenuItem):
    """Class for the health bar. Each bar is 5 health"""
    def __init__(self, pos, size, scale, events, health_emblem, empty_bar, filled_bar, max_health, health, center=True):
        super().__init__(pos, size, scale, events, center)

        self.max_health = max_health
        self.health = health
        self.emblem = health_emblem
        self.empty_bar = empty_bar
        self.filled_bar = filled_bar
        self.health_per_bar = 10
        self.step = 21
        self.immunity_frames = 20
        self.tick = 0
        self.damaged = False
        self.dead = False

    def render(self, disp):
        if self.center:
            for i in range(0, self.max_health // self.health_per_bar):
                if self.health > i * self.health_per_bar:
                    blit(
                        disp, self.filled_bar, (
                            20 + self.center_pos[0] + self.step * i,
                            self.center_pos[1] + 5
                        ))
                else:
                    blit(
                    disp, self.empty_bar, (
                        20 + self.center_pos[0] + self.step * i,
                        self.center_pos[1] + 5
                    ))
            blit(disp, self.emblem, self.center_pos)
        if self.damaged:
            if self.tick >= self.immunity_frames:
                self.tick = 0
                self.damaged = False
            else:
                self.tick += 1
        if self.health <= 0:
            self.dead = True
                
    def damage(self, damage_amount):
        if not self.damaged:
            self.health -= damage_amount
            self.damaged = True
            
class GameOver(MenuItem):
    """Class for GameOver Screen"""
    def __init__(self, pos, size, scale, game_over_image, respawn_button, func, center=True):
        super().__init__(pos, size, scale, [pygame.MOUSEBUTTONDOWN], center)
        self.image = game_over_image
        self.respawn_button = respawn_button
        self.button = Button(
           (self.center_pos[0], self.center_pos[1]+self.image.get_height()+40),
           (self.respawn_button.get_width(), self.respawn_button.get_height()),
           self.scale,
           self.respawn_button,
           "", func
        )
        
    def render(self, disp):
        """Render the images"""
        blit(disp, self.image, (self.center_pos[0]-self.respawn_button.get_width()//4, self.center_pos[1]))
        self.button.render(disp)
        
    def check_events(self, event):
        """Checks the event for the object"""
        self.button.check_events(event)
        
        
        

        
                    
                
                
        
        
    
        

        

    
        


