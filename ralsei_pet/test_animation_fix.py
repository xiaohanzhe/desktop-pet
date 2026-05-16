#!/usr/bin/env python3
# 测试动画切换修复
import time
import os
import sys

# 添加项目根目录到sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.main import RalseiPet
from PyQt5.QtWidgets import QApplication

class AnimationTest:
    def __init__(self):
        self.app = QApplication([])
        self.ralsei = RalseiPet()
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
            time.sleep(1)
        
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
        
        # 测试跳跃动作衔接
        print("\n测试跳跃动作衔接...")
        self.ralsei.start_jump(None, "down")
        time.sleep(2)  # 等待跳跃完成
        print("跳跃测试完成。")
        
        self.app.quit()

if __name__ == "__main__":
    test = AnimationTest()
    test.test_animation_switching()
