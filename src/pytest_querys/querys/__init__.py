from enum import Enum, unique

from pytest_querys.core.category import ServiceCategoryManager


@unique
class ServiceCategory(Enum):
    REDIS = "redis_server"
    WEB = "web_server"
    POSTGRES = "postgres_server"


ServiceCategoryManager.register_enum(ServiceCategory)
