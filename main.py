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
from scripts.utils import Settings, Telemetry, DisplayPositions, GameManager
from scripts.entities import Player
from scripts.assetMap import AssetMap
from scripts.tilemap import Tilemap
# --------------------------------------------------------------------------------

class Game():
    """The game class is the main object in the program, managing the update, rendering, and events of game objects."""
    def __init__(self):
        """Initiate game object with attributes for game"""
        # Initialize pygame
        pygame.init()

        self.settings = Settings() # Initiate settings class

        # Create seperate display and screen elements to be able to easily scale to any screen size
        self.display = pygame.Surface((384, 216)) # Only write to this surface 
        self.screen = pygame.display.set_mode(self.settings.screen_size) # Set screen size

        self.keybinds = self.settings.keybinds # gets a dictionary for game keybinds
        self.sWidth = pygame.display.get_window_size()[0]
        self.sHeight = pygame.display.get_window_size()[1]

        self.assetMap = AssetMap()

        self.tilemap = Tilemap(self, 32)
        self.trash_collected = 0
        self.recyclables_collected = 0
        self.total_trash = 10
        self.total_recyclables = 10
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        self.trash_font = self.font.render(f"0 / {self.total_trash}", True, (255, 250, 250))
        self.recyclables_text = self.font.render(f"0 / {self.total_recyclables}", True, (255, 250, 250))
        

        self.telemetry = Telemetry(self.settings.telemetry)

        self.movement = {
            'up':False,
            'down':False,
            'left':False,
            'right':False
        }

        self.scroll = [0 , 0]

        # Determine the largest 16:9 ratio that can fit in the screen for the display size
        # This method allows the program to automatically scale the game to any screen size
        if (self.sWidth < self.sHeight or self.sWidth == self.sHeight):
            self.dWidth = self.sWidth - (self.sWidth % 16)
            self.dHeight = math.trunc(self.dWidth * (9/16))
        else:
            self.dHeight = self.sHeight - (self.sHeight % 9)
            self.dWidth = math.trunc(self.dHeight * (16/9)) 

        self.scale = (self.sWidth / self.display.get_width(), self.sHeight / self.display.get_height())
        self.dPos = DisplayPositions((self.display.get_width(), self.display.get_height()))
        
        self.gameManager = GameManager('data/saves/test_save', self.tilemap)
        self.player = Player(self, (128, 128), (32, 32), self.gameManager)
        
        
        self.clock = pygame.time.Clock() # Create the game clock

    def test(self):
        pass

    def update_trash(self):
        self.trash_font = self.font.render(f"{self.trash_collected} / {self.total_trash}", True, (255, 250, 250))
        self.recyclables_text = self.font.render(f"{self.recyclables_collected} / {self.total_recyclables}", True, (255, 250, 250))

    def run(self):
        """Main game loop, handels updates and most game processes"""  
        while True:
            for event in pygame.event.get(): # Chack pygame events
                if event.type == pygame.QUIT: # Check if the X on the window was clicked
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: # Check for buttons that were pressed
                    if event.key == self.keybinds["up"]: # Check for the forward button being pressed
                        self.movement['up'] = True
                    if event.key == self.keybinds["down"]: # Check for the backward button being pressed
                        self.movement['down'] = True
                    if event.key == self.keybinds["left"]: # Check for the left button being pressed
                        self.movement['left'] = True
                    if event.key == self.keybinds["right"]: # Check for the right button being pressed
                        self.movement['right'] = True                       

                if event.type == pygame.KEYUP: # Check for buttons that were released
                    if event.key == self.keybinds["up"]: # Check for the forward button being released
                        self.movement['up'] = False
                    if event.key == self.keybinds["down"]: # Check for the backward button being released
                        self.movement['down'] = False
                    if event.key == self.keybinds["left"]: # Check for the left button being released
                        self.movement['left'] = False
                    if event.key == self.keybinds["right"]: # Check for the right button being released
                        self.movement['right'] = False

                self.player.check_events(event)
            
            # Create scroll offsets to have camera 'lag' behind the player for more fluid movement
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 5 # Smaller the last value (5), the less the lag 
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 5 # Smaller the last value (5), the less the lag 
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.screen.fill((20, 20, 20))
            self.display.fill((30, 30, 30))

            # Render the tilemap
            self.tilemap.render(self.display, render_scroll)

            # Update movement and render player (and HUD elements)
            self.player.update(**self.movement)
            self.player.render(self.display, render_scroll)

            # Scale the display surface to best fit the screen
            self.screen.blit(pygame.transform.scale( self.display, (self.dWidth, self.dHeight) ), 
                             ((self.sWidth/2)-(self.dWidth/2) , (self.sHeight/2)-(self.dHeight/2)))

            # Update Telemetry data
            self.telemetry.update() # update telemetry data
            # Update the display with data
            pygame.display.update() # Refresh the display
            
            self.clock.tick(60) # Limit FPS to 60 

Game().run() # Initialize and run the game