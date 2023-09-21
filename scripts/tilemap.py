from scripts.entities import SolidObject
from scripts.utils import load_image, load_images
import pygame
import json

BASE_TILEMAP_PATH = "data/rooms/"
TILES_AROUND = ((0, 0), (0, -1), (0, 1), (1, 0), (-1, 0), (1, 1), (-1, 1),
                (1, -1), (-1, -1))


class Tilemap():
    """Class to manage tiles"""

    def __init__(self, game, tile_size=32):
        """Initialize the Tilemap class"""
        self.game = game
        self.tile_size = tile_size

        self.tilemap = {}

    def load(self, path):
        """Load tilemap from json file"""
        level_file = open("data/settings.json",
                          "r")  # open the JSON file for settings
        level_data = json.load(BASE_TILEMAP_PATH +
                               path)  # Extract data from JSON as dictionary
        level_file.close()  # Close JSON file

        self.tilemap = {tuple(k): v for k, v in level_data.items()}

    def get_tile(self, pos):
        return self.tilemap.get((pos[0], pos[1]), None)

    def get_solid_around(self):
        """Returns a matrix of the positions of the surrounding solid tiles"""
        tiles = []
        for tile in TILES_AROUND:
            if self.get_tile(tile)['type'] == 'solid':
                tiles.append(tile)

        return tiles

    def get_interactable_arround(self):
        """Returns a matrix of surrounding interactable tiles"""
        tiles = []
        for tile in TILES_AROUND:
            if self.get_tile(tile).get('interaction', False) != False:
                tiles.append(tile)

        return tiles
