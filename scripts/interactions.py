# Created By: Zachary Hoover
# Created Date: 10/28/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This file contains functions for game interactions, these range from item item and tile interactions, 
to functions used by any game elements.
"""
# --------------------------------------------------------------------------------
# Internal imports 
from scripts.guiElements import ClosableTextBox
from scripts.utils import blit
from scripts.itemAttributes import Trash, Recyclable
from scripts.guiElements import ClosableTextBox

def show_text_box(item, player):
    """Shows a textbox to the screen with the text passed in"""
    print("Text-Box")
    player.hud.add(str(item.pos), ClosableTextBox(player.game.dPos.BOTTOM_CENTER, player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], item.meta['text']))
    print("CALLED RENDER")

def render_trash(disp, offset, game, loc):
    blit(disp, game.trash_font, (loc[0]*game.tilemap.tile_size-offset[0], loc[1]*game.tilemap.tile_size-offset[1]))

def render_recycle(disp, offset, game, loc):
    blit(disp, game.recyclables_text, (loc[0]*game.tilemap.tile_size-offset[0], loc[1]*game.tilemap.tile_size-offset[1]))

def on_interact_trash(item, player):
    for attribute in player.itembar.items[player.itembar.slot_selected][0].attributes:
        if isinstance(attribute, Recyclable):
            player.hud.add('temp-box', ClosableTextBox(player.game.dPos.BOTTOM_CENTER, player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], ['I cannot put recycables in the trash!']))
        elif isinstance(attribute, Trash):
            player.game.trash_collected +=  player.itembar.items[player.itembar.slot_selected][1]
            player.itembar.items[player.itembar.slot_selected] = (None, 0)

def set_room(tile, *args):
    args[0].gameManager.set_room_from_id(args[0].tilemap.get_tile(tile.pos).meta.get('id', 0))
    args[0].pos = [(args[0].tilemap.size[0]//2)*args[0].tilemap.tile_size+args[0].tilemap.tile_size//2, (args[0].tilemap.size[1]//2)*args[0].tilemap.tile_size]

def on_interact_recycle(item, player):
    for attribute in player.itembar.items[player.itembar.slot_selected][0].attributes:
        if isinstance(attribute, Trash):
            player.hud.add('temp-box', ClosableTextBox(player.game.dPos.BOTTOM_CENTER, player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], ['I cannot put trash in the recycables!']))
        elif isinstance(attribute, Recyclable):
            player.game.recyclables_collected +=  player.itembar.items[player.itembar.slot_selected][1]
            player.itembar.items[player.itembar.slot_selected] = (None, 0)

def pickup_item(item, player):
    player.inventory.add(item.copy())
    item.hide()

def on_off(tile, *args):
    if tile.meta.get('state', False):
        tile.variant = 1
    else:
        tile.variant = 0