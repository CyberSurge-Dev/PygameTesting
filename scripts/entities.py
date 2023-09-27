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
from scripts.tilemap import Tilemap

# --------------------------------------------------------------------------------
class PhysicsEntity:
    """Class object used for creating objects that interact with physics"""

    def __init__ (self, game, pos, size,  exceptions=[]):
        """Initialize the physics entity"""
        self.pos = list(pos) # Convert to list for mutability
        self.game = game
        self.size = size
        self.multiplyer = 1
        self.tilemap = self.game.tilemap
        self.exceptions = exceptions
        self.assetMap = self.game.assetMap

        # Create a dictionary to store colisions, and velocity
        self.colisions = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False
        }

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

        
        # Calculate movement for the frame
        frame_movement = (
            (movement['right']-movement['left']) + self.velocity[0],
            (movement['down']-movement['up']) + self.velocity[1]
        )
        
        # Check for collionions in left and right movement
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        # print(entity_rect)
        for rect in self.tilemap.get_rects_around(self.pos, self.exceptions).values():
            # print(rect)
            if rect != None and entity_rect.colliderect(rect):
                print("col left-right")
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        # Check for collisions in up and down movement
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in self.tilemap.get_rects_around(self.pos, self.exceptions).values():
            if rect != None and entity_rect.colliderect(rect):
                print("col up-down")
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

        tiles_around = self.tilemap.get_rects_around(self.pos, self.exceptions)
        
    def render(self, offset=(0, 0)):
        self.game.display.blit(self.assetMap.entities['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        


