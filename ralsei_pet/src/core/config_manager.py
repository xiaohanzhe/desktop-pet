import json
import os
import time
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file=None):
        # 默认配置文件路径
        if config_file is None:
            config_file = Path(__file__).parent.parent.parent / "config.json"
        self.config_file = Path(config_file)
        
        # 加载默认配置
        self.default_config = self._load_default_config()
        
        # 加载用户配置
        self.user_config = self._load_user_config()
        
        # 合并配置
        self.config = self._merge_configs(self.default_config, self.user_config)
        
        # 保存时间记录
        self.last_save_time = time.time()
        self.save_interval = 300  # 5分钟自动保存
    
    def _load_default_config(self):
        """加载默认配置"""
        return {
            "animation": {
                "fps": 6,
                "frame_delay": 166,  # 约6FPS
                "change_cooldown": 0.8
            },
            "movement": {
                "speed": 10.0,
                "min_speed": 8.0,
                "max_speed": 15.0,
                "mass": 30.0,
                "gravity": 500.0,
                "friction": 0.95,
                "air_resistance": 0.985,
                "bounce_coefficient": 0.2,
                "smoothness_factor": 0.1
            },
            "behavior": {
                "max_idle_duration": 15.0,
                "max_moving_duration": 10.0,
                "max_sleep_idle_duration": 300.0,  # 5分钟
                "jump_cooldown": 2.0,
                "max_jumps": 3,
                "stamina_regen_rate": 5.0,
                "jump_stamina_cost": 20.0
            },
            "ui": {
                "window_width": 100,
                "window_height": 100,
                "init_x_offset": 50,
                "init_y_offset": 50
            },
            "api": {
                "enabled": False,
                "api_key": "",
                "endpoint": ""
            },
            "logging": {
                "level": "INFO",
                "file": "pet.log"
            }
        }
    
    def _load_user_config(self):
        """加载用户配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _merge_configs(self, default, user):
        """合并配置"""
        if not isinstance(user, dict):
            return default
        
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config()
    
    def get_api_config(self):
        """获取API配置"""
        return self.config.get("api", {})
    
    def _save_config(self):
        """保存配置到文件"""
        current_time = time.time()
        if current_time - self.last_save_time >= self.save_interval:
            try:
                # 确保目录存在
                self.config_file.parent.mkdir(exist_ok=True)
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                
                self.last_save_time = current_time
            except Exception:
                pass
    
    def reload(self):
        """重新加载配置"""
        self.user_config = self._load_user_config()
        self.config = self._merge_configs(self.default_config, self.user_config)
