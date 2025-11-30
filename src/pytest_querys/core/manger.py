import importlib
import pkgutil
from abc import abstractmethod


class QueryManger:
    SERVICE_CATEGORY = None

    class Meta(type):
        def __init__(cls, name, bases, attrs):
            if 'SERVICE_CATEGORY' not in attrs or attrs['SERVICE_CATEGORY'] is None:
                raise NotImplementedError(f"{name} 必须定义 SERVICE_CATEGORY 类属性")

            super().__init__(name, bases, attrs)

    def __init__(self, inventory):
        self.inventory = inventory

    @abstractmethod
    def get_session(self, name):
        pass

    @abstractmethod
    def get_query(self, name):
        pass

    def get_service_config(self, name, category=None):
        category = category or self.SERVICE_CATEGORY
        return self.inventory.get_service_config(category, name)
