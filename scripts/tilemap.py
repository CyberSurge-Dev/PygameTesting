
from scripts.entities import SolidObject
from scripts.utils import load_image, load_images
import pygame

class Sprite():
    """Simple class to create sprites for SpriteMap"""
    def __init__(self, variants, type):
        self.variants = variants
        self.type = type
        self.type = pos    

class SpriteMap():
    """Simple class to for sprites and sprite types"""
    def __init__(self):
        """Initialize SpriteMap"""
        self.Map = {
            "wall" : Sprite(load_images("tiles/walls"), SolidObject()),
            "floor" : LoadSprite()
        }

class TileMap():
    """Class to manage the TileMap"""
    def __init__(self, game, tile_size = 16):
        
    