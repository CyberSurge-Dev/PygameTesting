# Created By: Zachary Hoover
# Created Date: 9/17/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains many general-purpose classes used throughout the program.

Settings() - The settings class is used to load settings information from settings.json.
Animation() - The animation classs is used as a system to generalize the creation of aniumations throughout the program.
"""
# --------------------------------------------------------------------------------
# External imports
from tkinter import Tk
import pygame
import pygame.locals
import json

# Internal imports

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

        self.keybinds = {} # Create an empty dictionary for keybinds
        for key in self.settings_data["keybinds"].keys(): # cycle through the keybinds dictionary from settings.json
            self.keybinds[key] = getattr(pygame.locals, "K_" + self.settings_data["keybinds"][key]) # set the keybind value to the pygame key attribute that corrosponds the value from settings.json using getattr()

class Animation():
    pass





        

    
