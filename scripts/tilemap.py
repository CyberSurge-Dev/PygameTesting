# Created By: Zachary Hoover
# Created Date: 9/21/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains the Tilemap class, which is a manager for all tile related
inquiries.

--+ Classes +-- 
TileMap(game, tile_zise) - Class to manage the layout, and metadata of tiles displayed on the screen.

--+ Variables +--
BASE_TILEMAP_PATH - Contains the base path were all rooms are stored.
TILES_AROUND - Store the relative positions of all tiles around a central tile.

"""
# --------------------------------------------------------------------------------
# External imports
import pygame
import json

# --------------------------------------------------------------------------------

BASE_TILEMAP_PATH = "data/rooms/"
TILES_AROUND  = {
    'top_left': (-1, -1),
    'top_center': (0, -1),
    'top_right': (1, -1),
    'left': (-1, 0),
    'center': (0, 0),
    'right': (1, 0),
    'bottom_left': (-1, 1),
    'bottom_center': (0, 1),
    'bottom_right': (1, 1) 
}

class Tilemap():
    """Class to manage Class to manage the layout, and metadata of tiles displayed on the screen."""
    
    def __init__(self, game, tile_size):
        """Initialize the Tilemap class"""
        self.game = game
        self.tile_size = tile_size
        self.assetMap = self.game.assetMap

        self.tilemap = {}

    def load(self, path):
        """Load tilemap from json file"""
        level_file = open(BASE_TILEMAP_PATH + path,
                          "r")  # open the JSON file for settings
        level_data = json.load(level_file)  # Extract data from JSON as dictionary
        level_file.close()  # Close JSON file

        # Load tilemap as dictionary from JSON file, convert strings to tuples
        self.tilemap = {tuple(int(v) for v in k.split(';')): v for k, v in level_data['tilemap'].items()}

    def get_tile(self, pos):
        return self.tilemap.get(pos, None)
    
    def tiles_arround(self, pos, exceptions = []):
        """Returns a dictionary of the tiles that are around a position"""
        tiles = {}
        # adjust pos to tilemap
        pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        # Check each tile around the posiyion
        
        for txt, Tpos in TILES_AROUND.items(): 
            # Get tile from tilemap
            tile = self.get_tile((pos[0]+Tpos[0], pos[1]+Tpos[1]))
            if tile != None:
                # Get the tiledata from assetMap
                tile = self.assetMap.tiles.get(tile.get('id'))
                # add tile position key
                tile['pos'] = (pos[0]+Tpos[0], pos[1]+Tpos[1])

            # Check for how the tile should be added to the dictionary
            if tile not in exceptions and tile != None:
                tiles[txt] = tile.copy()
            else:
                tiles[txt] = None
                
        return tiles

    def get_rects_around(self, pos, exceptions = []):
        """Returns a dictionary of the positions of the surrounding solid tiles"""
        tiles = {}
        for txt, tile in self.tiles_arround(pos, exceptions).items():
            if tile != None and tile.get('type') == 'solid':
                # self.game.telemetry.add(txt, self.tiles_arround(pos, exceptions)[txt]['pos'])
                tiles[txt] = pygame.Rect(
                    # Rect position
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size,
                    # Rect size
                    self.tile_size,
                    self.tile_size 
                )
                # self.game.telemetry.add(txt, (tiles[txt].x, tiles[txt].y))
            else:
                tiles[txt] = None
        return tiles

    def get_interactable_arround(self, pos, exceptions = []):
        """Returns a matrix of surrounding interactable tiles"""
        tiles = {}
        for txt, tile in self.tiles_arround(pos, exceptions).items():
            if tile != None and tile.get('interaction', False) != False:
                tiles[txt] = tile
            else:
                tiles[txt] = None

        return tiles

    def render(self, offset=(0, 0)):
        # Render each tile in the Tilemap        
        for x in range(offset[0] // self.tile_size, (offset[0] + self.game.display.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + self.game.display.get_height()) // self.tile_size + 1):
                loc = (x, y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    self.game.display.blit(self.assetMap.tiles[tile['id']]['variants'][tile['variant']], (loc[0] * self.tile_size - offset[0], loc[1] * self.tile_size - offset[1]))
