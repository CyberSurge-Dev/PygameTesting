# Created By: Zachary Hoover
# Created Date: 9/26/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains the Asset map, a class of dictionaries that correlate with
tiles, entities, items, etc. The Asset Map also contains the images (sprites), and 
interacions of each asset. 

--+ Classes +-- 
AssetMap() - Simple class to store the asset map

"""
from scripts.utils import load_image, load_images, Animation
from scripts.interactions import *
from scripts.gameItems import Item
from scripts.itemAttributes import Trash, Recyclable, Cooldown
from scripts.tiles import Tile, InteractableTile
from scripts.entities import Enemy

class AssetMap():
    """Simple class to store the asset map"""
    tiles = {
        'NaT' : Tile(load_image('tiles/not_a_tile.png')),
        'wall' : Tile(load_images('tiles/walls'), True), 
        'floor' : Tile(load_images('tiles/floors')),
        'note-wall' : InteractableTile(load_images('tiles/note_walls'), True, {}, show_text_box, collision_interactable=False),
        'door' : InteractableTile(load_images('tiles/doors'), False, {}, interactable=False, on_collision=set_room),
        'chest' : InteractableTile(load_images("tiles/")),
        'spikes' : InteractableTile(load_images('tiles/spikes'), False, {'tick':0, 'cooldown':0, 'spike-time':0, "damage":0, "offset":0}, interactable=False, on_collision=spike_damage, on_render=spike_tick, collision_interactable=False)
    }
    entities = {
        'player': {
            'left' : Animation(load_images('entities/player/left'), 7),
            'right' : Animation(load_images('entities/player/right'), 7),
            'up' : Animation(load_images('entities/player/up'), 7),
            'down' : Animation(load_images('entities/player/down'), 7),
            'down-left' : Animation(load_images('entities/player/left'), 7),
            'down-right' : Animation(load_images('entities/player/right'), 7),
            'up-left' : Animation(load_images('entities/player/left'), 7),
            'up-right' : Animation(load_images('entities/player/right'), 7),
            'idle' : load_image('entities/player/player.png')
        },
        'skeleton': Enemy({
            'left' : Animation(load_images('entities/skeleton/left'), 5),
            'right' : Animation(load_images('entities/skeleton/right'), 5),
            'up' : Animation(load_images('entities/skeleton/up'), 5),
            'down' : Animation(load_images('entities/skeleton/down'), 5),
            'down-left' : Animation(load_images('entities/skeleton/left'), 5),
            'down-right' : Animation(load_images('entities/skeleton/right'), 5),
            'up-left' : Animation(load_images('entities/skeleton/left'), 5),
            'up-right' : Animation(load_images('entities/skeleton/right'), 5),
            'idle' : load_image('entities/skeleton/skeleton.png'),
        }),
        'arrow' : Projectile(load_image('entities/arrows/wooden_arrow.png'), 5, 10, arrow_hit)
    }
    gui = {
        "itembar" : load_image("gui/hud/itembar.png"),
        "itembar_selected" : load_image("gui/hud/selected.png"),
        "interaction" : Animation(load_images("gui/icons/interaction"), 2),
        "text-box" : load_image("gui/text_box.png"),
        "close" : load_image("gui/icons/close.png"),
        "inventory" : load_image("gui/inventory.png"),
        "health-emblem" : load_image("gui/health_bar/emblem.png"),
        "empty-health-bar" : load_image("gui/health_bar/empty_bar.png"),
        "filled-health-bar" : load_image("gui/health_bar/filled_bar.png"),
        "game-over-image" : load_image("gui/game_over/game_over_text.png"),
        "respawn-button" : load_image("gui/game_over/respawn_button.png")
    }
    items = {
        "bucket" : Item("Bucket", 4, load_image('items/bucket.png'), interaction=pickup_item),
        "crushed-can" : Item("Crushed Can", 64, load_image('items/crushed_can.png'), interaction=pickup_item),
        "crumbled-paper" : Item("Crumbled Paper", 64, load_image('items/crumpled_paper.png'), interaction=pickup_item),
        "paper-cup" : Item("Paper Cup", 64, load_image('items/paper_cup.png'), interaction=pickup_item),
        "rotton-apple" : Item("Rotton Apple", 64, load_image('items/rotton_apple.png'), interaction=pickup_item),
        "wooden-bow" : Item("Wooden Bow", 1, load_image("items/bows/wooden_bow.png"), pickup_item, fire_arrow, None, True, {'cooldown':10, 'tick':0}, Cooldown())
    }
    decor = {
        'desk' : {'variants': [load_image("tiles/desk.png")]},
        'bookshelf' : {'variants': [load_image("tiles/bookshelf.png")]},
    }
    
    