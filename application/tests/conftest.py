import eventlet
eventlet.monkey_patch()

import pytest
from nameko.containers import ServiceContainer


def pytest_addoption(parser):
    parser.addoption('--test-db-url', action='store', dest='TEST_DB_URL')


@pytest.fixture
def db_url(request):
    return request.config.getoption("TEST_DB_URL")


@pytest.yield_fixture
def container_factory():

    all_containers = []

    def make_container(service_cls, config, worker_ctx_cls=None):
        container = ServiceContainer(service_cls, config, worker_ctx_cls)
        all_containers.append(container)
        return container

    yield make_container

    for c in all_containers:
        try:
            c.stop()
        except:
            pass
