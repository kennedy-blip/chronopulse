# src/engine/game.py
from ursina import Ursina, window, camera, color, Text, time, DirectionalLight, AmbientLight, Sky, Vec3
from src.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.entities.player import Player
from src.entities.obstacle import Obstacle
from src.systems.track_gen import TrackGenerator
from src.systems.adrenaline import AdrenalineSystem
from src.systems.time_shift import TimeShiftSystem
from src.engine.physics import check_collision
from src.database.db_manager import init_db, save_run, get_high_score

class ChronoGameManager:
    def __init__(self):
        self.app = Ursina()
        window.title = WINDOW_TITLE
        window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        window.borderless = False
        window.color = color.rgb(20, 24, 33)
        
        init_db()
        
        # Initialize Game Systems & Entities
        self.player = Player(position=(0, 0, 0))
        self.track_gen = TrackGenerator()
        self.adrenaline = AdrenalineSystem()
        self.time_system = TimeShiftSystem()
        
        # Proper Camera Parenting & Lighting for Visual Depth
        camera.parent = self.player
        camera.position = (0, 4.5, -12)
        camera.rotation = (18, 0, 0)
        
        self.dir_light = DirectionalLight(y=20, z=-20, shadows=True)
        self.dir_light.look_at(self.player)
        self.amb_light = AmbientLight(color=color.rgb(100, 100, 110))
        self.sky = Sky(color=color.rgb(30, 35, 45))

        # HUD Overlays
        self.score_text = Text(text="Score: 0", position=(-0.85, 0.45), scale=1.5, color=color.white)
        self.adrenaline_text = Text(text="Adrenaline: 0%", position=(-0.85, 0.40), scale=1.2, color=color.cyan)
        self.epoch_text = Text(text="Epoch: PRESENT", position=(-0.85, 0.35), scale=1.2, color=color.yellow)
        self.controls_text = Text(text="Controls: [A / D] or [Left / Right Arrows] to Switch Lanes | [Space] to Jump", position=(-0.85, -0.45), scale=0.9, color=color.light_gray)
        
        self.obstacles = []
        self.next_obstacle_z = 30.0
        self.score = 0
        self.is_game_over = False

    def update(self):
        if self.is_game_over:
            return

        self.track_gen.update_track(self.player.z)
        self.adrenaline.update(time.dt, is_running_fast=True)
        
        self.score = int(self.player.z)
        self.score_text.text = f"Score: {self.score}"
        self.adrenaline_text.text = f"Adrenaline: {int(self.adrenaline.value)}%"
        
        # Spawn obstacles ahead
        if self.player.z + 80 > self.next_obstacle_z:
            obs = Obstacle(z_pos=self.next_obstacle_z)
            self.obstacles.append(obs)
            self.next_obstacle_z += 25.0

        # Collision check
        for obs in self.obstacles:
            if check_collision(self.player, obs):
                self.trigger_game_over()
                break

        # Cleanup passed obstacles
        self.obstacles = [o for o in self.obstacles if o.z > self.player.z - 10]

        # Overdrive time shift trigger
        if self.adrenaline.is_overdrive:
            new_epoch = self.time_system.cycle()
            epochs = ["PRESENT", "PAST (Industrial)", "FUTURE (Cyber)"]
            self.epoch_text.text = f"Epoch: {epochs[new_epoch]}"
            self.track_gen.set_epoch_theme(new_epoch)
            self.adrenaline.value = 0.0

    def trigger_game_over(self):
        self.is_game_over = True
        self.player.speed = 0
        save_log_score = self.score
        save_run(save_log_score, self.time_system.current_epoch)
        high = get_high_score()
        
        Text(text="CRITICAL COLLISION - RUN TERMINATED", position=(-0.35, 0.1), scale=1.8, color=color.red)
        Text(text=f"Final Score: {save_log_score} | High Score: {high}", position=(-0.3, 0.0), scale=1.3, color=color.white)
        Text(text="Restart game via terminal (python main.py)", position=(-0.3, -0.1), scale=1.1, color=color.orange)

    def run(self):
        global update_hook
        update_hook = self.update
        self.app.run()

update_hook = lambda: None
def update():
    update_hook()