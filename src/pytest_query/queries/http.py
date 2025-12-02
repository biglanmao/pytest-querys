from functools import singledispatchmethod

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from pytest_query.core.manger import QueryManger
from pytest_query.queries import ServiceCategory


class HttpQueryManger(QueryManger):
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

    @singledispatchmethod
    def get_session(self, name):
        raise NotImplementedError("Unsupported types")

    @get_session.register
    def get_session_from_name(self, name: str):
        session = requests.Session()
        service_config = self.inventory.get_query_config(self.SERVICE_CATEGORY, name)
        self._configure_session(session, service_config)
        return session

    @get_session.register
    def get_session_from_config(self, config: dict):
        session = requests.Session()
        self._configure_session(session, config)
        return session

    def get_query(self, name, inventory=None):
        pass

    def get_uri_prefix(self, config):
        address = config["address"]
        port = config["port"]
        protocol = "https" if config.get("tls", False) else "http"
        uri_prefix = f'{protocol}://{address}:{port}/'
        return uri_prefix
