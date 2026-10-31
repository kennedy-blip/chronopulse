# src/entities/player.py
from ursina import Entity, color, held_keys, time, Vec3
import math

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale = (1, 2, 1)
        self.origin_y = -0.5

        # --- Detailed Humanoid Articulated Structure ---
        # Head & Cybernetic Visor
        self.head = Entity(parent=self, model='sphere', color=color.rgb(240, 200, 170), scale=(0.4, 0.4, 0.4), y=1.5, z=0.0)
        self.visor = Entity(parent=self, model='cube', color=color.cyan, scale=(0.42, 0.12, 0.22), y=1.55, z=-0.08)

        # Torso & Tactical Jacket Armor
        self.torso = Entity(parent=self, model='cube', color=color.rgb(40, 45, 60), scale=(0.65, 0.9, 0.35), y=0.9)
        self.jacket_accent = Entity(parent=self, model='cube', color=color.magenta, scale=(0.67, 0.4, 0.37), y=0.95, z=0.02)

        # Glowing Quantum Data-Core Backpack
        self.backpack = Entity(parent=self, model='cube', color=color.cyan, scale=(0.4, 0.5, 0.25), y=0.9, z=0.25)

        # Articulated Limbs (Arms & Legs for running stride animation)
        self.left_arm = Entity(parent=self, model='cube', color=color.rgb(40, 45, 60), scale=(0.18, 0.7, 0.18), position=(-0.45, 1.1, 0))
        self.right_arm = Entity(parent=self, model='cube', color=color.rgb(40, 45, 60), scale=(0.18, 0.7, 0.18), position=(0.45, 1.1, 0))

        self.left_leg = Entity(parent=self, model='cube', color=color.rgb(25, 25, 30), scale=(0.22, 0.8, 0.22), position=(-0.18, 0.4, 0))
        self.right_leg = Entity(parent=self, model='cube', color=color.rgb(25, 25, 30), scale=(0.22, 0.8, 0.22), position=(0.18, 0.4, 0))

        # Movement & Physics
        self.lane = 0  # -1: Left, 0: Center, 1: Right
        self.target_x = 0
        self.speed = 18.0
        
        # Jump physics
        self.is_jumping = False
        self.jump_velocity = 0.0
        self.gravity = -35.0
        self.ground_y = 0.0
        self.anim_timer = 0.0

    def update(self):
        # Lane switching via Arrow Keys or A/D
        if held_keys['a'] or held_keys['left arrow']:
            self.lane = max(-1, self.lane - 1)
        if held_keys['d'] or held_keys['right arrow']:
            self.lane = min(1, self.lane + 1)

        self.target_x = self.lane * 2.5
        self.x = lerp(self.x, self.target_x, time.dt * 15)
        self.z += self.speed * time.dt

        # Procedural running animation cycle (swinging limbs)
        if not self.is_jumping:
            self.anim_timer += time.dt * self.speed * 0.8
            stride = math.sin(self.anim_timer) * 35.0
            self.left_arm.rotation_x = stride
            self.right_arm.rotation_x = -stride
            self.left_leg.rotation_x = -stride
            self.right_leg.rotation_x = stride
        else:
            # Tuck limbs during jump
            self.left_arm.rotation_x = -20
            self.right_arm.rotation_x = -20
            self.left_leg.rotation_x = 20
            self.right_leg.rotation_x = 20

        # Jump handling (Spacebar)
        if (held_keys['space'] or held_keys['w'] or held_keys['up arrow']) and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = 12.0

        if self.is_jumping:
            self.y += self.jump_velocity * time.dt
            self.jump_velocity += self.gravity * time.dt
            if self.y <= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.jump_velocity = 0.0

def lerp(a, b, t):
    return a + (b - a) * t