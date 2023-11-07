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
    def update(self, item):
        """Updates the attribute"""
        

class Recyclable(Attribute):
    pass

class Trash(Attribute):
    pass

class Cooldown(Attribute):
    """
    Class for item cooldown, will overide any metadata called 'tick' or 'cooldown'.

    Cooldown between item actions, to check if item cooldown is up, check for the 'tick' metadata to be equal to
    0, and set it to 1 when you want to start another cooldown.
    """
    def update(self, item):
        """Handles logic for cooldown"""
        if item.meta['tick'] != 0:
            # Increment the tick until it is greater than the cooldown
            if item.meta['tick'] < item.meta['cooldown']:
                item.meta['tick'] += 1
            else:
                item.meta['tick'] = 0