# 状态机类，用于管理角色动作状态
class PetStateMachine:
    def __init__(self):
        # 定义状态枚举
        self.states = {
            'IDLE': 'idle',
            'WALKING': 'walking',
            'RUNNING': 'running',
            'JUMPING': 'jumping',
            'FALLING': 'falling',
            'RECOVERING': 'recovering',
            'SLEEPING': 'sleeping',
            'LAUGHING': 'laughing',
            'SURPRISED': 'surprised',
            'SHY': 'shy',
            'UNHAPPY': 'unhappy',
            'USING_ITEM': 'using_item',
            'SPELLCASTING': 'spellcasting',
            'ROLLING': 'rolling',
            'SLIDING': 'sliding',
            'TEASPLASHED': 'teasplashed',
            'VICTORIOUS': 'victorious'
        }
        
        # 初始状态
        self.current_state = self.states['IDLE']
        
        # 状态转换表
        self.transitions = {
            'IDLE': ['WALKING', 'RUNNING', 'JUMPING', 'SLEEPING', 'LAUGHING', 'SURPRISED', 'SHY', 'UNHAPPY', 'USING_ITEM', 'SPELLCASTING', 'ROLLING', 'SLIDING', 'TEASPLASHED', 'VICTORIOUS'],
            'WALKING': ['IDLE', 'RUNNING', 'JUMPING', 'FALLING', 'SURPRISED', 'SHY'],
            'RUNNING': ['IDLE', 'WALKING', 'JUMPING', 'FALLING', 'SURPRISED', 'SHY'],
            'JUMPING': ['IDLE', 'WALKING', 'RUNNING', 'FALLING'],
            'FALLING': ['RECOVERING'],
            'RECOVERING': ['IDLE', 'WALKING', 'RUNNING'],
            'SLEEPING': ['IDLE', 'WALKING', 'RUNNING', 'SURPRISED'],
            'LAUGHING': ['IDLE', 'WALKING', 'RUNNING'],
            'SURPRISED': ['IDLE', 'WALKING', 'RUNNING'],
            'SHY': ['IDLE', 'WALKING', 'RUNNING'],
            'UNHAPPY': ['IDLE', 'WALKING', 'RUNNING'],
            'USING_ITEM': ['IDLE', 'WALKING', 'RUNNING'],
            'SPELLCASTING': ['IDLE', 'WALKING', 'RUNNING'],
            'ROLLING': ['IDLE', 'WALKING', 'RUNNING'],
            'SLIDING': ['IDLE', 'WALKING', 'RUNNING'],
            'TEASPLASHED': ['IDLE', 'WALKING', 'RUNNING'],
            'VICTORIOUS': ['IDLE', 'WALKING', 'RUNNING']
        }
        
    def set_state(self, new_state):
        """设置新状态"""
        if new_state in self.states.values() and new_state in self.transitions.get(self.current_state, []):
            self.current_state = new_state
            return True
        return False
    
    def get_state(self):
        """获取当前状态"""
        return self.current_state
    
    def is_state(self, state):
        """检查是否为指定状态"""
        return self.current_state == state