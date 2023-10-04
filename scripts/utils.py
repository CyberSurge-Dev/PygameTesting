# Created By: Zachary Hoover
# Created Date: 9/17/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains many general-purpose classes and functions used throughout the program.

--+ Classes +-- 
Settings() - The settings class is used to load settings information from settings.json.
Animation(images, image_dur, loop = False) - The animation classs is used as a system to generalize the creation of aniumations throughout the program.
Telemetry(active) - Simple class for tracking variables and displaying/changing telemetry data in console.

--+ Functions +-- 
load_image(path) - Loads the image at the given path, and returns it as a pygame image object.
load_images(path) - Loads all images in given path and returns them as a list of pygame image objects.

--+ Variables +-- 
BASE_IMAGE_PATH - Stores the base path were all images are stored.

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

# --------------------------------------------------------------------------------

class Settings():
    def __init__(self):
        """Initialize variables with information relevent throughout the program, as well as manage the settings file"""
        
        settingsJSON = open("data/settings.json", "r") # open the JSON file for settings
        self.settings_data = json.load(settingsJSON) # Extract data from JSON as dictionary
        settingsJSON.close() # Close JSON file

        if self.settings_data['display']['fullscreen']: # Check is fullscreen is enabled
            root = Tk()
            self.screen_size = (root.winfo_screenwidth(), root.winfo_screenheight()) # Set the screen size to the current display size
        else: 
            self.screen_size = (self.settings_data['display']['resolution'][0], self.settings_data['display']['resolution'][1]) # Set screen to size from settings.json

        # Assign keybinds from settings
        self.keybinds = {} # Create an empty dictionary for keybinds
        for key in self.settings_data["keybinds"].keys(): # cycle through the keybinds dictionary from settings.json
            self.keybinds[key] = getattr(pygame.locals, "K_" + self.settings_data["keybinds"][key]) # set the keybind value to the pygame key attribute that corrosponds the value from settings.json using getattr()

        # Set developer Settings
        if self.settings_data['developer']['developer']:
            self.telemetry = self.settings_data['developer']['telemetry']
        else:
            self.telemetry = False

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
    return pygame.image.load(BASE_IMAGE_PATH + path) # returns the loaded pygame image object

def load_images(path):
    """Loads all images in given path and returns them as a list of pygame image objects."""
    images = []
    for img in sorted(os.listdir(BASE_IMAGE_PATH + path)): # Cycles through file paths of given directory (uses sorted() for Linux compatibility)
         images.append(load_image(path + "/" + img)) # Saves the loaded image in the images list

    return images # Return the list of pygame image objects
    

class Animation():
    pass

