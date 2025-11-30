import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from pytest_querys.core.manger import QueryManger
from pytest_querys.querys import ServiceCategory
from pytest_querys.core.registry import service_manger


@service_manger.register(ServiceCategory.WEB.value)
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
