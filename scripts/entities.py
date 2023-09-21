# Created By: Zachary Hoover
# Created Date: 9/17/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains entity classes for physics objects, players, enemies, projectiles, etc. 

--+ Classes +-- 
PhysicsEntity() - Class object used for creating objects that interact with physics\
Player()
Enemey()

"""
# --------------------------------------------------------------------------------
# External imports
import pygame

# --------------------------------------------------------------------------------
class PhysicsEntity():
    """Class object used for creating objects that interact with physics"""
    def __init__ (self, game, pos, size, exceptions = []):
        """Initialize variables for physics entity"""
        self.game = game
        self.pos = list(pos) # Convert to list to better be able to modify positions
        self.size = size

class SolidObject():
    """Simple class for solid objects"""



