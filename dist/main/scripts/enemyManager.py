# Created By: Zachary Hoover
# Created Date: 11/6/2023
# Version: 1.0
# --------------------------------------------------------------------------------
"""
Enemy manager class, holds list of enemies and target player to determine movement. 

"""
# --------------------------------------------------------------------------------
# External imports
import pygame

class EnemyManager():
    """Enemy manager class, holds list of enemies and target player to determine movement. """
    def __init__(self):
        """Initialize variables for EnemyManager"""
        self.enemies = []
        
    def update(self, physicsEntity):
        """Update the enemies with player location to determine what movement the enemy will make."""
        for enemy in self.enemies:
            if enemy.health < 0:
                enemy.on_death(enemy, self)
                self.enemies.remove(enemy)
            else:
                enemy.update(physicsEntity)
                
    def render(self, disp, offset):
        """Render enemies to screen"""
        for enemy in self.enemies:
            enemy.render(disp, offset)
            
    def add(self, enemy):
        """Add enemy to manager"""
        self.enemies.append(enemy)

    def check_collisions(self, rect):
        """Check if rect collided with any entities"""
        entities = []
        for entity in self.enemies:
            if entity.rect().colliderect(rect):
                entities.append(entity)

        return entities