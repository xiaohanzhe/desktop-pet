import time
import statistics

# 添加性能监控功能
class PerformanceMonitor:
    def __init__(self):
        self.function_times = {}
        self.start_time = time.time()
        
    def record_time(self, function_name, execution_time):
        """记录函数执行时间"""
        if function_name not in self.function_times:
            self.function_times[function_name] = []
        self.function_times[function_name].append(execution_time)
        
    def get_stats(self):
        """获取性能统计信息"""
        stats = {}
        for function_name, times in self.function_times.items():
            if times:
                stats[function_name] = {
                    'count': len(times),
                    'avg': statistics.mean(times) * 1000,  # 转换为毫秒
                    'min': min(times) * 1000,
                    'max': max(times) * 1000
                }
        return stats
    
    def print_stats(self):
        """打印性能统计信息"""
        pass

# 创建全局性能监控实例
perf_monitor = PerformanceMonitor()

# 性能监控装饰器
def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        perf_monitor.record_time(func.__name__, execution_time)
        return result
    return wrapper