# Created By: Zachary Hoover
# Created Date: 10/16/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains base classes to create gui objects eaily throughout the program

--+ Classes +-- 


"""
# --------------------------------------------------------------------------------

class MenuItem():
    """Simple base class for all menu buttons"""

    def __init__(self, pos, size, game, scale, center = True):
        """Initiazlizes the menu item""" ""
        if center:
            self.pos = (pos[0]-(size[0]//2), pos[1]-(size[1]//2))
        else:
            self.pos = pos
        self.size = size
        self.game = game
        self.scale = scale

    def render(self, disp):
        """Renders the menu item"""

    def check_events(self):
        """Check the events for the menu item""" ""
        s_pos = (int(self.pos[0] * self.scale[0]), int(self.pos[1] * self.scale[1]))

class Button(MenuItem):
    """Button menu item"""

    def __init__(self, pos, size, game, scale, image, text, func):
        """Initializes the button"""
        super().__init__(pos, size, game, scale)
        self.text = text
        self.func = func
        self.image = image

    def check_events():
        """Checks for clicks on button"""

    def render(self, disp):
        disp.blit(self.image, self.pos)


