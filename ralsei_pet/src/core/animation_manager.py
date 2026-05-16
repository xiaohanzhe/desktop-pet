import time
import random
from PyQt5.QtCore import QElapsedTimer

class AnimationManager:
    def __init__(self, sprite_loader):
        self.sprite_loader = sprite_loader
        self.current_animation = "idle"
        self.next_animation = None
        self.current_frame = 0
        self.animation_change_cooldown = 0.8
        self.last_animation_change = time.time() - self.animation_change_cooldown
        self.animation_fps = 6
        self.animation_frame_delay = int(1000 / self.animation_fps)
        self.current_offset = (0, 0)
        self._last_animation_time_ms = 0
        
        # 动画优先级系统
        self.animation_priorities = {
            "idle": 1,
            "walk_down": 2,
            "walk_left": 2,
            "walk_right": 2,
            "walk_up": 2,
            "run_down": 2,
            "run_left": 2,
            "run_right": 2,
            "run_up": 2,
            "laugh": 3,
            "jump": 3,
            "fall": 3,
            "spell": 3,
            "tea": 3,
            "victory": 3,
            "wave": 3,
            "wave_start": 3,
            "dance": 3,
            "cry": 3,
            "hug": 3,
            "roll": 3,
            "slide": 3,
            "act": 3,
            "attack": 3,
            "battleintro": 3,
            "cotton_talk": 3,
            "cower": 3,
            "curtsy": 3,
            "defend": 3,
            "hug_stop": 3,
            "kneel_cry": 3,
            "kneel_serious": 3,
            "look_up": 3,
            "nuzzle": 3,
            "pose": 3,
            "sing": 3,
            "surprised": 3,
            "wave_down": 3
        }
        
        self.current_priority = self.animation_priorities.get(self.current_animation, 1)
        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()
    
    def update_animation(self, pet_state, is_moving, is_jumping, is_falling, is_recovering, current_direction, has_ball, is_wearing_suit, is_holding_cotton_candy, is_shy, is_unhappy, is_sleeping_walk, is_surprised):
        current_time_ms = self.elapsed_timer.elapsed()
        current_time = current_time_ms / 1000.0
        
        base_delay_ms = 1000.0 / self.animation_fps
        drag_delay_ms = base_delay_ms
        
        if not self._last_animation_time_ms:
            self._last_animation_time_ms = current_time_ms
            return None
        
        elapsed_ms = current_time_ms - self._last_animation_time_ms
        if elapsed_ms < drag_delay_ms:
            return None
        
        frames_to_advance = int(elapsed_ms / drag_delay_ms)
        if frames_to_advance < 1:
            frames_to_advance = 1
        
        new_animation = None
        
        if is_jumping:
            if not hasattr(self, 'jump_phase'):
                self.jump_phase = "ready"
            if self.jump_phase == "ready":
                new_animation = "jump_ready"
                self.jump_phase = "jumping"
            elif self.jump_phase == "jumping":
                if has_ball:
                    new_animation = "jump_ball"
                else:
                    new_animation = "jump"
            else:
                new_animation = "land"
                self.jump_phase = None
        elif is_falling:
            new_animation = "fall_back"
        elif is_recovering:
            pass
        elif is_moving:
            speed_sq = 0  # 需要从外部传入
            speed_threshold = 0  # 需要从外部传入
            
            if speed_sq > speed_threshold:
                base_animation = "run"
            else:
                base_animation = "walk"
            
            if is_wearing_suit:
                animation_suffix = f"_butler"
                if is_unhappy:
                    animation_suffix = f"_butler_unhappy"
            elif is_holding_cotton_candy:
                animation_suffix = "_cotton_candy"
            elif is_shy:
                animation_suffix = "_blush"
            elif is_unhappy:
                animation_suffix = "_unhappy"
            elif is_sleeping_walk:
                animation_suffix = "_sleep"
            else:
                animation_suffix = ""
            
            new_animation = f"{base_animation}_{current_direction}{animation_suffix}"
        else:
            new_animation = "idle"
        
        self._last_animation_time_ms = current_time_ms
        return new_animation, frames_to_advance