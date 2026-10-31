# src/entities/obstacle.py
from ursina import Entity, color
import random

class Obstacle(Entity):
    def __init__(self, z_pos, **kwargs):
        super().__init__(**kwargs)
        self.model = 'cube'
        self.color = color.rgb(200, 50, 50)
        self.scale = (1.8, 1.2, 1.2)
        
        # Random lane (-1, 0, or 1)
        self.lane = random.choice([-1, 0, 1])
        self.x = self.lane * 2.5
        self.y = 0.6
        self.z = z_pos