# Created By: Zachary Hoover
# Created Date: 9/17/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains the main running code for the program, as well as the Game object with the game loop.
This program updates the other game objects and acts an event handler for the program.

Game - The game class is the main object in the program, managing the update, rendering, and events of game objects.
"""
# --------------------------------------------------------------------------------
# External impots
import pygame
import sys

# Internal imports
from scripts.utils import Settings
# --------------------------------------------------------------------------------

class Game():
    def __init__(self):
        """Initiate game object with attributes for game"""
        # Initialize pygame
        pygame.init()

        self.settings = Settings() # Initiate settings class
        self.screen = pygame.display.set_mode(self.settings.screen_size) # Set screen size
        self.keybinds = self.settings.keybinds # gets a dictionary for game keybinds

        self.clock = pygame.time.Clock() # Create the game clock



    def run(self):
        """Main game loop, handels updates and most game processes"""
        while True:

            for event in pygame.event.get(): # Chack pygame events
                if event.type == pygame.QUIT: # Check if the X on the window was clicked
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: # Check for buttons that were pressed
                    if event.key == self.keybinds["forward"]: # Check for the forward button being pressed
                        pass
                    if event.key == self.keybinds["backward"]: # Check for the backward button being pressed
                        pass
                    if event.key == self.keybinds["left"]: # Check for the left button being pressed
                        pass
                    if event.key == self.keybinds["right"]: # Check for the right button being pressed
                        pass                       

                if event.type == pygame.KEYUP: # Check for buttons that were released
                    if event.key == self.keybinds["forward"]: # Check for the forward button being released
                        pass
                    if event.key == self.keybinds["backward"]: # Check for the backward button being released
                        pass
                    if event.key == self.keybinds["left"]: # Check for the left button being released
                        pass
                    if event.key == self.keybinds["right"]: # Check for the right button being released
                        pass
                        
            pygame.display.update() # Refresh the display
            self.clock.tick(60) # Limit FPS to 60 

Game().run() # Initialize and run the game