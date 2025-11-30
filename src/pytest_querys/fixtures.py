#
# 1、获取所有的管理器
# 2、获取querys和session
import os
import pytest as pytest
import yaml

from pytest_querys.core.inventory import ServicesInventory
from pytest_querys.core.registry import service_manger, service_query, service_session


@pytest.fixture(scope="session")
def services_inventory(request):
    file_path = request.config.getini("service_inventory")
    file_path = os.path.join(request.config.getoption("rootdir"), file_path)
    print("cfg_file_path", file_path)
    if not os.path.exists(file_path):
        inventory = None
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
            inventory = ServicesInventory(cfg)
    return inventory


@pytest.fixture(scope="session")
def service_mangers(services_inventory):
    def get_query_manger(name):
        return service_manger.get(name)(services_inventory)

    return get_query_manger


@pytest.fixture(scope="session")
def service_querys(services_inventory):
    def get_query_manger(name):
        return service_query.get(name)(services_inventory)

    return get_query_manger


@pytest.fixture(scope="session")
def service_sessions(services_inventory):
    def get_query_manger(name):
        return service_session.get(name)(services_inventory)

    return get_query_manger
