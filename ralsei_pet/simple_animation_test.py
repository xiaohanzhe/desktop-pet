#!/usr/bin/env python3
# 简单测试动画切换修复
import time

class MockRalseiPet:
    def __init__(self):
        self.current_animation = "idle"
        self.last_animation_change = time.time() - 1.0  # 初始化为1秒前
        self.animation_change_cooldown = 0.8  # 0.8秒冷却时间
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
            "land": 3,
            "sing": 3
        }
        self.current_priority = self.animation_priorities.get(self.current_animation, 1)
    
    def change_animation(self, new_animation, force=False):
        # 模拟动画切换逻辑
        current_time = time.time()
        
        # 检查是否是不同分组的动画切换
        current_group = self.current_animation.split('_')[0] if '_' in self.current_animation else self.current_animation
        new_group = new_animation.split('_')[0] if '_' in new_animation else new_animation
        
        # 检查冷却时间和优先级
        if not force:
            # 不同分组的动画切换需要更长的冷却时间
            if current_group != new_group:
                if current_time - self.last_animation_change < self.animation_change_cooldown * 2:
                    return False
            else:
                if current_time - self.last_animation_change < self.animation_change_cooldown:
                    return False
        
        # 执行动画切换
        self.current_animation = new_animation
        self.current_priority = self.animation_priorities.get(new_animation, 1)
        self.last_animation_change = current_time
        return True

class AnimationTest:
    def __init__(self):
        self.ralsei = MockRalseiPet()
        self.animation_changes = []
        self.last_animation = self.ralsei.current_animation
        self.last_change_time = time.time()
    
    def test_animation_switching(self):
        print("开始测试动画切换...")
        
        # 模拟不同状态下的动画切换
        test_states = [
            ("idle", "正常状态"),
            ("walk_down", "行走状态"),
            ("jump", "跳跃状态"),
            ("laugh", "大笑状态"),
            ("sing", "唱歌状态"),
            ("idle", "回到正常状态")
        ]
        
        for animation, state in test_states:
            print(f"\n测试切换到 {state} ({animation})")
            result = self.ralsei.change_animation(animation)
            print(f"切换结果: {result}")
            
            # 记录动画变化
            current_time = time.time()
            if self.last_animation != self.ralsei.current_animation:
                time_diff = current_time - self.last_change_time
                self.animation_changes.append((self.last_animation, self.ralsei.current_animation, time_diff))
                print(f"从 {self.last_animation} 切换到 {self.ralsei.current_animation}，时间间隔: {time_diff:.3f}秒")
                self.last_animation = self.ralsei.current_animation
                self.last_change_time = current_time
            
            # 等待一段时间
            time.sleep(0.5)
        
        # 打印测试结果
        print("\n测试结果总结:")
        print(f"动画切换次数: {len(self.animation_changes)}")
        for i, (from_anim, to_anim, time_diff) in enumerate(self.animation_changes):
            print(f"{i+1}. 从 {from_anim} 到 {to_anim}: {time_diff:.3f}秒")
        
        # 检查是否有快速切换
        fast_switches = [change for change in self.animation_changes if change[2] < 0.5]
        if fast_switches:
            print(f"\n发现 {len(fast_switches)} 次快速切换（小于0.5秒）:")
            for from_anim, to_anim, time_diff in fast_switches:
                print(f"  - {from_anim} -> {to_anim}: {time_diff:.3f}秒")
        else:
            print("\n没有发现快速切换，动画切换正常。")
        
        # 测试快速切换不同分组的动画
        print("\n测试快速切换不同分组的动画...")
        self.ralsei.last_animation_change = time.time() - 2.0  # 重置冷却时间
        self.animation_changes = []
        self.last_animation = self.ralsei.current_animation
        self.last_change_time = time.time()
        
        # 快速切换不同分组的动画
        quick_changes = ["idle", "walk_down", "laugh", "jump", "sing", "idle"]
        for animation in quick_changes:
            result = self.ralsei.change_animation(animation)
            print(f"从 {self.ralsei.current_animation} 到 {animation}: {result}")
            
            # 记录动画变化
            current_time = time.time()
            if self.last_animation != self.ralsei.current_animation:
                time_diff = current_time - self.last_change_time
                self.animation_changes.append((self.last_animation, self.ralsei.current_animation, time_diff))
                self.last_animation = self.ralsei.current_animation
                self.last_change_time = current_time
        
        # 打印快速切换测试结果
        print("\n快速切换测试结果:")
        print(f"尝试切换次数: {len(quick_changes)}")
        print(f"成功切换次数: {len(self.animation_changes)}")
        for i, (from_anim, to_anim, time_diff) in enumerate(self.animation_changes):
            print(f"{i+1}. 从 {from_anim} 到 {to_anim}: {time_diff:.3f}秒")

if __name__ == "__main__":
    test = AnimationTest()
    test.test_animation_switching()
