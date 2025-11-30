from enum import Enum, unique
from typing import Type, List, Optional


class CategoryManager:
    _registered_enums: List[Type[Enum]] = []
    _value_map = None
    _name_set = set()
    _value_set = set()

    @classmethod
    def register_enum(cls, enum_cls: Type[Enum]):
        """注册新的枚举类"""
        if enum_cls in cls._registered_enums:
            return

        # 检查冲突
        for member in enum_cls:
            if member.name in cls._name_set:
                raise ValueError(f"枚举成员 name 冲突: '{member.name}'")
            if member.value in cls._value_set:
                raise ValueError(f"枚举成员 value 冲突: '{member.value}'")

        # 通过检查后注册
        cls._registered_enums.append(enum_cls)
        for member in enum_cls:
            cls._name_set.add(member.name)
            cls._value_set.add(member.value)

        # 清空缓存，下次从_string查找时重建
        cls._value_map = None

    @classmethod
    def get_all_types(cls) -> List[str]:
        """返回所有服务值"""
        return list(cls._value_set)

    @classmethod
    def get_all_members(cls) -> List[Enum]:
        """返回所有枚举成员"""
        result = []
        for enum_cls in cls._registered_enums:
            result.extend(list(enum_cls))
        return result

    @classmethod
    def from_string(cls, value: str) -> Optional[Enum]:
        """根据字符串查找对应枚举成员，忽略大小写"""
        if cls._value_map is None:
            cls._value_map = {}
            for enum_cls in cls._registered_enums:
                for member in enum_cls:
                    cls._value_map[member.value.lower()] = member
        return cls._value_map.get(value.lower().strip())

    @classmethod
    def is_valid_type(cls, service_type: str) -> bool:
        return cls.from_string(service_type) is not None


class ServiceCategoryManager(CategoryManager):
    pass
