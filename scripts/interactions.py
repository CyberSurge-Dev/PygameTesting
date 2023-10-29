# Created By: Zachary Hoover
# Created Date: 10/28/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains functions for game interactions

"""
# --------------------------------------------------------------------------------
# Internal imports 
from scripts.guiElements import ClosableTextBox
from scripts.utils import blit
from scripts.itemAttributes import Trash, Recyclable

def show_text_box(item, player):
    """Shows a textbox to the screen with the text passed in"""
    player.hud.add(str(item['pos']), ClosableTextBox(player.game.dPos.BOTTOM_CENTER, player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], item['text']))
    print("CALLED RENDER")

def render_trash(disp, offset, game, loc):
    blit(disp, game.trash_font, (loc[0]*game.tilemap.tile_size-offset[0], loc[1]*game.tilemap.tile_size-offset[1]))

def render_recycle(disp, offset, game, loc):
    blit(disp, game.recyclables_text, (loc[0]*game.tilemap.tile_size-offset[0], loc[1]*game.tilemap.tile_size-offset[1]))

def on_interact_trash(item, player):
    if Recyclable in player.itembar.items[player.itembar.slot_selected][1].attributes:
        pass # add code for this here
    
def on_interact_recycle(item, player):
    pass

def pickup_item(item, player):
    player.inventory.add(item.copy())
    item.hide()
    