# Created By: Zachary Hoover
# Created Date: 9/17/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains the main running code for the program, as well as the Game object with the game loop.
This program updates the other game objects and acts an event handler for the program.

--+ Classes +--
Game() - The game class is the main object in the program, managing the update, rendering, and events of game objects.
"""
# --------------------------------------------------------------------------------
# External impots
import pygame, sys, math

# Internal imports
from scripts.utils import Settings
# --------------------------------------------------------------------------------

class Game():
    """The game class is the main object in the program, managing the update, rendering, and events of game objects."""
    def __init__(self):
        """Initiate game object with attributes for game"""
        # Initialize pygame
        pygame.init()

        self.settings = Settings() # Initiate settings class

        # Create seperate display and screen elements to be able to easily scale to any screen size
        self.display = pygame.Surface((640, 360)) # Only write to this surface 
        self.screen = pygame.display.set_mode(self.settings.screen_size) # Set screen size
        
        self.keybinds = self.settings.keybinds # gets a dictionary for game keybinds
        self.sWidth = pygame.display.get_window_size()[0]
        self.sHeight = pygame.display.get_window_size()[1]

        # Determine the smallest 16:9 ratio that can fit in the screen for the display size
        if (self.sWidth < self.sHeight or self.sWidth == self.sHeight):
            self.dWidth = self.sWidth - (self.sWidth % 16)
            self.dHeight = math.trunc(self.dWidth * (9/16))
        else:
            self.dHeight = self.sHeight - (self.sHeight % 16)
            self.dWidth = math.trunc(self.dHeight * (16/9)) 
        
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

            self.screen.fill((20, 20, 20))
            self.display.fill((30, 30, 30))
            
            self.display.blit(pygame.image.load("data/sprite.png").convert(), (5, 5))
            

            self.screen.blit(pygame.transform.scale( self.display, (self.dWidth, self.dHeight) ), 
                             (  (self.sWidth/2)-(self.dWidth/2) , (self.sHeight/2)-(self.dHeight/2) ))
            
            pygame.display.update() # Refresh the display
            self.clock.tick(60) # Limit FPS to 60 

Game().run() # Initialize and run the game