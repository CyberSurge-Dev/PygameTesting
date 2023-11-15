# Created By: Zachary Hoover
# Created Date: 10/28/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This file contains functions for game interactions, these range from item item and tile interactions, 
to functions used by any game elements.
"""
# --------------------------------------------------------------------------------
# External imports
import math
import json
import pygame

# Internal imports 
from scripts.guiElements import ClosableTextBox, EndScreen
from scripts.itemAttributes import Trash, Recyclable
from scripts.guiElements import ClosableTextBox
from scripts.entities import Projectile
from scripts.itemAttributes import Accessory
from scripts.utils import convert_time

def game_end_screen(*args):
    """Show the game end screen"""
    if args[1].gameManager.get_meta('completed') == True:
        args[1].hud.add("game-end", EndScreen((args[1].game.dPos.CENTER[0], args[1].game.dPos.CENTER[1]-15), args[1].game.scale, 
                  args[1].assetMap.gui['game-end-image'],
                  args[1].assetMap.gui['restart-button'],
                  args[1].assetMap.gui['continue-button'],
                  args[1]
                  ))
        
def check_room_state(tile, disp, offset, tile_size, tilemap):
    """Checks room metadata to figure out if tile should be converted to a chest."""
    if tilemap.gameManager.get_meta("completed") == True:
        chest = tilemap.assetMap.tiles['chest'].copy()
        # Set specific tiledata from old tile
        chest.meta.update(tile.meta)
        chest.pos = tile.pos
        chest.meta = chest.meta.copy()
        tilemap.tilemap[tile.pos] = chest

def check_room_state_doors(tile, disp, offset, tile_size, tilemap):
    """Checks room metadata to figure out if tile should be converted to a chest."""
    if tilemap.gameManager.get_meta("completed") == True:
        door = tilemap.assetMap.tiles['door'].copy()
        door.meta.update(tile.meta)
        # Set specific tiledata from old tile
        door.pos = tile.pos
        door.meta = door.meta.copy()
        door.variant = tile.variant # Set tile varient
        tilemap.tilemap[tile.pos] = door

def open_chest(tile, player):
    """Handles what will happen when a chest is interacted with"""
    # Remove old text-box, if there is one
    player.hud.remove("text-box")
    print(tile.meta)
    if not tile.meta['opened']:
        if tile.meta.get("text", None) == None: # Display default message if none is set
            # add items in chest to player inventory
            for i in range(0, tile.meta.get('ammount', 1)):
                player.inventory.add(player.tilemap.assetMap.items[tile.meta.get('item', 'NaI')].copy())
            tile.meta['opened'] = True
            player.gameManager.add_meta(tile.pos, {'opened' : True})
            tile.variant = 1
            # Display a message for the player
            
            # Check if the item is an accessory (to display a seprate message)
            isAccessory = False # Check if the item is an accessory
            for attribute in player.tilemap.assetMap.items[tile.meta.get('item', 'NaI')].attributes:
                if isinstance(attribute, Accessory):
                    isAccessory = True
            if isAccessory:
                # Display a different message if the item is an accessory
                if tile.meta.get('tag', None) != None:
                    player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], 
                                                        [f"I got a {player.tilemap.assetMap.items[tile.meta.get('item', 'NaI')].display_name} Accessory!", "", f"Press ' {player.game.settings.settings_data['keybinds'].get('inventory', 'NaK')} ' to open your inventory and equip it.", "Press it again to close."]))
                else: 
                    player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], 
                                                        [f"I got a {player.tilemap.assetMap.items[tile.meta.get('item', 'NaI')].display_name} Accessory!", "", f"Press ' {player.game.settings.settings_data['keybinds'].get('inventory', 'NaK')} ' to open your inventory and equip it.", "Press it again to close."],
                                                        player.assetMap.tags.get(tile.meta.get('tag', None), None), True, player
                                                        ))
            else:
                if tile.meta.get('tag', None) != None:
                    player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], 
                                                        [f"I got a {player.tilemap.assetMap.items[tile.meta.get('item', 'NaI')].display_name}!"],
                                                        player.assetMap.tags.get(tile.meta.get('tag', None), None), True, player
                                                        ))
                else:
                    player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], 
                                                        [f"I got a {player.tilemap.assetMap.items[tile.meta.get('item', 'NaI')].display_name}!"]))
        else:
            # add items in chest to player inventory
            for i in range(0, tile.meta.get('ammount', 1)):
                player.inventory.add(player.tilemap.assetMap.items[tile.meta.get('item', 'NaI')].copy())
            tile.meta['opened'] = True
            player.gameManager.add_meta(tile.pos, {'opened' : True})
            tile.variant = 1

            # Display message set in tilemap
            if tile.meta.get('tag', None) != None: 
                player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], 
                                                        tile.meta.get('text', []),
                                                        player.assetMap.tags.get(tile.meta.get('tag', None), None), True, player
                                                        ))
            else:
                player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], 
                                                        tile.meta.get('text', [])))
    else:
        # Display a message fro the player
        player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], ["This chest is empty!"]))

def check_chest_state(tile, *args):
    """Check the state of the chest, set variant"""
    if tile.meta['opened']:
        tile.variant = 1

def fire_arrow(item, event, player):
    """Fire an arrow at event position, using metadata from item"""
    if item.meta['tick'] == 0:
        # Create an arrow, set trjectory and pos, append to render list
        pos = (player.game.sWidth//2, player.game.sHeight//2) # Base player position as center of screen
        print("player: ", pos, " Mouse:", event.pos)
        arrow = player.tilemap.assetMap.entities['arrow'].copy()
        tPos = player.pos.copy()
        arrow.set([tPos[0]+16, tPos[1]+13], math.atan2((event.pos[1]-pos[1]), (event.pos[0]-pos[0]))) # Set arrow information, shift arrow start pos in a stupid way
        print(arrow, "has been added to projectiles")
        player.projectiles.append(arrow)
        item.meta['tick'] = 1 # set to one to activate cooldown

def arrow_hit(arrow, entity):
    """Logic for when an arrow hits an entity"""
    entity.damage(arrow.damage)

def show_text_box(item, player):
    """Shows a textbox to the screen with the text passed in"""
    # Remove old text-box, if there is one
    player.hud.remove("text-box")
    player.hud.add("text-box", ClosableTextBox((player.game.dPos.TOP_CENTER[0], 42), player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], item.meta['text']))
    player.gameManager.add_meta(item.pos, {'checked' : True})

def on_interact_trash(item, player):
    for attribute in player.itembar.items[player.itembar.slot_selected][0].attributes:
        if isinstance(attribute, Recyclable):
            player.hud.add('temp-box', ClosableTextBox(player.game.dPos.BOTTOM_CENTER, player.game.scale, player.assetMap.gui['text-box'], player.assetMap.gui['close'], ['I cannot put recycables in the trash!']))
        elif isinstance(attribute, Trash):
            player.game.trash_collected +=  player.itembar.items[player.itembar.slot_selected][1]
            player.itembar.items[player.itembar.slot_selected] = (None, 0)

def set_room(tile, *args):
    # Remove old text-box, if there is one
    args[1].hud.remove("text-box")
    args[1].gameManager.set_room_from_id(args[1].tilemap.get_tile(tile.pos).meta.get('id', 0))
    # Set x and y postion, using an offset if the room is of an odd width
    if args[1].tilemap.size[0] % 2 == 0:
        args[1].pos = [(args[1].tilemap.size[0]//2)*args[1].tilemap.tile_size, (args[1].tilemap.size[1]//2)*args[1].tilemap.tile_size]
    else:
        args[1].pos = [(args[1].tilemap.size[0]//2)*args[1].tilemap.tile_size+args[1].tilemap.tile_size//2, (args[1].tilemap.size[1]//2)*args[1].tilemap.tile_size]

    if args[1].gameManager.get_meta("text") != {}:
        args[1].hud.add("text-box", ClosableTextBox((args[1].game.dPos.TOP_CENTER[0], 42), args[1].game.scale, args[1].assetMap.gui['text-box'], args[1].assetMap.gui['close'], args[1].gameManager.get_meta("text")))
   
    if tile.meta.get('tag', None) != None:
        args[1].assetMap.tags.get(tile.meta.get('tag'))(*args)

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

def spike_tick(tile, *args):
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
            
            
        
    