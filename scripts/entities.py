# Created By: Zachary Hoover
# Created Date: 9/17/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains entity classes for physics objects, players, enemies, projectiles, etc. 

--+ Classes +-- 
PhysicsEntity() - Class object used for creating objects that interact with physics
Player()
Enemey()

"""
# --------------------------------------------------------------------------------
# External imports
import pygame
import math

# Internal imports
from scripts.guiElements import ItemBar, ClosableTextBox, Inventory, HealthBar
from scripts.guiManager import GUIManager
from scripts.utils import blit
# --------------------------------------------------------------------------------
class PhysicsEntity:
    """Class object used for creating objects that interact with physics"""

    def __init__ (self, game, pos, size, sprite=None, multiplier=1, *exceptions):
        """Initialize the physics entity"""
        self.pos = list(pos) # Convert to list for mutability
        self.game = game
        self.size = size
        self.multiplier = multiplier
        self.tilemap = self.game.tilemap
        self.exceptions = exceptions
        self.sprite = sprite # Can be a dictionary or just a pygame surface
        self.stunned = False
        
        # Create a dictionary to store colisions, and velocity
        self.colisions = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False
        }

        self.state = "idle"
        
        self.velocity = [0, 0]

    def rect(self):
        """Returns a pygame Rect onject at the location of the player"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, **movement):
        """
        Update function for handeling the movement of physics object

        Pass in movement with direction = movment (ex: left = 1)
        """
        # Reset collisions
        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        if not self.stunned:
            # Calculate movement for the frame
            frame_movement = (
                ((movement['right']-movement['left']) + self.velocity[0]) * self.multiplier,
                ((movement['down']-movement['up']) + self.velocity[1]) * self.multiplier
            )
        else:
            frame_movement = [0, 0]

        self.game.telemetry.add('movement[0]', frame_movement[0])
        self.game.telemetry.add('movement[1]', frame_movement[1])
        
        # Check for collionions in left and right movement
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        rect_pos = []

        for rect in self.tilemap.get_solid_rects_around(self.pos):
            if rect != None and entity_rect.colliderect(rect):
                rect_pos.append((rect.x, rect.y))
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                    self.game.telemetry.add('colision', 'right')
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                    self.game.telemetry.add('colision', 'left')
                self.pos[0] = entity_rect.x

        self.game.telemetry.add((entity_rect.centerx, entity_rect.centery), rect_pos)
        
        # Check for collisions in up and down movement
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in self.tilemap.get_solid_rects_around(self.pos):
            if rect != None and entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[0] = 0
        elif self.collisions['left'] or self.collisions['right']:
            self.velocity[1] = 0

        # Set the player state based on the frame movement
        if frame_movement[0] > 0:
            if frame_movement[1] > 0:
                self.state = 'up-right'
            elif frame_movement[1] < 0:
                self.state = 'down-right'
            else:
                self.state = 'right'
        elif frame_movement[0] < 0:
            if frame_movement[1] > 0:
                self.state = 'up-left'
            elif frame_movement[1] < 0:
                self.state = 'down-left'
            else:
                self.state = 'left'
        elif frame_movement[1] > 0:
            self.state = 'down'
        elif frame_movement[1] < 0:
            self.state = 'up'
        else:
            self.state = 'idle'
        
    def render(self, disp, offset=(0, 0)):
        """Render the entity to the screen"""
        img = None # Set to None as placeholder
        if type(self.sprite) == dict:
            img = self.sprite.get(self.state, None)
        else:
            img = self.sprite
        
        blit(disp, img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def set_pos(self, position):
        """Sets the location of the entity, relative to the center of the rect"""
    
class Player(PhysicsEntity):
    """Class for all player related physics, and interactions."""

    def __init__ (self, game, pos, size, gameManager, multiplier=1, *exceptions):
        """Initialize the player and physics entity"""""
        # Create variables for reference to other elements
        self.game = game
        self.gameManager = gameManager
        self.tilemap = self.game.tilemap
        self.assetMap = self.game.assetMap
        self.inventory = {}
        # Create HUD items
        self.hud = GUIManager()
        self.hud.add('itembar', ItemBar(self.game.dPos.BOTTOM_CENTER, (81, 24), self.game.scale, self.assetMap.gui['itembar'], self.assetMap.gui['itembar_selected']))
        self.itembar = self.hud.menu_items['itembar']
        self.hud.add('inventory', Inventory(self.game.dPos.CENTER, (81, 95), self.game.scale, self.assetMap.gui['inventory'], self.assetMap.gui['itembar_selected'], self.itembar, self.game))
        self.hud.ignore('inventory')
        self.hud.add('health-bar', HealthBar((2,2), (0, 0), self.game.scale, [], 
                                             self.assetMap.gui['health-emblem'],
                                             self.assetMap.gui["empty-health-bar"], 
                                             self.assetMap.gui['filled-health-bar'], 
                                             40, 40))
        self.health_bar = self.hud.menu_items['health-bar']
        self.inventory = self.hud.menu_items['inventory']
        self.inventory_open = False
        self.interaction = False

        super().__init__(game, pos, size, self.assetMap.entities['player'], multiplier, exceptions)

    def check_events(self, event):
        """Check events for the player"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.itembar.items[self.itembar.slot_selected][0] != None:
            if event.button == 1:  # Left mouse button.
                self.itembar.items[self.itembar.slot_selected][0].left_button(event)
            elif event.button == 3:  # Right mouse button.
                self.itembar.items[self.itembar.slot_selected][0].right_button(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == self.game.keybinds['inventory']:
                if self.inventory_open:
                    self.hud.background_tint = False
                    self.stunned = False
                    self.hud.unignore('itembar')
                    self.hud.ignore('inventory')
                    self.inventory_open = False
                else:
                    self.hud.background_tint = True
                    self.interaction = False
                    self.stunned = True
                    self.hud.ignore('itembar')
                    self.hud.unignore('inventory')
                    self.inventory_open = True
            elif event.key == pygame.K_e and self.interaction:
                thing = self.tilemap.closest_interactable(self.pos)
                if thing != None:
                    thing.interact(self)
            
        self.hud.check_events(event)

    def update(self, **movement):
        """Updates the player"""
        super().update(**movement)
        # Update currently held items attributes 
        if self.itembar.items[self.itembar.slot_selected][0] != None:
            self.itembar.items[self.itembar.slot_selected][0].update()
        if self.tilemap.closest_interactable(self.pos) != None:
            self.interaction = True
        else:
            self.interaction = False
        if self.health_bar.dead:
            self.gameManager.set_room(0)
            self.health_bar.health = self.health_bar.max_health
            self.health_bar.dead = False
        
        self.tilemap.check_collisions(self.rect(), self)
        
    def render(self, disp, offset=(0, 0)):
        """Render player and HUD elements."""
        super().render(disp, offset)
        # Render the HUD items
        self.hud.render(disp)
        if self.interaction:
            blit(disp, self.assetMap.gui['interaction'], (self.pos[0]-offset[0], self.pos[1]-offset[1]))
            