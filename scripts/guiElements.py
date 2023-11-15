# Created By: Zachary Hoover
# Created Date: 10/16/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains base classes to create gui objects eaily throughout the program
"""
# --------------------------------------------------------------------------------
# External imports
import pygame
import json

# Internal imports
from scripts.utils import blit, render_font
from scripts.itemAttributes import Accessory
from scripts.utils import convert_time

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
        self.font = pygame.font.Font('freesansbold.ttf', int(8*self.scale[1]))
        self.font_small = pygame.font.Font('freesansbold.ttf', int(5*self.scale[1]))
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
                    render_font(self.counts[i], self.scale, (pos[0]+2, pos[1]+2))
                    
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
            render_font(self.text, self.scale, ((self.center_pos[0]+(self.size[0]/2))-(self.text.get_width()//self.scale[1])/2, self.center_pos[1]-self.text.get_height()//self.scale[1]))

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
    def __init__(self, pos, scale, box_image, button_image, text, on_close=None, center=True, *args):
        super().__init__(pos, (box_image.get_width(), box_image.get_height()), scale, [pygame.MOUSEBUTTONDOWN], center)
        self.font = pygame.font.Font('freesansbold.ttf', int(7*self.scale[1]))
        self.padding = 4
        self.image = box_image
        self.text = []
        self.args = args
        self.on_close = on_close
        if self.center:
            self.button = Button((self.center_pos[0] + self.image.get_width()+self.padding*2, self.center_pos[1]+button_image.get_height()), (button_image.get_width(), button_image.get_height()), scale, button_image, "", self.close)
        for t in text:
            self.text.append(self.font.render(t, True, (255, 250, 250)))
        
    def close(self):
        self.delete = True
        print(self.on_close)
        if self.on_close != None:
            self.on_close(*self.args)

    def check_events(self, event):
        self.button.check_events(event)

    def render(self, disp):
        super().render(disp)
        if self.center:
            temp_pos = [self.center_pos[0]+self.padding, self.center_pos[1]+self.padding]
            for font in self.text:
                render_font(font, self.scale, temp_pos)
                temp_pos[1] += self.font.get_height()//self.scale[1]+2
        self.button.render(disp)
                
            
class Inventory(MenuItem):
    def __init__(self, pos, size, scale,  inventory_image, selected_image, itembar, game, center=True):
        super().__init__(pos, size, scale, [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP], center=True)
        self.image = inventory_image
        self.selected_image = selected_image
        self.font_title = pygame.font.Font('freesansbold.ttf', 8)
        self.font_count = pygame.font.Font('freesansbold.ttf', int(4*self.scale[1]))
        self.columns = 4
        self.rows = 3
        self.padding = 3
        self.spacing = 3
        self.icon_size = 16
        self.inventory = {}
        self.held = False
        self.counts = {}
        self.itembar = itembar
        self.max_accessories = 3
        self.accsessories = [(None, 0)] * self.max_accessories
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

    def update_accessories(self, *args):
        """Update each accessory"""
        for accessory in self.accsessories:
            if accessory[0] != None:
                accessory[0].update(*args)

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

                for loc in range(0, self.max_accessories):
                    rect = pygame.Rect(
                        (
                         (self.center_pos[0]+86)*self.scale[0],
                         int((self.center_pos[1]+3+loc*(self.icon_size+2)+loc)*self.scale[1])
                         ),
                        (int(18*self.scale[0]), int(18*self.scale[1]))
                    )
                    if rect.collidepoint(event.pos):
                        self.selcted = (loc, 'accesories', self.accsessories[loc])
                print(self.selcted)
            
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
                    elif self.selcted[1] == 'itembar':
                        self.itembar.items[self.selcted[0]] = self.inventory[loc]
                        self.inventory[loc] = self.selcted[2]
                    else:
                        if self.selcted[2][0] != None:
                            if self.inventory[loc][0] == None:
                                self.accsessories[self.selcted[0]] = self.inventory[loc]
                                self.inventory[loc] = self.selcted[2]
                                for attribute in self.selcted[2][0].attributes:
                                    attribute.remove()
                            else:
                                flag = False
                                for attribute in self.inventory[loc][0].attributes:
                                    if isinstance(attribute, Accessory):
                                        flag = True
                                for attribute in self.selcted[2][0].attributes:
                                    if isinstance(attribute, Accessory):
                                        flag = True
                                if not flag:
                                    self.accsessories[self.selcted[0]] = self.inventory[loc]
                                    self.inventory[loc] = self.selcted[2]
                                    for attribute in self.selcted[2][0].attributes:
                                        attribute.remove()
                                
                    self.selcted = (loc, 'inventory', self.inventory.get(loc, None))

            for loc in range(0, self.itembar.max_items):
                rect = pygame.Rect((int((self.center_pos[0]+self.padding+loc*(self.icon_size+2)+loc)*self.scale[0]),
                                        int((self.center_pos[1]+74)*self.scale[1])
                                        ), (int(18*self.scale[0]), int(18*self.scale[1])))
                if rect.collidepoint(event.pos):
                    if self.selcted[1] == 'inventory':
                        self.inventory[self.selcted[0]] = self.itembar.items[loc]
                        self.itembar.items[loc] = self.selcted[2]
                    elif self.selcted[1] == 'itembar':
                        self.itembar.items[self.selcted[0]] = self.itembar.items[loc]
                        self.itembar.items[loc] = self.selcted[2]
                    else:
                        if self.selcted[2][0] != None:
                            if self.itembar.items[loc][0] == None:
                                self.accsessories[self.selcted[0]] = self.itembar.items[loc]
                                self.itembar.items[loc] = self.selcted[2]
                                for attribute in self.selcted[2][0].attributes:
                                    attribute.remove()
                            else:
                                flag = False
                                for attribute in self.itembar.items[loc][0].attributes:
                                    if isinstance(attribute, Accessory):
                                        flag = True
                                for attribute in self.selcted[2][0].attributes:
                                    if isinstance(attribute, Accessory):
                                        flag = True
                                if not flag:
                                    self.accsessories[self.selcted[0]] = self.itembar.items[loc]
                                    self.itembar.items[loc] = self.selcted[2]
                                    for attribute in self.selcted[2][0].attributes:
                                        attribute.remove()
                    self.selcted = (loc, 'itembar', self.itembar.items[loc])

            for loc in range(0, self.max_accessories):
                    rect = pygame.Rect(
                        (
                         (self.center_pos[0]+86)*self.scale[0],
                         int((self.center_pos[1]+3+loc*(self.icon_size+2)+loc)*self.scale[1])
                         ),
                        (int(18*self.scale[0]), int(18*self.scale[1]))
                    )
                    if rect.collidepoint(event.pos) and self.selcted[2][0] != None:
                        print(f"\n{self.accsessories[loc][0]}\n")
                        if self.selcted[2][0] != None:
                            for attribute in self.selcted[2][0].attributes:
                                if isinstance(attribute, Accessory):
                                    if self.selcted[1] == 'inventory':
                                        self.inventory[self.selcted[0]] = self.accsessories[loc]
                                        self.accsessories[loc] = self.selcted[2]
                                    elif self.selcted[1] == 'itembar':
                                        self.itembar.items[self.selcted[0]] = self.accsessories[loc]
                                        self.accsessories[loc] = self.selcted[2]
                                    else:
                                        self.accsessories[self.selcted[0]] = self.accsessories[loc]
                                        self.accsessories[loc] = self.selcted[2]
                                    self.selcted = (loc, 'accesories', self.accsessories[loc])

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
        elif self.selcted != None and self.selcted[1] == 'accesories':
            blit(disp, self.selected_image, 
                 ((self.center_pos[0]+86),
                  int((self.center_pos[0]+3+self.selcted[0]*(self.icon_size+2)+self.selcted[0]))-72)
                )

        # Render inventory items
        for loc in self.inventory:
            if self.inventory[loc][0] != None:
                pos = (
                    self.center_pos[0]+self.padding+loc[0]*(self.icon_size+2)+loc[0]+1,
                    self.center_pos[1]+11+loc[1]*(self.icon_size+2)+loc[1]+1
                )
                blit(disp, self.inventory[loc][0].icon, pos)
                render_font(self.counts[loc], self.scale, (pos[0]+2, pos[1]+2))
        # Render ItemBar items
        for loc in range(0, self.itembar.max_items):
            if self.itembar.items[loc][0] != None:
                pos = (
                    self.center_pos[0]+self.padding+loc*(self.icon_size+2)+loc+1,
                    self.center_pos[1]+75
                )
                blit(disp, self.itembar.items[loc][0].icon, (pos))
                render_font(self.itembar.counts[loc], self.scale, (pos[0]+2, pos[1]+2))

        # Display Accessory icons
        for loc in range(0, self.max_accessories):
            if self.accsessories[loc][0] != None:
                blit(disp, self.accsessories[loc][0].icon, 
                 ((self.center_pos[0]+87),
                  int((self.center_pos[0]+3+loc*(self.icon_size+2)+loc))-71)
                )
        
        # Display icon at mouse cursor when held
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
        self.font = pygame.font.Font('freesansbold.ttf', int(8*self.scale[1]))
        self.health_font = self.font.render(str(self.max_health)+"/"+str(self.max_health), True, (255, 250, 250))
        self.health_per_bar = 10
        self.step = 21
        self.heal_tick = 0
        self.ticks_between_healing = 390
        self.immunity_frames = 20
        self.damage_multiplier = 1
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
            render_font(self.font.render(str(self.health)+"/"+str(self.max_health), True, (255, 250, 250)), self.scale, 
                        (self.center_pos[0]+20 ,self.center_pos[1] + 19))
            
        # Increment ticks between healing, if needed    
        if self.health < self.max_health:
            if self.heal_tick >= self.ticks_between_healing:
                self.heal_tick = 0
                self.health += 1
            else:
                self.heal_tick += 1
        else:
            self.heal_tick = 0

        # Increment ticks between damage, if needed    
        if self.damaged:
            if self.tick >= self.immunity_frames:
                self.tick = 0
                self.damaged = False
            else:
                self.tick += 1
        if self.health <= 0:
            self.dead = True
                
    def damage(self, damage_amount):
        if not self.damaged and self.health > 0:
            if int(damage_amount*self.damage_multiplier) > self.health:
                self.health = 0
            else:
                self.health -= int(damage_amount*self.damage_multiplier)
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

class EndScreen(MenuItem):
    """Class for the screen showed at the end of the screen"""
    def __init__(self, pos, scale, game_end_image, restart_button, continue_button, player, center=True):
        super().__init__(pos, (game_end_image.get_width(), game_end_image.get_height()), scale, [pygame.MOUSEBUTTONDOWN], center)
        self.image = game_end_image
        self.restart_button_img = restart_button
        self.continue_button_img = continue_button
        self.player=player
        # Freeze the player and hide game elements
        player.stunned = True
        player.hud.background_tint = True
        player.hud.ignore('itembar')
        player.hud.ignore('inventory')
        player.hud.ignore('text-box')
        player.game_over = True

        self.restart_button = Button((self.center_pos[0]+(self.image.get_width()//2), self.center_pos[1]+self.image.get_height()+15+(self.restart_button_img.get_height()//2) ), (self.restart_button_img.get_width(), self.restart_button_img.get_height()),
                                     self.scale, self.restart_button_img, "", self.restart_game)
        self.continue_button = Button((self.center_pos[0]+(self.image.get_width()//2), self.center_pos[1]+self.image.get_height()+20+self.restart_button_img.get_height()+(self.continue_button_img.get_height()//2)), (self.continue_button_img.get_width(), self.continue_button_img.get_height()),
                                     self.scale, self.continue_button_img, "", self.continue_game)
        
        self.large_font_size = 9
        self.small_font_size = 4
        self.font_spacing = 1

        self.large_font = pygame.font.Font('freesansbold.ttf', int(self.large_font_size*self.scale[1]))
        self.small_font = pygame.font.Font('freesansbold.ttf', int(self.small_font_size*self.scale[1]))

        items_found = 0
        total_items = 0
        total_rooms = 0
        rooms_completed = 0
        total_notes = 0
        notes_checked = 0
        for room in self.player.gameManager.rooms.values():
            # Create variables to store temporary values
            chests_opened_in_room = 0
            total_chests_in_room = 0

            notes_checked_in_room = 0
            total_notes_in_room = 0

            with open("data/rooms/"+room['room'], 'r') as r:
                room_data = json.load(r)
            total_rooms += 1 # Increment rooms

            # Check for chests opened in the room
            for k, v in room_data.get('tilemap', {}).items():
                if v.get('id', None) == 'chest' or v.get('id', None) == 'objective-chest':
                    total_items += 1
                    total_chests_in_room += 1
                    if room.get('meta', {}).get(tuple([int(x) for x in k.split(";")]), {}).get('opened', False):
                        items_found += 1
                        chests_opened_in_room += 1

                # Check note-walls
                elif v.get('id', None) == 'note-wall':
                    total_notes += 1
                    total_notes_in_room += 1
                    if room.get('meta', {}).get(tuple([int(x) for x in k.split(";")]), {}).get('checked', False):
                        notes_checked += 1
                        notes_checked_in_room += 1

            # Check if the room was marked as completed, and if all chests and notes were checked/opened
            if (room.get('meta', {}).get('completed', False) and 
                (chests_opened_in_room >= total_chests_in_room) and 
                (notes_checked_in_room >= total_notes_in_room)):
                rooms_completed += 1

        # Render fonts to be displayed
        self.chest_label = self.small_font.render(f"Chests Opened - {items_found}/{total_items}", True, (255, 250, 250))
        self.chest_counts = self.small_font.render(f"{items_found}/{total_items}", True, (255, 250, 250))

        self.rooms_label = self.small_font.render(f"Rooms Completed - {rooms_completed}/{total_rooms}", True, (255, 250, 250))
        self.room_counts = self.small_font.render(f"{rooms_completed}/{total_rooms}", True, (255, 250, 250))

        self.notes_label = self.small_font.render(f"Notes Checked - {notes_checked}/{total_notes}", True, (255, 250, 250))
        self.note_counts = self.small_font.render(f"{notes_checked}/{total_notes}", True, (255, 250, 250))

        self.percentage_label = self.large_font.render(f"{int(((items_found+notes_checked+rooms_completed)/(total_items+total_notes+total_rooms))*100)}%", True, (255, 250, 250))
        self.time_label = self.small_font.render(f"{convert_time(pygame.time.get_ticks()//1000)}", True, (255, 250, 250))


    def check_events(self, event):
        """Run check events for element"""
        self.restart_button.check_events(event)
        self.continue_button.check_events(event)
        
    def restart_game(self):
        """Method called when the user presses the restart button"""
        self.player.game.__init__()
        

    def continue_game(self):
        """Method called when the user resses the continue button"""
        self.delete = True
        self.player.hud.background_tint = False
        self.player.game_over = False
        self.player.stunned = False

        self.player.hud.unignore('itembar')
        self.player.hud.unignore('text-box')

    def render(self, disp):
        """Render gui element, and buttons"""
        super().render(disp)

        # Render buttons
        self.restart_button.render(disp)
        self.continue_button.render(disp)

        # Render game stats
        render_font(self.percentage_label, self.scale, (self.center_pos[0]+ ((self.size[0]//2) - (self.percentage_label.get_width()//2)//self.scale[0]), self.center_pos[1]+30))
        render_font(self.time_label, self.scale, (self.center_pos[0]+ (self.size[0]//2)  - (self.time_label.get_width()//2)//self.scale[0], self.center_pos[1]+30+self.large_font_size+self.font_spacing))
        # Additional game Stats
        render_font(self.rooms_label, self.scale, (self.center_pos[0]+ (self.size[0]//2)  - (self.rooms_label.get_width()//2)//self.scale[0], self.center_pos[1]+30+(self.small_font_size*2)+self.large_font_size+(self.font_spacing*3)))
        render_font(self.chest_label, self.scale, (self.center_pos[0]+ (self.size[0]//2)  - (self.chest_label.get_width()//2)//self.scale[0], self.center_pos[1]+30+(self.small_font_size*3)+(self.font_spacing*4)+self.large_font_size))
        render_font(self.notes_label, self.scale, (self.center_pos[0]+ (self.size[0]//2)  - (self.notes_label.get_width()//2)//self.scale[0], self.center_pos[1]+30+(self.small_font_size*4)+(self.font_spacing*5)+self.large_font_size))
