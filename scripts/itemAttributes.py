# Created By: Zachary Hoover
# Created Date: 10/24/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
This program contains the classes for item attributes, attributes are modifiers that affect items

--+ Classes +-- 
Attribute() - 

"""
# --------------------------------------------------------------------------------

class Attribute():
    """Simple base class for all attributes.""" 
    def __init__(self):
        """Initialize variables"""
        self.active = False   
    def update(self, item, *args):
        """Updates the attribute"""
    def remove(self, *args):
        """Undo the effects"""
        

class Recyclable(Attribute):
    pass

class Trash(Attribute):
    pass

class Accessory(Attribute):
    pass

class Cooldown(Attribute):
    """
    Class for item cooldown, will overide any metadata called 'tick' or 'cooldown'.

    Cooldown between item actions, to check if item cooldown is up, check for the 'tick' metadata to be equal to
    0, and set it to 1 when you want to start another cooldown.
    """
    def update(self, item, *args):
        """Handles logic for cooldown"""
        if item.meta['tick'] != 0:
            # Increment the tick until it is greater than the cooldown
            if item.meta['tick'] < item.meta['cooldown']:
                item.meta['tick'] += 1
            else:
                item.meta['tick'] = 0

class HealthBoost():
    def __init__(self, boost):
        self.active = False
        self.boost = boost
        self.target = None
    def update(self, *args):
        if not self.active:
            self.target = args[1]
            self.active = True
            args[1].health_bar.max_health += self.boost
    def remove(self, *args):
        """Remove effect"""
        if self.active:
            self.active = False
            if self.target.health_bar.health > (self.target.health_bar.max_health - self.boost):
                self.target.health_bar.health = self.target.health_bar.max_health - self.boost
            self.target.health_bar.max_health -= self.boost
