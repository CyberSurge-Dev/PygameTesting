# Created By: Zachary Hoover
# Created Date: 9/17/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains many general-purpose classes and functions used throughout the program.

--+ Classes +-- 
Settings() - The settings class is used to load settings information from settings.json.
Animation(images, image_dur, loop = False) - The animation classs is used as a system to generalize the creation 
                                             of aniumations throughout the program.
Telemetry(active) - Simple class for tracking variables and displaying/changing telemetry data in console.
GameManager() - The game manager class is used to manage and load save files.

--+ Functions +-- 
load_image(path) - Loads the image at the given path, and returns it as a pygame image object.
load_images(path) - Loads all images in given path and returns them as a list of pygame image objects.
blit(surface, image, pos) - Simple replacment for blit, allows Animations to be passed in.

--+ Variables +-- 
BASE_IMAGE_PATH - Stores the base path were all images are stored.
clear - Stores the function to clear the console for Telemetry Data.

"""
# --------------------------------------------------------------------------------
# External imports
from tkinter import Tk
import pygame
import pygame.locals
import json
import os

# Global variables
BASE_IMAGE_PATH = "data/images/"
clear = lambda: os.system('clear' if os.name == 'posix' else 'cls')
screen = None
# --------------------------------------------------------------------------------

class GameManager():
    """The game manager class is used to manage and load save files."""
    def __init__(self, save_file, tilemap, game):
        """Initialize GameManager variables"""
        global screen
        screen = game.font_screen
        
        self.tilemap = tilemap
        with open(save_file+'/rooms.json') as f:
            self.rooms = {int(k): v for k, v in json.load(f).items()}
        self.tilemap.load(self.rooms[0]['room'])
        self.current_room = 0

    def set_room(self, room):
        self.tilemap.load(self.rooms[room]['room'])
        
    def set_room_from_id(self, door_id):
        self.tilemap.load(self.rooms[ int(self.rooms[self.current_room]['doors'][str(door_id)]) ] ['room'])
        self.current_room = int(self.rooms[self.current_room]['doors'][str(door_id)])

class Settings():

    def __init__(self):
        """Initialize variables with information relevent throughout the program, as well as manage the settings file"""
        
        settingsJSON = open("data/settings.json",
                            "r")  # open the JSON file for settings
        self.settings_data = json.load(
            settingsJSON)  # Extract data from JSON as dictionary
        settingsJSON.close()  # Close JSON file

        if self.settings_data['display'][
                'fullscreen']:  # Check is fullscreen is enabled
            root = Tk()
            self.screen_size = (
                root.winfo_screenwidth(), root.winfo_screenheight()
            )  # Set the screen size to the current display size
        else:
            self.screen_size = (self.settings_data['display']['resolution'][0],
                                self.settings_data['display']['resolution'][1]
                                )  # Set screen to size from settings.json
            

        # Assign keybinds from settings
        self.keybinds = {}  # Create an empty dictionary for keybinds
        for key in self.settings_data["keybinds"].keys(
        ):  # cycle through the keybinds dictionary from settings.json
            self.keybinds[key] = getattr(
                pygame.locals, "K_" + self.settings_data["keybinds"][key]
            )  # set the keybind value to the pygame key attribute that corrosponds the value from settings.json using getattr()

        # Set developer Settings
        if self.settings_data['developer']['developer']:
            self.telemetry = self.settings_data['developer']['telemetry']
        else:
            self.telemetry = False


class DisplayPositions:
    """Simple utility class to store display positions"""

    def __init__(self, display_size):
        """Using the dislpay size, set the positions of the display""" ""
        self.CENTER = (display_size[0] // 2, display_size[1] // 2)
        self.BOTTOM_CENTER = (display_size[0] // 2, display_size[1])
        self.TOP_CENTER = (display_size[0] // 2, 0)
        self.TOP_LEFT = (0, 0)
        self.TOP_RIGHT = (display_size[0], 0)
        self.BOTTOM_LEFT = (0, display_size[1])
        self.BOTTOM_RIGHT = (display_size[0], display_size[1])


class Telemetry:
    """Simple class for tracking variables and displaying/changing telemetry data in console."""

    def __init__(self, active):
        """Initiate the telemtry class and variables"""
        self.telemetry_data = {}
        self.telemetry_log = []
        self.active = active

    def add(self, key, value):
        """Adds the given key and value to the telemetry values"""
        self.telemetry_data[key] = value

    def update(self):
        """Clears the screen and displays the telemetry data"""
        if self.active:
            clear()
            for k, v in self.telemetry_data.items():
                print(f"{k}: {v}")

            self.telemetry_data = {}

            # Print persistent data to screen
            print("\nTelemetry Log:")
            for item in reversed(self.telemetry_log):
                print(" ", item)

    def remove(self, key):
        """Removes given key from telemetry data"""
        self.telemetry_data.pop(key, None)

    def log(self, value):
        """Add persistent data to telemetry (will not be removed on update)"""
        self.telemetry_log.append(value)
        if len(self.telemetry_log) > 50:
            self.telemetry_log = self.telemetry_log[1:52]


def load_image(path):
    """Loads the image at the given path, and returns it as a pygame image object."""
    return pygame.image.load(BASE_IMAGE_PATH +
                             path)  # returns the loaded pygame image object


def blit(surface, image, pos):
    if image == None:
        pass
    elif type(image) == Animation:
        surface.blit(image.tick(), pos)
    else:
        surface.blit(image, pos)

def render_font(font, scale, pos):
    """Poorly made hack to fix the low resolution font rendering"""
    print(screen)
    print((pos[0]*scale[0], pos[1]*scale[1]))
    blit(screen, font, (pos[0]*scale[0], pos[1]*scale[1]))

def load_images(path):
    """Loads all images in given path and returns them as a list of pygame surface objects (can also be Animation objects)."""
    images = []
    for img in sorted(os.listdir(BASE_IMAGE_PATH + path)):  # Cycles through file paths of given directory (uses sorted() for Linux compatibility)
        if os.path.isdir(os.path.join(BASE_IMAGE_PATH + path, img)):
            images.append(Animation(load_images(os.path.join(path, img))))
        else:
            images.append(load_image(path + "/" + img))  # Saves the loaded image in the images list

    return images  # Return the list of pygame image objects


class Animation():
    """Animation object, stores frames and is ued for animated images"""

    def __init__(self, frames, fps=5):
        """Initialize variables needed for animation"""
        self.frames = frames
        self.frame_index = 0  # Current frame
        self.fps = fps
        self.current_tick = 0  # Current tick
        self.frame_time = 60 / fps  # Calculate the time between frames in game ticks

    def tick(self):
        """Increment the animation one tick, returns current frame"""
        # Increment current tick
        if self.current_tick >= self.frame_time:
            self.current_tick = 0
            # Increment to the next frame index
            if self.frame_index < len(self.frames) - 1:
                self.frame_index += 1
            else:
                # Reset frame back to beginning
                self.frame_index = 0
        else:
            self.current_tick += 1

        return self.frames[self.frame_index]

    def current_frame(self):
        """Returns the current frame"""
        return self.frames[self.frame_index]
