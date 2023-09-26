from scripts.utils import load_image, load_images, Animation

class AssetMap():
    """Simple class to store the asset map"""
    tiles = {
        'wall' : {'type':'solid', 'variants':load_images('tiles/walls')}  
    }
    entities = {
        'player': {
            'idle':Animation(load_images('entities/player/idle'), 4)
        },
        'skeleton': {
            
        }
    }