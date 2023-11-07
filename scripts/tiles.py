# Created By: Zachary Hoover
# Created Date: 10/30/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This file contains the Tile object classes, used for creating tiles simply.

--+ Classes +-- 
Tile() - Base tile
"""
# --------------------------------------------------------------------------------
from scripts.utils import blit

class Tile():
    """Base class for tiles, stores tile details"""
    def __init__(self, image, solid=False, meta={}, on_render=None, render_overide=None):
        """Initialize values on initialization."""
        self.image = image
        self.on_render = on_render
        self.meta = meta # Meta can also be changed when loaded
        self.solid = solid
        self.hidden = False
        self.render_override = render_overide

        # Tile information set when loaded from tilemap
        self.pos = (0, 0)
        self.variant = 0
        self.tile_group = ""# Tile group refference 

    def render(self, disp, offset, tilesize, *args):
        """Render the tile given the tilesize and position"""
        if not self.hidden and self.render_override == None:
            # If statements to check images upladed
            if type(self.image) == list:
                blit(disp, self.image[self.variant], (
                    self.pos[0]*tilesize-offset[0],
                    self.pos[1]*tilesize-offset[1]
                ))
            else:
                blit(disp, self.image, (
                    self.pos[0]*tilesize-offset[0],
                    self.pos[1]*tilesize-offset[1]
                ))
            if self.on_render != None:
                self.on_render(self, disp, offset, tilesize, *args)
        else:
            self.render_override(self, disp, offset, tilesize, *args)

    def copy(self):
        """Return a copy of the tile"""
        return Tile(self.image, self.solid, self.meta, self.on_render)

class InteractableTile(Tile):
    """Interactable tile, add interaction behaviour"""
    def __init__(self, image, solid=False, meta={}, interaction=None, first_interaction=None, on_collision=None, interactable=True, collision_interactable=True, on_render=None, render_override=None):
        """Initialize values on initialization"""
        super().__init__(image, solid, meta, on_render, render_override)
        self.interactable = interactable
        self.collision_interactable = collision_interactable
        self.times_interacted = 0
        self.interaction = interaction
        self.on_collision = on_collision
        if first_interaction == None:
            self.first_interaction = interaction
        else:
            self.first_interaction = first_interaction

    def interact(self, *args):
        """Call appropraite interaction function"""""
        if self.interactable:
            # Run correct function if the tile is interactable
            if self.times_interacted < 1 and self.first_interaction != None:
                self.first_interaction(self, *args)
            elif self.interaction != None:
                self.interaction(self, *args)
            self.times_interacted += 1

    def collision(self, *args):
        """Call appropraite collision function"""""
        if self.collision_interactable and self.on_collision != None:
            # Run correct function if the tile is interactable
            self.on_collision(self, *args)

    def copy(self):
        """Returns a copy of the object"""
        return InteractableTile(
            self.image,
            self.solid,
            self.meta,
            self.interaction,
            self.first_interaction,
            self.on_collision,
            self.interactable,
            self.collision_interactable,
            self.on_render,
            self.render_override
        )

class TileGroup():
    """Groups tiles together with shared metadata"""
    def __init__(self):
        """Initialize TileGroup"""
        self.tiles = {}
        self.meta = {}
        self.id = ""

    def add(self, tile):
        """Adds tile to group"""
        self.tiles[tile.pos] = tile

    def remove(self, tile_pos):
        """Remove tile from group"""
        del self.tiles[tile_pos]
        