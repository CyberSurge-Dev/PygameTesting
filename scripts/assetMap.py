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

class AssetMap():
    """Simple class to store the asset map"""
    tiles = {
        'wall' : {'type':'solid', 'variants' : load_images('tiles/walls')}, 
        'floor' : {'type':'floor', 'variants' : load_images('tiles/floors')},
        'note-wall' : {'type':'solid', 'variants' : load_images("tiles/note_walls"), "interaction" : show_text_box}
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
        'skeleton': {}
    }
    gui = {
        "itembar" : load_image("gui/hud/itembar.png"),
        "itembar_selected" : load_image("gui/hud/selected.png"),
        "interaction" : Animation(load_images("gui/icons/interaction"), 2),
        "text-box" : load_image("gui/text_box.png"),
        "close" : load_image("gui/icons/close.png"),
        "inventory" : load_image("gui/inventory.png")
    }
    items = {
        "sample" : {'icon' : load_image('items/test/sample.png')},
        "bucket" : Item("Bucket", 1, load_image('items/bucket.png'))
    }
    