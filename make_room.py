# Created By: Zachary Hoover
# Created Date: 11/7/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
A crude program to create basic tilemaps (just the room outlines).

Makes blank, rectangular rooms.
"""
# --------------------------------------------------------------------------------
# External impots
import json

# --------------------------------------------------------------------------------
# Change these variables to create empty room files
filename = "room_19.json"
width = 7
height = 5
# Set how many doors you want on each side
doors = {
    "left" : 1,
    "right" : 0,
    "bottom" : 0,
    "top" : 0
}
path = "C:/Users/Zachary Hoover/Documents/PygameTesting/data/rooms/trial_chambers/"

# Create base dictionary to be written to the file
output = {
    "tilemap" : {},
    "tile-groups" : {},
    "items" : {},
    "decor" : {},
    "entities": {},
    "meta" : {}
}

for x in range(0, width):
    for y in range(0, height):
        key = f"{str(x)};{str(y)}"

        # Check top row
        if y == 0:
            if x == 0: # If on the top-left corner
                output['tilemap'][key] = {"id":"wall", "variant":1}
            elif x == width-1: # If on the top-right corner
                output['tilemap'][key] = {"id":"wall", "variant":7}
            else: # If anywere on top row that is not a corner
                output['tilemap'][key] = {"id":"wall", "variant":0}
        elif y == height-1: # Check bottom row
            if x == 0: # If on the bottom-left corner
                output['tilemap'][key] = {"id":"wall", "variant":8}
            elif x == width-1: # If on the top-right corner
                output['tilemap'][key] = {"id":"wall", "variant":10}
            else: # If anywere on top row that is not a corner
                output['tilemap'][key] = {"id":"wall", "variant":9}
        else: # Everything between
            if x == 0: # Check for a left-side piece
                output['tilemap'][key] = {"id":"wall", "variant":2}
            elif x == width-1: # Check for a right-side piece
                output['tilemap'][key] = {"id":"wall", "variant":6}
            else:
                output['tilemap'][key] = {"id":"floor"}
        # Check for sides

def evenly_distribute_items(room_width, num_items):
    if num_items <= 0:
        return []

    if room_width % 2 == 0:
        # If the room width is even, distribute items starting from 1/2 item width to room width
        item_spacing = room_width // (num_items + 1)
        if num_items > 1:
            start_position = 0
        else:   
            start_position = item_spacing // 2
    else:
        # If the room width is odd, distribute items starting from 0 to room width
        item_spacing = (room_width // num_items) + 1
        if num_items > 1:
            start_position = item_spacing // 2
        else:
            start_position = (item_spacing // 2)-1
            

    positions = [start_position + i * item_spacing for i in range(num_items)]
    return positions


# put doors in
id = 0
for wall, value in doors.items():
    if wall == "top":
        for pos in evenly_distribute_items(width-2, value):
            output['tilemap'][str(pos+1)+";0"] = {"id":"door", "variant":0, "meta":{"id":str(id)}}
            id += 1
    elif wall == "left":
        for pos in evenly_distribute_items(height-2, value):
            output['tilemap']["0;"+str(pos+1)] = {"id":"door", "variant":1, "meta":{"id":str(id)}}
            id += 1
    elif wall == "bottom":
        for pos in evenly_distribute_items(width-2, value):
            output['tilemap'][str(pos+1)+f";{height-1}"] = {"id":"door", "variant":2, "meta":{"id":str(id)}}
            id += 1
    else:
        for pos in evenly_distribute_items(height-2, value):
            output['tilemap'][f"{width-1};"+str(pos+1)] = {"id":"door", "variant":3, "meta":{"id":str(id)}}
            id += 1
        
print(output)
# Serializing json
json_object = json.dumps(output, indent=4)

# Write output to file
with open(path+filename, "w") as outfile:
    outfile.write(json_object)

