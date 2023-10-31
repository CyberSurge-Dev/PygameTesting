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
from scripts.utils import blit
from scripts.tiles import Tile, InteractableTile

# External imports
import pygame
import math

POSITIONS_AROUND = ((0, 1), (0, -1), (-1, 0), (1, 0), (-1, -1), (-1, 1),
                    (1, -1), (1, 1), (0, 0))


class Tilemap():
    """Tilemap class manages, loads, and renders the tiles for the game"""

    def __init__(self, asset_map, tile_size):
        """Initialize variables"""
        self.asset_map = asset_map
        self.tile_size = tile_size

        self.tilemap = {}
        self.decor = {}  # Just images, can have floating point positions
        self.items = {}  # Item objects to be rendered on the tilemap

    def load(self, tile_data):
        """Load the tilemap from a provided dictionary""" ""

        # Load information from Tilemap
        for k, v in tile_data['tilemap']:
            tile = self.assetMap.tiles[v.get('id', 'NaT')].copy()
            tile.pos = tuple([int(x) for x in k.split(";")])
            tile.variant = v.get('variant', 0)

            self.tilemap[tuple([int(x) for x in k.split(";")])] = tile
        for k, v in tile_data['decor']:
            self.decor[tuple([float(x) for x in k.split(";")
                              ])] = self.assetMap.decor[v.get('id', 'NaD')]

        for k, v in tile_data['items']:
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
                self.tilemap.get((pos[0] + position[0], pos[1] + position[1]),
                                 None))
        return tiles

    def get_solid_rects_around(self, pos):
        """Returns a list of rects areound the given position"""
        return [
            pygame.Rect(tile.pos[0] * self.tile_size,
                        tile.pos[1] * self.tile_size, self.tile_size,
                        self.tile_size) for tile in self.get_tiles_around(pos)
            if tile != None and tile.solid
        ]
    
    def get__rects_around(self, pos):
        """Returns a list of rects areound the given position"""
        return [
            pygame.Rect(tile.pos[0] * self.tile_size,
                        tile.pos[1] * self.tile_size, self.tile_size,
                        self.tile_size) for tile in self.get_tiles_around(pos)
            if tile != None
        ]

    def get_interactable_tiles(self):
        """Returns a list of all interactable tiles in tilemap"""
        return [x for x in self.tilemap.values() if type(x) == InteractableTile]

    def get_interactable_tiles_around(self, pos):
        """Returns a list of interactable tiles around pos"""
        return [x for x in self.get_tiles_around(pos) if type(x) == InteractableTile]
    
    def get_collided_items(self, rect):
        """Returns a list of Item objects that collide with the passed in Rect"""
        return [
            item for pos, item in self.items.items() 
            if pygame.Rect(item.icon.get_width(), item.icon.get_height(), pos[0]*self.tile_size, pos[1]*self.tile_size).colliderect(rect)
        ]
    
    def closest_interactable_tile(self, pos):
        pos = (int(pos[0]-self.tile_size//2), int(pos[1]-self.tile_size//2))
        distances = {abs(math.hypot((int(tile.pos[0]-self.tile_size//2), int(tile.pos[1]-self.tile_size//2)), pos)): tile for tile in self.get_interactable_tiles_around(pos)}
        # Return closest interactable tiles
        return distances.get(min(*distances, default=0), None)
    
    def closest_item(self, pos):
        pass
       

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
