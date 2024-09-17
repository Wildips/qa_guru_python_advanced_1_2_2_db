import pytest

from service_tests.config import Server
from service_tests.utils.base_session import BaseSession


@pytest.fixture(scope='session')
def reqresin(env):
    with BaseSession(base_url=Server(env).reqres) as session:
        yield session
