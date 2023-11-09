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
from json import load
from scripts.utils import load_image, load_images, Animation
from scripts.interactions import *
from scripts.gameItems import Item
from scripts.itemAttributes import Cooldown, Accessory, HealthBoost, IFrameBoost, DamageBoost, DeffenseBoost, SpeedBoost
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
        'spikes' : InteractableTile(load_images('tiles/spikes'), False, {'tick':0, 'cooldown':0, 'spike-time':0, "damage":0, "offset":0}, interactable=False, on_collision=spike_damage, on_render=spike_tick, collision_interactable=False),
        'chest' : InteractableTile([load_image('tiles/chest/chest.png'), load_image('tiles/chest/open_chest.png')], True, {'item':"NaI", "ammount":1, 'opened':False}, open_chest, None, None, True, False, check_chest_state),
        'objective-chest' : InteractableTile([load_image("tiles/floors/floor_00.png")], False, {'item':"NaI", "ammount":1}, None, None, None, False, False, check_room_state)
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
        'arrow' : Projectile(load_image('entities/arrows/wooden_arrow.png'), 5, 7, arrow_hit)
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
        "NaI" : Item("NaI", 1, load_image("items/not_a_item.png")),
        "bucket" : Item("Bucket", 4, load_image('items/bucket.png'), interaction=pickup_item),
        "crushed-can" : Item("Crushed Can", 64, load_image('items/crushed_can.png'), interaction=pickup_item),
        "crumbled-paper" : Item("Crumbled Paper", 64, load_image('items/crumpled_paper.png'), interaction=pickup_item),
        "paper-cup" : Item("Paper Cup", 64, load_image('items/paper_cup.png'), interaction=pickup_item),
        "rotton-apple" : Item("Rotton Apple", 64, load_image('items/rotton_apple.png'), interaction=pickup_item),
        "wooden-bow" : Item("Wooden Bow", 1, load_image("items/bows/wooden_bow.png"), pickup_item, fire_arrow, None, True, {'cooldown':100, 'tick':0}, Cooldown()),
        "emerald-bow" :  Item("Wooden Bow", 1, load_image("items/bows/emerald_bow.png"), pickup_item, fire_arrow, None, True, {'cooldown':20, 'tick':0}, Cooldown()),
        "pink-spoon" : Item("Pink Spoon", 1, load_image("items/pink_spoon.png"), pickup_item),
        "heart-sigil" : Item("Heart Sigil (+10 Health)", 1, load_image("items/not_a_item.png"), pickup_item, None, None, False, {}, HealthBoost(10), Accessory()),
        "anklet-of-the-wind" : Item("Anklet of the Wind (+20% Speed)", 1, load_image("items/not_a_item.png"), pickup_item, None, None, False, {}, SpeedBoost(1.2) , Accessory()),
        "ninja-gear" : Item("Ninja Gear (+3 Immunity Frames)", 1, load_image("items/not_a_item.png"), pickup_item, None, None, False, {}, IFrameBoost(3), Accessory()),
        "armor-plate" : Item("Armor Plate (-8% Damage Reduction)", 1, load_image("items/not_a_item.png"), pickup_item, None, None, False, {}, DeffenseBoost(0.92), Accessory()),
        "steel-gauntlet" : Item("Steel Gauntlet (+5% Damage)", 1, load_image("items/not_a_item.png"), pickup_item, None, None, False, {}, DamageBoost(1.05), Accessory()),
        "glass-cannon" : Item("Glass Cannon (-60% Damage Reduction, +45% Damage)", 1, load_image("items/not_a_item.png"), pickup_item, None, None, False, {}, DamageBoost(1.45), DeffenseBoost(1.6), Accessory())
    }
    decor = {
        'rug' : load_image("decor/rug.png"),
        'skull' : load_image("decor/skull.png"),
        'large-rug' : load_image("decor/large_rug.png"),
        'bookshelf' : load_image("decor/bookshelf.png"),
        "cobweb" : load_image("decor/cobweb.png"),
        "danger" : load_image("decor/danger.png")
    }
    