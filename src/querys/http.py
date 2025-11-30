from enum import unique, Enum

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from src.manger import QueryManger
from src.category import ServiceCategoryManager

from src.registry import service_manger

'''
# 最终将这个类放在entry point让从这个注册。
# 这样其他的注册到entry point也可以直接注册。

'''


@unique
class ServiceCategory(Enum):
    REDIS = "redis_server"
    WEB = "web_server"
    POSTGRES = "postgres_server"


ServiceCategoryManager.register_enum(ServiceCategory)


@service_manger.register(ServiceCategory.WEB.value)
class WebQueryManger(QueryManger):
    '''
        创建和管理全局的web资源对象。
        1、完成web资源的初始化和资源获取。
        2、返回一个获取资源的函数，然后可以传递参数来获取需要的资源。直接传递资源的名称即可。返回一个web_session。
        3、最终返回的是request 。session对象
        4、seesion自己支持上下文管理则不用实现上下文管理，直接返回session。
        方法设计，设计一个seesion的管理的夹具。然后按照给定的服务器名称创建初始化对应的session对象，进行会话的初始化后进行返回。然后在夹具中对seesion进行上下文管理
    '''
    SERVICE_CATEGORY = ServiceCategory.WEB

    def _configure_session(self, session, config):
        retry = Retry(
            total=3,
            backoff_factor=config.get("retry_num", 3),
            status_forcelist=config.get("retry_code", [500, 502, 503, 504])
        )
        adapter = HTTPAdapter(max_retries=retry)

        if config.get("tls", False):
            session.mount("https://", adapter)
        else:
            session.mount("http://", adapter)

        session.headers.update(config.get("header", {}))

        if not config.get("cert_verify", True):
            session.verify = False

    def get_session(self, name):
        session = requests.Session()
        service_config = self.inventory.get_service_config(self.SERVICE_CATEGORY, name)
        self._configure_session(session, service_config)
        return session

    def get_query(self, name):
        pass

    def get_uri_prefix(self, config):
        address = config["address"]
        port = config["port"]
        protocol = "https" if config.get("tls", False) else "http"
        uri_prefix = f'{protocol}://{address}:{port}/'
        return uri_prefix
