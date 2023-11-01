# Created By: Zachary Hoover
# Created Date: 10/30/2023
# Version: 2.0
# --------------------------------------------------------------------------------
"""
This file contains the re-written tilemap, which was re-written to support
more customizable tile objects, and contains more robust, and simpiler to work 
with methods.

--+ Classes +-- 
Tilemap() - Tilemap class manages, loads, and renders the tiles for the game
"""
# --------------------------------------------------------------------------------
# Internal imports
from code import interact
from scripts.utils import blit
from scripts.tiles import Tile, InteractableTile

# External imports
import pygame
import math
import json

POSITIONS_AROUND = ((0, 1), (0, -1), (-1, 0), (1, 0), (-1, -1), (-1, 1),
                    (1, -1), (1, 1), (0, 0))
BASE_TILEMAP_PATH = "data/rooms/"


class Tilemap():
    """Tilemap class manages, loads, and renders the tiles for the game"""

    def __init__(self, asset_map, tile_size):
        """Initialize variables"""
        self.assetMap = asset_map
        self.tile_size = tile_size

        self.tilemap = {}
        self.decor = {}  # Just images, can have floating point positions
        self.items = {}  # Item objects to be rendered on the tilemap

    def load(self, filename):
        """Load the tilemap from a provided dictionary"""
        with open(BASE_TILEMAP_PATH + filename, "r") as f:
            tile_data = json.load(f) 
        # Reset tilemaps
        self.tilemap = {}
        self.decor = {}  # Just images, can have floating point positions
        self.items = {}  # Item objects to be rendered on the tilemap

        # Load information from Tilemap
        for k, v in tile_data.get('tilemap', {}).items():
            # Load tile information from fle and assetMap
            tile = self.assetMap.tiles[v.get('id', 'NaT')].copy()
            tile.pos = tuple([int(x) for x in k.split(";")])
            tile.variant = v.get('variant', 0)
            tile.meta.update(v.get('meta', {}))
            # Put the tile into the tilemap
            self.tilemap[tuple([int(x) for x in k.split(";")])] = tile
        
        for k, v in tile_data.get('decor', {}).items():
            # Load decor from file, these are just images
            self.decor[tuple([float(x) for x in k.split(";")
                              ])] = self.assetMap.decor[v.get('id', 'NaD')]

        for k, v in tile_data.get('items', {}).items():
            # Load items from tilemap (these are objects derived from the Item class)
            self.items[tuple([float(x) for x in k.split(";")
                              ])] = self.assetMap.items[v.get('id', 'NaI')]

    def get_tile(self, pos):
        """Returns tile at given position"""
        return self.tilemap.get(pos, None)

    def get_tiles_around(self, pos):
        """Returns a list of tiles that are around the given position"""
        pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        # Create a dictionary of positions around the player
        tiles = []
        for position in POSITIONS_AROUND:
            tiles.append(
                self.tilemap.get((pos[0] + position[0], pos[1] + position[1]), None))
        return tiles

    def get_solid_rects_around(self, pos):
        """Returns a list of rects areound the given position"""
        return [
            pygame.Rect(tile.pos[0] * self.tile_size,
                        tile.pos[1] * self.tile_size, self.tile_size,
                        self.tile_size) for tile in self.get_tiles_around(pos)
            if tile != None and tile.solid
        ]
    
    def get_rects_around(self, pos):
        """Returns a list of rects areound the given position"""
        return [
            pygame.Rect(tile.pos[0] * self.tile_size,
                        tile.pos[1] * self.tile_size, self.tile_size,
                        self.tile_size) for tile in self.get_tiles_around(pos)
            if tile != None
        ]

    def get_interactable_tiles(self):
        """Returns a list of all interactable tiles in tilemdap"""
        return [x for x in self.tilemap.values() if type(x) == InteractableTile]

    def get_interactable_tiles_around(self, pos):
        """Returns a list of interactable tiles around pos"""
        return [x for x in self.get_tiles_around(pos) if type(x) == InteractableTile]
    
    def get_interactable_only_tiles_around(self, pos):
        """Returns a list of interactable tiles around pos"""
        return [x for x in self.get_interactable_tiles_around(pos) if x.collision_interactable == False or x.interactable]
    
    def get_collide_only_tiles_around(self, pos):
        """Returns a list of interactable tiles around pos that are collision only."""
        return [x for x in self.get_interactable_tiles_around(pos) if type(x) == InteractableTile and x.interactable == False and x.collision_interactable]
    
    def get_collided_items(self, rect):
        """Returns a list of Item objects that collide with the passed in Rect"""
        return [
            item for pos, item in self.items.items() 
            if pygame.Rect(pos[0]*self.tile_size, pos[1]*self.tile_size, item.icon.get_width(), item.icon.get_height()).colliderect(rect)
        ]
    
    def closest_interactable_tile(self, pos):
        pos = (int(pos[0]+self.tile_size//2), int(pos[1]+self.tile_size//2))
        distances = {abs(math.hypot((int(tile.pos[0]+self.tile_size//2), int(tile.pos[1]+self.tile_size//2)), pos)): tile for tile in self.get_interactable_tiles_around(pos)}
        # Return closest interactable tile
        return distances.get(min(*distances.keys(), default=0), None)
    
    def closest_interactable_item(self, pos):
        pos = (int(pos[0]+self.tile_size//2), int(pos[1]+self.tile_size//2))
        distances = {
            abs(math.hypot(pos, (k[0] + int(item.icon.get_width()//2), k[1] + int(item.icon.get_height()//2)))) : item 
            for k, item in self.items.items() if item.is_interactable()
        }
        # Return closest interactable item
        return distances.get(min(*distances.keys(), default=0), None)

    def closest_interactable(self, position):
        pos = (int(position[0]+self.tile_size//2), int(position[1]+self.tile_size//2))
        distances = {
            abs(math.hypot(int(tile.pos[0]+self.tile_size//2) - pos[0], int(tile.pos[1]+self.tile_size//2) - pos[1])) : tile 
                           for tile in self.get_interactable_only_tiles_around(pos)
        }
        # Return closest interactable tile
        items_collided = self.get_collided_items(pygame.Rect(position[0], position[1], self.tile_size, self.tile_size)) 
        distances.update({
            abs(math.hypot(k[0] + int(item.icon.get_width()//2) - pos[0], k[1] + int(item.icon.get_height()//2) - pos[1])) : item 
            for k, item in self.items.items() 
            if item != None and item.is_interactable() and item in items_collided
        })

        return distances.get(min(distances.keys(), default=0), None)

    def check_collisions(self, rect, *args):
        """Checks if the passed in rect is colliding with any tiles"""
        # Set rect to collide with
        for tile in self.get_interactable_tiles_around((rect.x, rect.y)):
            if pygame.Rect(tile.pos[0]*self.tile_size, tile.pos[1]*self.tile_size, self.tile_size, self.tile_size).colliderect(rect):
                tile.on_collision(tile, *args)
                print("collide with tile")

    def add_tile(self, pos, tile):
        """Adds or overwrites tile at location"""
        if type(pos) != tuple:
            raise ValueError("Position must be a tuple.")
        else:
            tile.pos = pos # Make sure the pos for both is equal
            self.tilemap[pos] = tile

    def add_decor(self, pos, decor):
        """Adds surface to decor at given position(can be a float)"""
        self.decor[pos] = decor

    def add_item(self, pos, item):
        """Adds item to be rendered on Tilemap (Note: input should be a copy)"""
        self.items[pos] = item
    
    def render(self, disp, offset):
        """Render the tilemap"""
        for tile in self.tilemap.values():
            tile.render(disp, offset, self.tile_size)
        for pos, dec in self.decor.items():
            blit(disp, dec, (pos[0] * self.tile_size - offset[0],
                             pos[1] * self.tile_size - offset[1]))
        for pos, item in self.items.items():
            blit(disp, item.icon, (pos[0] * self.tile_size - offset[0],
                                   pos[1] * self.tile_size - offset[1]))
