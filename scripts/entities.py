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

    def __init__ (self, game, pos, size):
        """Initialize the physics entity"""
        self.pos = list(pos) # Convert to list for mutability
        self.game = game
        self.size = size
        self.multiplyer = 1
        self.tilemap = game.tilemap

        # Create a dictionary to store colisions, and velocity
        self.state = {
            'forward': {'col':False, 'vel':0},
            'backward': {'col':False, 'vel':0},
            'left': {'col':False, 'vel':0},
            'right': {'col':False, 'vel':0}
        }

    def rect(self):
        """Returns a pygame Rect onject at the location of the player"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, **movement):
        """
        Update function for handeling the movement of physics object

        Pass in movement with direction = movment (ex: left = 1)
        """
        player_rect = self.rect()
        tiles_around = self.tilemap.get_rects_around(self.pos)
        
        if tiles_around['top_center'] != None:
            tiles_around['top_center'] # add stuff for rects
            
            
        
    def render(self, offset):
        pass
        


