import catalogue
import os
from functools import wraps

'''
代办：1、处理manger类的条件管理，manger必须是基于QueryManger的才允许注册
'''

def make_registry_conditional(registry):
    """只对特定注册表实例应用条件补丁"""

    original_register = registry.register

    def conditional_register(name_or_func=None, condition=None):
        """条件注册方法"""

        def actual_decorator(obj):
            should_register = True

            if condition is not None:
                should_register = condition()
            else:
                auto_condition = getattr(obj, '_register_condition', None)
                if auto_condition is not None:
                    should_register = auto_condition()

            if should_register:
                if isinstance(name_or_func, str):
                    return original_register(name_or_func)(obj)
                else:
                    registry_name = getattr(obj, '_registry_name', obj.__name__.lower())
                    return original_register(registry_name)(obj)
            else:
                return obj

        # 处理不同的调用方式
        if callable(name_or_func):
            # @registry.register
            return actual_decorator(name_or_func)
        else:
            # @registry.register("name") 或 @registry.register(condition=...)
            return actual_decorator

    registry.register = conditional_register
    return registry


service_manger = catalogue.create("services", "manger")
service_query = catalogue.create("services", "query")
service_session = catalogue.create("services", "session")

# make_registry_conditional(service_manger)
#
#
# # 这个注册表支持条件注册
# @service_manger.register(condition=lambda: os.getenv("ENV") == "production")
# class ProductionService:
#     pass
#
#
# @service_manger.register("email")
# class EmailService:
#     _register_condition = lambda: os.getenv("ENABLE_EMAIL") == "true"
#
#
# # 这个注册表保持原始行为
# @normal_registry.register("logger")
# class LoggerService:
#     pass  # 始终注册


