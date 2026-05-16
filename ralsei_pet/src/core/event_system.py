class EventSystem:
    def __init__(self):
        # 事件监听器字典，键为事件名称，值为回调函数列表
        self._listeners = {}
    
    def on(self, event_name, callback):
        """注册事件监听器"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)
    
    def off(self, event_name, callback):
        """移除事件监听器"""
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
            except ValueError:
                pass
    
    def emit(self, event_name, *args, **kwargs):
        """触发事件"""
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    from .logger import logger
                    logger.error(f"事件处理错误 [{event_name}]: {e}")
    
    def clear(self, event_name=None):
        """清空事件监听器"""
        if event_name:
            if event_name in self._listeners:
                del self._listeners[event_name]
        else:
            self._listeners.clear()

# 创建全局事件系统实例
event_system = EventSystem()
