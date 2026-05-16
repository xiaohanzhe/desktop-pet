import math
import random

class AnimationSystem:
    def __init__(self, pet):
        self.pet = pet
        self.current_animation = "idle"
        self.next_animation = None
        self.current_frame = 0
        self.animation_change_cooldown = 0.8
        self.last_animation_change = 0
        self.animation_fps = 6
        self.animation_frame_delay = int(1000 / self.animation_fps)
        self.current_offset = (0, 0)
        self._last_animation_time_ms = 0
        
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
    
    def update_animation(self, current_time_ms, elapsed_ms):
        """更新动画帧"""
        # 计算基础延迟
        base_delay_ms = 1000.0 / self.animation_fps
        
        # 根据拖拽速度调整动画帧率
        if hasattr(self.pet, '_is_being_dragged') and self.pet._is_being_dragged and hasattr(self.pet, '_drag_speed'):
            drag_delay_ms = base_delay_ms * (1.0 - min(0.8, self.pet._drag_speed / 200.0))
        else:
            drag_delay_ms = base_delay_ms
        
        # 检查是否达到了播放下一帧的时间
        if not self._last_animation_time_ms:
            self._last_animation_time_ms = current_time_ms
            return
        
        if elapsed_ms < drag_delay_ms:
            return
        
        # 计算应该跳过的帧数（补帧/丢帧机制）
        frames_to_advance = int(elapsed_ms / drag_delay_ms)
        if frames_to_advance < 1:
            frames_to_advance = 1
        
        # 确定当前应该播放的动画
        new_animation = self._determine_animation()
        
        # 低概率触发被踩动作
        if random.random() < 0.01 and not self.pet.is_moving and not self.pet.is_jumping and not self.pet.is_falling:
            self.pet.is_splat = True
            self.pet.splat_start_time = current_time_ms / 1000.0
            new_animation = "splat"
        
        # 检查被踩状态是否应该结束
        if hasattr(self.pet, 'is_splat') and self.pet.is_splat:
            if not hasattr(self.pet, 'splat_start_time'):
                self.pet.splat_start_time = current_time_ms / 1000.0
            if (current_time_ms / 1000.0) - self.pet.splat_start_time >= 10.0:
                self.pet.is_splat = False
                self.pet.splat_start_time = None
        
        # 平滑切换动画
        self._handle_animation_switch(new_animation)
        
        # 更新动画帧
        self._update_animation_frame(frames_to_advance)
        
        # 更新状态计时器
        self._update_state_timers(elapsed_ms)
        
        # 更新最后动画时间
        self._last_animation_time_ms = current_time_ms
    
    def _determine_animation(self):
        """确定当前应该播放的动画"""
        if self.pet.is_jumping:
            if not hasattr(self.pet, 'jump_phase'):
                self.pet.jump_phase = "ready"
            if self.pet.jump_phase == "ready":
                self.pet.jump_phase = "jumping"
                return "jump_ready"
            elif self.pet.jump_phase == "jumping":
                if self.pet.has_ball:
                    return "jump_ball"
                else:
                    return "jump"
            else:
                self.pet.jump_phase = None
                return "land"
        elif self.pet.is_falling:
            if not hasattr(self.pet, 'fall_start_time') or self.pet.fall_start_time is None:
                self.pet.fall_start_time = time.time()
            if self.pet.fall_start_time is not None and time.time() - self.pet.fall_start_time >= 1.0:
                self.pet.is_falling = False
                self.pet.is_recovering = True
                self.pet.recovery_start_time = time.time()
            return "fall_back"
        elif self.pet.is_recovering:
            if not hasattr(self.pet, 'recovery_start_time') or self.pet.recovery_start_time is None:
                self.pet.recovery_start_time = time.time()
            if self.pet.recovery_start_time is not None and time.time() - self.pet.recovery_start_time >= 2.0:
                self.pet.is_recovering = False
                self.pet.fall_start_time = None
                self.pet.recovery_start_time = None
            return "idle"
        elif self.pet.is_using_item:
            return "item"
        elif self.pet.is_spellcasting:
            return "spell"
        elif self.pet.is_laughing:
            return "laugh"
        elif self.pet.is_rolling:
            return "roll"
        elif self.pet.is_sliding:
            return "slide"
        elif self.pet.is_teasplashed:
            return "tea"
        elif self.pet.is_victorious:
            return "victory"
        elif self.pet.is_moving:
            return self._get_movement_animation()
        else:
            return self._get_idle_animation()
    
    def _get_movement_animation(self):
        """获取移动动画"""
        speed_sq = self.pet.current_speed_x * self.pet.current_speed_x + self.pet.current_speed_y * self.pet.current_speed_y
        speed_threshold = (self.pet.speed * 1.5) ** 2
        
        if speed_sq > speed_threshold:
            base_animation = "run"
        else:
            base_animation = "walk"
        
        # 根据情绪和状态决定动画变化
        if self.pet.is_wearing_suit:
            animation_suffix = f"_butler"
            if self.pet.is_unhappy:
                animation_suffix = f"_butler_unhappy"
        elif self.pet.is_holding_cotton_candy:
            animation_suffix = "_cotton_candy"
        elif self.pet.is_shy:
            animation_suffix = "_blush"
        elif self.pet.is_unhappy:
            animation_suffix = "_unhappy"
        elif self.pet.is_sleeping_walk:
            animation_suffix = "_sleep"
        else:
            animation_suffix = ""
        
        return f"{base_animation}_{self.pet.current_direction}{animation_suffix}"
    
    def _get_idle_animation(self):
        """获取空闲动画"""
        if self.pet.idle_timer >= 180.0:
            return "idle"
        elif self.pet.is_happy:
            return "laugh"
        elif self.pet.is_surprised:
            return "surprised"
        elif self.pet.is_shy:
            return "smile_left" if self.pet.current_direction == "left" else "smile_right"
        elif hasattr(self.pet, 'is_waving') and self.pet.is_waving:
            return self._handle_wave_animation()
        elif hasattr(self.pet, 'is_being_thrown') and self.pet.is_being_thrown:
            return "hatless_throw"
        else:
            return "idle"
    
    def _handle_wave_animation(self):
        """处理挥手动画"""
        if not hasattr(self.pet, 'wave_phase') or self.pet.wave_phase == "start":
            self.pet.wave_phase = "waving"
            self.pet.wave_start_time = time.time()
            return "wave_start"
        elif self.pet.wave_phase == "waving":
            if time.time() - self.pet.wave_start_time >= 2.0:
                self.pet.wave_phase = "end"
            return "wave_down"
        else:
            if time.time() - self.pet.wave_start_time >= 3.0:
                self.pet.is_waving = False
                self.pet.wave_phase = None
                self.pet.wave_start_time = None
            return "wave_start"
    
    def _handle_animation_switch(self, new_animation):
        """处理动画切换"""
        if self.current_animation != new_animation:
            if new_animation is None:
                new_animation = 'idle'
            
            if new_animation not in self.pet.sprite_loader.sprites:
                base_anim = 'idle'
                if len(new_animation.split('_')) >= 2:
                    base_anim = new_animation.split('_')[0] + '_' + new_animation.split('_')[1]
                    if base_anim not in self.pet.sprite_loader.sprites:
                        base_anim = 'idle'
                new_animation = base_anim
            
            is_same_category = False
            if self.current_animation and new_animation:
                current_is_movement = self.current_animation.startswith('walk_') or self.current_animation.startswith('run_')
                new_is_movement = new_animation.startswith('walk_') or new_animation.startswith('run_')
                
                if current_is_movement and new_is_movement:
                    is_same_category = True
                current_parts = self.current_animation.split('_')
                new_parts = new_animation.split('_')
                if len(current_parts) >= 2 and len(new_parts) >= 2:
                    if current_parts[0] == new_parts[0] and current_parts[0] in ['walk', 'run', 'idle', 'laugh', 'sing', 'pose']:
                        is_same_category = True
            
            if is_same_category:
                if self.pet.change_animation(new_animation, force=True):
                    self.current_frame = 0
            else:
                if random.random() < 0.3:
                    if self.pet.change_animation(new_animation, force=False):
                        self.current_frame = 0
    
    def _update_animation_frame(self, frames_to_advance):
        """更新动画帧"""
        if self.pet.is_moving or self.pet.is_jumping or self.pet.is_falling or self.pet.is_recovering:
            frames = self.pet.sprite_loader.sprites.get(self.current_animation, [])
            frame_count = len(frames)
            
            if frame_count > 0:
                self.current_frame = self.current_frame % frame_count
                sprite = frames[self.current_frame]
                if sprite:
                    self._update_sprite_display(sprite)
                
                self.current_frame += frames_to_advance
        else:
            if not hasattr(self.pet, '_last_idle_frame') or self.pet._last_idle_frame != 1:
                frames = self.pet.sprite_loader.sprites.get(self.current_animation, [])
                frame_count = len(frames)
                if frame_count > 0:
                    self.current_frame = min(1, frame_count - 1)
                    sprite = frames[self.current_frame]
                    if sprite:
                        self._update_sprite_display(sprite)
                self.pet._last_idle_frame = 1
    
    def _update_sprite_display(self, sprite):
        """更新精灵显示"""
        scale_factor = getattr(self.pet, '_cached_scale_factor', 2.0)
        target_width = int(sprite.width() * scale_factor)
        target_height = int(sprite.height() * scale_factor)
        
        if self.pet.width() != target_width or self.pet.height() != target_height:
            old_pos = self.pet.pos()
            old_center_x = old_pos.x() + self.pet.width() // 2
            old_center_y = old_pos.y() + self.pet.height() // 2
            
            new_x = old_center_x - target_width // 2
            new_y = old_center_y - target_height