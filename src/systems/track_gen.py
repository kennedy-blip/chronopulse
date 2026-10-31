# src/systems/track_gen.py
from ursina import Entity, color
import math

class TrackGenerator:
    def __init__(self, segment_length=25, pool_size=12):
        self.segment_length = segment_length
        self.pool_size = pool_size
        self.segments = []
        self.buildings_left = []
        self.buildings_right = []

        for i in range(self.pool_size):
            z_pos = i * segment_length
            
            # Road segment
            road = Entity(
                model='cube',
                scale=(8, 0.2, segment_length),
                color=color.rgb(30, 30, 35),
                position=(0, -0.1, z_pos)
            )
            self.segments.append(road)

            # Left Skyscraper
            b_left = Entity(
                model='cube',
                scale=(6, 25, segment_length),
                color=color.rgb(50, 60, 80),
                position=(-8, 12.5, z_pos)
            )
            self.buildings_left.append(b_left)

            # Right Skyscraper
            b_right = Entity(
                model='cube',
                scale=(6, 25, segment_length),
                color=color.rgb(50, 60, 80),
                position=(8, 12.5, z_pos)
            )
            self.buildings_right.append(b_right)

    def update_track(self, player_z):
        for i in range(self.pool_size):
            road = self.segments[i]
            b_l = self.buildings_left[i]
            b_r = self.buildings_right[i]

            if road.z < player_z - self.segment_length:
                new_z = road.z + (self.pool_size * self.segment_length)
                road.z = new_z
                b_l.z = new_z
                b_r.z = new_z
                
                # Curving effect using sine wave
                curve_offset = math.sin(new_z * 0.03) * 4.0
                road.x = curve_offset
                b_l.x = curve_offset - 8
                b_r.x = curve_offset + 8

    def set_epoch_theme(self, epoch_id):
        # Change urban aesthetic based on active time era
        if epoch_id == 0:  # Present
            col_road = color.rgb(30, 30, 35)
            col_bldg = color.rgb(50, 60, 80)
        elif epoch_id == 1:  # Past (Industrial Rust & Brick)
            col_road = color.rgb(45, 35, 30)
            col_bldg = color.rgb(90, 50, 40)
        else:  # Future (Cyber Neon Slate)
            col_road = color.rgb(15, 20, 35)
            col_bldg = color.rgb(20, 90, 110)

        for road in self.segments:
            road.color = col_road
        for b in self.buildings_left + self.buildings_right:
            b.color = col_bldg