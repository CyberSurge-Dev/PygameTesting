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
from scripts.entities import Projectile
import math

def fire_arrow(item, event, player):
    """Fire an arrow at event position, using metadata from item"""
    if item.meta['tick'] == 0:
        # Create an arrow, set trjectory and pos, append to render list
        pos = (player.game.sWidth//2, player.game.sHeight//2) # Base player position as center of screen
        print("player: ", pos, " Mouse:", event.pos)
        arrow = player.tilemap.assetMap.entities['arrow'].copy()
        tPos = player.pos.copy()
        arrow.set([tPos[0], tPos[1]+15], math.atan2((event.pos[1]-pos[1]), (event.pos[0]-pos[0]))) # Set arrow information
        player.projectiles.append(arrow)
        item.meta['tick'] = 1 # set to one to activate cooldown

def arrow_hit(arrow, entity):
    """Logic for when an arrow hits an entity"""
    entity.damage(arrow.damage)

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
    args[1].gameManager.set_room_from_id(args[1].tilemap.get_tile(tile.pos).meta.get('id', 0))
    # Set x and y postion, using an offset if the room is of an odd width
    if args[1].tilemap.size[0] % 2 == 0:
        args[1].pos = [(args[1].tilemap.size[0]//2)*args[1].tilemap.tile_size, (args[1].tilemap.size[1]//2)*args[1].tilemap.tile_size]
    else:
        args[1].pos = [(args[1].tilemap.size[0]//2)*args[1].tilemap.tile_size+args[1].tilemap.tile_size//2, (args[1].tilemap.size[1]//2)*args[1].tilemap.tile_size]

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

def spike_damage(tile, *args):
    if tile.collision_interactable:
        args[1].health_bar.damage(tile.meta['damage'])

def spike_tick(tile, disp, offset, tilesize, *args):
    """Increment spike ticks"""
    # Check offset
    if tile.meta['offset'] >= 0:
        tile.meta['offset'] -= 1
        if tile.meta['offset'] < 0:
            tile.collision_interactable = True
            tile.variant = 1

    if not tile.collision_interactable:
        if tile.meta['tick'] >= tile.meta['cooldown']:
            tile.meta['tick'] = 0
            tile.collision_interactable = True
            tile.variant = 1
            
        else:
            tile.collision_interactable = False
            tile.meta['tick'] += 1
            tile.variant = 0
            
    elif tile.collision_interactable:
        if tile.meta['tick'] >= tile.meta['spike-time']:
            tile.meta['tick'] = 0
            tile.collision_interactable = False
            tile.variant = 0
        else:
            tile.collision_interactable = True
            tile.meta['tick'] += 1
            tile.variant = 1
            
            
        
    