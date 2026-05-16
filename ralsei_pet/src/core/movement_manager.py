import time
import math
from PyQt5.QtCore import QPoint

class MovementManager:
    def __init__(self):
        self.target_pos = QPoint(100, 100)
        self.speed = 10.0
        self.min_speed = 8.0
        self.max_speed = 15.0
        self.mass = 30.0
        self.gravity = 500.0
        self.friction = 0.95
        self.air_resistance = 0.985
        self.bounce_coefficient = 0.2
        self.smoothness_factor = 0.1
        self.current_speed_x = 0
        self.current_speed_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.is_moving = True
        self.idle_timer = 0
        self.moving_duration = 0
        self.is_falling = False
        self.is_recovering = False
        self.fall_start_time = None
        self.recovery_start_time = None
        self.max_idle_duration = 0
        self.max_moving_duration = 0
        self.last_update_time = time.time()
        self.current_direction = "down"
        self.previous_direction = "down"
        self.swing_speed = 0.01
        self.direction_change_smoothness = 0.5
        self.speed_fluctuation = 0.0
        self.fluctuation_speed = 0.01
        self.stride_fluctuation = 0.0
        self.stride_variation = 1.0
        self.speed_variation = 1.0
        self.movement_noise = 0.0
        self.noise_change_rate = 0.005
        self.is_jumping = False
        self.jump_height = 50
        self.jump_duration = 1.0
        self.jump_start_time = 0
        self.jump_start_pos = QPoint(0, 0)
        self.jump_target_pos = QPoint(0, 0)
        self.jump_target_window = None
        self.jump_count = 0
        self.max_jumps = 3
        self.jump_cooldown = 2.0
        self.last_jump_time = 0
        self.resting_time = 0
        self.needs_rest = False
        self.stamina = 100.0
        self.stamina_regen_rate = 5.0
        self.jump_stamina_cost = 20.0
        self.is_following_mouse = False
        self.mouse_follow_speed = 5
        self.mouse_follow_distance = 50
        self._last_mouse_pos = None
        self.rest_duration = 5.0
        self.is_sleeping = False
        self.sleep_timer = 0
        self.max_sleep_idle_duration = 300
        self.last_interaction_time = time.time()
        self.fall_duration = 0.0
        self.max_fall_duration = 5.0
        self.recovery_duration = 0.0
        self.recovery_max_duration = 5.0
        self.has_ball = False
        self.is_holding_cotton_candy = False
        self.is_wearing_suit = False
        self.is_using_item = False
        self.is_spellcasting = False
        self.is_laughing = False
        self.is_rolling = False
        self.is_sliding = False
        self.is_teasplashed = False
        self.is_victorious = False
        self.is_surprised = False
        self.is_happy = False
        self.is_shy = False
        self.is_unhappy = False
        self.is_sleeping_walk = False
        self.surprised_timer = 0
        self.happy_timer = 0
        self.shy_timer = 0
        self.unhappy_timer = 0
        self.idle_walk_timer = 0
        self.current_window = None
        self.window_level = 0
        self.last_window_check_time = 0
        self.window_check_interval = 2.0
        self.last_window_rect = None
        self.ralsei_window_relative_pos = QPoint(0, 0)
        self.is_gravity_falling = False
        self.fall_speed = 0.0
        self.spatial_pos = {"x": 0, "y": 0, "z": 0}
        self.current_platform_z = 0
        self.current_floor = None
        self.last_floor_check_time = 0
        self.floor_check_interval = 1.0
        self.current_time = time.strftime("%H:%M:%S")
        self.time_of_day = "morning"
        self.weather = "sunny"
        self.temperature = 22.0
        self.humidity = 50.0
        self.emotions = {
            "happiness": 50.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "boredom": 0.0,
            "tiredness": 0.0,
            "excitement": 0.0
        }
        self.mood = "normal"
        self.last_mood_change = time.time()
        self.is_watching_video = False
        self.video_start_time = 0
        self.video_duration = 0
        self.current_video_url = ""
        self.video_platform = ""
        self.video_title = ""
        self.video_watch_history = []
        self.video_preferences = ["游戏", "动画", "音乐", "科普", "搞笑", "Deltarune", "Undertale"]
        self.current_activity = "idle"
        self.activity_history = []
        self.dragged_file = None
        self.is_following_dragged_file = False
    
    def update_movement(self, elapsed_time, screen_geometry):
        current_time = time.time()
        
        if self.is_jumping:
            self._handle_jump(elapsed_time, current_time)
            return
        elif self.is_gravity_falling:
            self._handle_gravity_fall(elapsed_time, current_time)
            return
        elif self.is_falling:
            self._handle_fall(elapsed_time, current_time)
            return
        elif self.is_recovering:
            self._handle_recovery(elapsed_time, current_time)
            return
        elif self.is_following_mouse:
            self._handle_mouse_follow(elapsed_time)
            return
        elif self.is_following_dragged_file:
            self._handle_dragged_file_follow(elapsed_time)
            return
        
        if self.is_moving:
            self._update_normal_movement(elapsed_time, screen_geometry)
        else:
            self._update_idle_state(elapsed_time)
    
    def _update_normal_movement(self, elapsed_time, screen_geometry):
        current_pos = self.pos()
        dx = self.target_pos.x() - current_pos.x()
        dy = self.target_pos.y() - current_pos.y()
        distance_sq = dx * dx + dy * dy
        distance = math.sqrt(distance_sq) if distance_sq > 0 else 0
        
        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance
            
            if distance_sq > 10000:
                target_move_speed = self.speed * 1.0
            elif distance_sq < 2500:
                target_move_speed = self.speed * (distance / 50)
            else:
                target_move_speed = self.speed * 0.8
            
            current_speed = math.hypot(self.current_speed_x, self.current_speed_y)
            new_speed = current_speed + (target_move_speed - current_speed) * 0.5
            
            max_move_distance = self.speed * 1.0
            base_move_distance = new_speed * elapsed_time
            move_distance = min(distance, base_move_distance, max_move_distance)
            
            new_x = current_pos.x() + direction_x * move_distance
            new_y = current_pos.y() + direction_y * move_distance
            new_x = int(round(new_x))
            new_y = int(round(new_y))
            
            new_x = max(0, min(new_x, screen_geometry.width() - self.width()))
            new_y = max(0, min(new_y, screen_geometry.height() - self.height()))
            
            actual_dx = new_x - current_pos.x()
            actual_dy = new_y - current_pos.y()
            actual_distance = math.hypot(actual_dx, actual_dy) if actual_dx != 0 or actual_dy != 0 else 1.0
            
            if actual_distance > 0:
                self.current_speed_x = (actual_dx / actual_distance) * new_speed
                self.current_speed_y = (actual_dy / actual_distance) * new_speed
            
            self.move(new_x, new_y)
            
            speed_magnitude = math.hypot(self.current_speed_x, self.current_speed_y)
            if speed_magnitude > 1.0:
                angle = math.atan2(self.current_speed_y, self.current_speed_x) * 180 / math.pi
                if -30 <= angle < 30:
                    new_dir = "right"
                elif 60 <= angle < 120:
                    new_dir = "down"
                elif -120 <= angle < -60:
                    new_dir = "up"
                else:
                    new_dir = "left"
                
                if self.current_direction != new_dir:
                    self.current_direction = new_dir
        
        if distance_sq <= (self.speed * 2) ** 2:
            self.is_moving = False
            self.idle_timer = 0
            self.max_idle_duration = random.uniform(2.0, 5.0)
            self.last_movement_end_time = current_time
            self.current_speed_x = 0
            self.current_speed_y = 0
    
    def _update_idle_state(self, elapsed_time):
        self.idle_timer += elapsed_time
        if self.idle_timer >= self.max_idle_duration:
            if random.random() < 0.7:
                self.randomize_movement_pattern()
                self.is_moving = True
                self.moving_duration = 0
            else:
                self.max_idle_duration = random.uniform(3.0, 6.0)
    
    def randomize_movement_pattern(self):
        self.last_start_pos = self.pos()
        current_time = time.time()
        
        if hasattr(self, 'last_movement_end_time'):
            time_since_last_move = current_time - self.last_movement_end_time
            move_probability = 0.4
            
            if random.random() < move_probability or time_since_last_move < 1.0:
                self.is_moving = True
            else:
                self.max_idle_duration = random.uniform(6.0, 15.0)
                self.is_moving = False
        else:
            if random.random() < 0.3:
                self.is_moving = True
            else:
                self.is_moving = False
                self.max_idle_duration = random.uniform(6.0, 15.0)
    
    def generate_new_move_target(self, screen_geometry):
        self.max_moving_duration = random.uniform(3.0, 10.0)
        self.speed = random.uniform(self.min_speed * 0.4, self.max_speed * 0.6)
        
        sprite_size = 100
        current_pos = self.pos()
        
        if hasattr(self, 'previous_direction'):
            if random.random() < 0.99:
                direction = self.previous_direction
            else:
                direction = random.choice(['up', 'down', 'left', 'right'])
        else:
            direction = random.choice(['up', 'down', 'left', 'right'])
        
        if random.random() < 0.6:
            if direction in ['up', 'down']:
                direction = random.choice(['left', 'right'])
        
        move_distance = random.randint(80, 250)
        
        if direction == 'up':
            target_x = current_pos.x() + random.randint(-40, 40)
            target_y = max(50, current_pos.y() - move_distance)
        elif direction == 'down':
            target_x = current_pos.x() + random.randint(-40, 40)
            target_y = min(screen_geometry.height() - sprite_size, current_pos.y() + move_distance)
        elif direction == 'left':
            target_x = max(50, current_pos.x() - move_distance)
            target_y = current_pos.y() + random.randint(-40, 40)
        else:
            target_x = min(screen_geometry.width() - sprite_size, current_pos.x() + move_distance)
            target_y = current_pos.y() + random.randint(-40, 40)
        
        self.previous_direction = direction
        
        final_offset_x = random.randint(-10, 10)
        final_offset_y = random.randint(-10, 10)
        
        target_x += final_offset_x
        target_y += final_offset_y
        
        target_x = max(50, min(target_x, screen_geometry.width() - sprite_size))
        target_y = max(50, min(target_y, screen_geometry.height() - sprite_size))
        
        self.target_pos = QPoint(target_x, target_y)
        self.is_moving = True
        self.moving_duration = 0
    
    def _handle_jump(self, elapsed_time, current_time):
        pass
    
    def _handle_gravity_fall(self, elapsed_time, current_time):
        pass
    
    def _handle_fall(self, elapsed_time, current_time):
        pass
    
    def _handle_recovery(self, elapsed_time, current_time):
        pass
    
    def _handle_mouse_follow(self, elapsed_time):
        pass
    
    def _handle_dragged_file_follow(self, elapsed_time):
        pass