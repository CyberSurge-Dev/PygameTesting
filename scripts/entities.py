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
import random

# Internal imports
from scripts.guiElements import ItemBar, Inventory, HealthBar, GameOver
from scripts.guiManager import GUIManager
from scripts.utils import blit
import math
# --------------------------------------------------------------------------------
class PhysicsEntity:
    """Class object used for creating objects that interact with physics"""

    def __init__ (self, tilemap, pos, size, hitbox, sprite=None, multiplier=1, hitbox_on_bottom=True, *exceptions):
        """Initialize the physics entity"""
        self.pos = list(pos) # Convert to list for mutability
        self.size = size
        self.multiplier = multiplier
        self.tilemap = tilemap
        self.exceptions = exceptions
        self.sprite = sprite # Can be a dictionary or just a pygame surface
        self.stunned = False
        self.hitbox = hitbox
        self.hitbox_on_bottom = hitbox_on_bottom
        
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
        if not self.hitbox_on_bottom:
            return pygame.Rect(self.pos[0]+((self.size[0]-self.hitbox[0])//2), self.pos[1]+((self.size[1]-self.hitbox[1])//2), self.hitbox[0], self.hitbox[1])
        else:
            return pygame.Rect(self.pos[0]+((self.size[0]-self.hitbox[0])//2), self.pos[1]+((self.size[1]-self.hitbox[1])), self.hitbox[0], self.hitbox[1])

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
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x-(self.size[0]-self.hitbox[0])//2
        
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
                if self.hitbox_on_bottom:
                    self.pos[1] = entity_rect.y-(self.size[1]-self.hitbox[1])
                else:
                    self.pos[1] = entity_rect.y-(self.size[1]-self.hitbox[1])//2

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

    def __init__ (self, game, pos, size, hitbox, gameManager, multiplier=1, *exceptions):
        """Initialize the player and physics entity."""
        # Create variables for reference to other elements
        self.gameManager = gameManager
        self.tilemap = game.tilemap
        self.game = game
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
        self.hud.add('game-over', GameOver((self.game.dPos.CENTER[0], self.game.dPos.CENTER[1]-30), (0,0), self.game.scale, self.assetMap.gui["game-over-image"], self.assetMap.gui["respawn-button"], self.reset))
        self.hud.ignore('game-over')
        self.health_bar = self.hud.menu_items['health-bar']
        self.inventory = self.hud.menu_items['inventory']
        self.inventory_open = False
        self.interaction = False

        self.projectiles = []

        super().__init__(game.tilemap, pos, size, hitbox, self.assetMap.entities['player'], multiplier, True, exceptions)
        
    def reset(self):
        """Function that handles what is done when game over."""
        self.gameManager.set_room(0)
        self.health_bar.health = self.health_bar.max_health
        self.health_bar.dead = False
        self.hud.background_tint = False
        self.hud.ignore('game-over')
        self.hud.unignore('itembar')
        self.stunned = False
        self.arrows = []
        self.pos = [(self.tilemap.size[0]//2)*self.tilemap.tile_size, self.tilemap.size[1]//2*self.tilemap.tile_size]

    def check_events(self, event):
        """Check events for the player."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.itembar.items[self.itembar.slot_selected][0] != None:
            if event.button == 1:  # Left mouse button.
                self.itembar.items[self.itembar.slot_selected][0].left_button(event, self)
            elif event.button == 3:  # Right mouse button.
                self.itembar.items[self.itembar.slot_selected][0].right_button(event, self)
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
        """Updates the player."""
        super().update(**movement)
        # Update currently held items attributes 
        if self.itembar.items[self.itembar.slot_selected][0] != None:
            self.itembar.items[self.itembar.slot_selected][0].update()
        if self.tilemap.closest_interactable(self.pos) != None:
            self.interaction = True
        else:
            self.interaction = False
        if self.health_bar.dead:
            self.hud.background_tint = True
            self.stunned = True
            try:
                self.hud.ignore('itembar')
                self.hud.unignore('game-over')
            except: pass
        else:
            try:
                self.hud.unignore('itembar')
            except: pass
             
        self.tilemap.check_collisions(self.rect(), self)

        for projectile in self.projectiles:
            projectile.update(self)
        
    def render(self, disp, offset=(0, 0)):
        """Render player and HUD elements."""
        super().render(disp, offset)
        if self.interaction:
            blit(disp, self.assetMap.gui['interaction'], (self.pos[0]-offset[0], self.pos[1]-offset[1]))

        # Render the projectiles
        for projectile in self.projectiles:
            projectile.render(disp, offset)

        # Render the HUD items
        self.hud.render(disp)
    
class Enemy(PhysicsEntity):
    """Class for enemies."""
    def __init__ (self, sprite, damage=5, health=10, multiplier=0.25, distance_from_target=1, size=(32,32), hitbox=(24,24), meta={}, onDeath=None):
        """Initialize the enemy entity."""
        # Infromation to be set appon tilemap instilization
        self.pos = [0, 0]
        self.damage = damage
        self.health = health
        self.meta = meta
        self.distance_from_target=distance_from_target
        self.onDeath = onDeath
        self.damaged = False
        self.immunity_frames = 20
        self.tick = 21
        
        super().__init__(None, self.pos, size, hitbox, sprite, multiplier, [])
    
    def do_damage(self, damage_amount):
        if not self.damaged:
            self.health -= damage_amount
            self.damaged = True
        
    def update(self, physicsEntity):
        """Determine what direction the enemy needs to move in to go toward player."""
        # Dictionary for enemy movement
        pos = physicsEntity.pos

        # Increment ticks for immunity frames 
        if self.damaged:
            if self.tick >= self.immunity_frames:
                self.tick = 0
                self.damaged = False
            else:
                self.tick += 1

        movement = {
            'up' : False,
            'down': False,
            'left': False,
            'right': False
        }

        # Check horizontal movement
        if (self.pos[0]-pos[0]-self.distance_from_target > 15):
            movement['left'] = True
        elif (self.pos[0]-pos[0]+self.distance_from_target < -15):
            movement['right'] = True
        else:
            movement['right'] = False
            movement['left'] = False
           
        # Check vertical movement 
        if (self.pos[1]-pos[1]-self.distance_from_target < -15):
            movement['down'] = True
        elif (self.pos[1]-pos[1]+self.distance_from_target > 15):
            movement['up'] = True
        else:
            movement['up'] = False
            movement['down'] = False

        # Check for collision with passed entity
        if self.rect().colliderect(physicsEntity.rect()):
            physicsEntity.health_bar.damage(self.damage)

        super().update(**movement)
    
    def on_death(self, *args):
        """What happends on the death of the entity."""
        if self.onDeath != None:
            self.onDeath(self, args)

    def copy(self):
        """Return a copy of self."""
        return Enemy(self.sprite, self.damage, self.health, self.multiplier, self.distance_from_target, self.size, self.hitbox, self.meta, self.onDeath)

class Projectile(PhysicsEntity):
    """Class for projectiles."""
    def __init__(self, sprite, damage=5, multiplier=10, onHit=None):
        self.damage = damage
        self.multiplier = 10
        self.onHit = onHit
        self.sprite = sprite
        self.multiplier
        # Set on release
        self.pos = [0, 0]
        self.angle = 0 # Angle of projectile

    def set(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.sprite = pygame.transform.rotate(self.sprite, -math.degrees(self.angle))

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.sprite.get_width(), self.sprite.get_height())

    def update(self, player):
        """Update the arrow."""
        # Check for impacts with enemies
        for enemy in player.tilemap.enemyManager.check_collisions(self.rect()):
            enemy.do_damage(self.damage)
            player.projectiles.remove(self)
            
        # Check for impacts with the wall
        for tile in player.tilemap.get_solid_rects_around(self.pos):
            if self.rect().colliderect(tile):
                try: # Use try-except block to avoide having to fix a critical issue with collisions
                    player.projectiles.remove(self)
                except: pass
        self.pos[0] += math.cos(self.angle) * self.multiplier
        self.pos[1] += math.sin(self.angle) * self.multiplier

    def render(self, disp, offset):
        """Redner the arrow."""
        
        blit(disp, self.sprite, (self.pos[0]-offset[0], self.pos[1]-offset[1]))

    def copy(self):
        return Projectile(self.sprite, self.damage, self.onHit)

        

        
        
    
            