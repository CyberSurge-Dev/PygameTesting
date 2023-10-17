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

class AssetMap():
    """Simple class to store the asset map"""
    tiles = {
        'wall' : {'type':'solid', 'variants':load_images('tiles/walls')}, 
        'floor' : {'type':'floor', 'variants':load_images('tiles/floors')}
    }
    entities = {
        'player': load_image('entities/player/player.png'),
        'skeleton': {
        }
    }
    gui = {
        "Test" : load_image(r"gui/hud/itembar.png")
    }
    