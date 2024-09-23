import pytest
import logging

pytest_plugins = ["fixture_sessions"]


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")
    logging.info("parser")


@pytest.fixture(scope="session")
def env(request):
    e = request.config.getoption("--env", default="dev")
    logging.info(f"env : {e}")
    return e
