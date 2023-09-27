import pygame
import json

BASE_TILEMAP_PATH = "data/rooms/"
TILES_AROUND  = {
    'top_left': (-1, 1),
    'top_center': (0, 1),
    'top_right': (1, 1),
    'left': (-1, 0),
    'center': (0, 0),
    'right': (1, 0),
    'bottom_left': (-1, -1),
    'bottom_center': (0, -1),
    'bottom_right': (1, -1) 
}

class Tilemap():
    """Class to manage tiles"""

    def __init__(self, game, tile_size=32):
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

        self.tilemap = {tuple(int(v) for v in k.split(';')): v for k, v in level_data['tilemap'].items()}

    def get_tile(self, pos):
        # print("Get Tile POS:", (pos[0], pos[1]))
        return self.tilemap.get((pos[0], pos[1]), None)
    
    def tiles_arround(self, pos, exceptions = []):
        """Returns a dictionary of the tiles that are around a position"""
        tiles = {}
        # adjust pos to tilemap
        pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        # Check each tile around the player
        for txt, Tpos in TILES_AROUND.items():
            tile = self.get_tile((pos[0]+Tpos[0], pos[1]+Tpos[1]))
            if tile != None:
                # print("Tile ID:",self.get_tile((pos[0]+Tpos[0], pos[1]+Tpos[1]))['id'])
                tile = self.assetMap.tiles[self.get_tile((pos[0]+Tpos[0], pos[1]+Tpos[1]))['id']]
                # add tile position key
                tile['pos'] = (pos[0]+Tpos[0], pos[1]+Tpos[1])
            # Check if the tile is in exceptions before adding
            if tile not in exceptions:
                tiles[txt] = tile
                # print("Tile:",tile)
            
        return tiles

    def get_rects_around(self, pos, exceptions = []):
        """Returns a matrix of the positions of the surrounding solid tiles"""
        tiles = {}
        for txt, tile in self.tiles_arround(pos, exceptions).items():
            if tile != None and tile.get('type') == 'solid':
                tiles[txt] = pygame.Rect(
                    # Rect position
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size,
                    # Rect size
                    self.tile_size,
                    self.tile_size 
                )
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
        for pos, tilemapped in self.tilemap.items():
            self.game.display.blit(
                self.assetMap.tiles[tilemapped['id']]['variants'][tilemapped['variant']],
                (
                    pos[0] * self.tile_size,
                    pos[1] * self.tile_size
                )
            )
