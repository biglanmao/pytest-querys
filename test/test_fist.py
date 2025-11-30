from pytest_querys.querys import ServiceCategory


def test_get_manger(service_mangers):
    web_manger = service_mangers(ServiceCategory.WEB.value)
    baidu_session = web_manger.get_session("baidu")
    print(baidu_session)