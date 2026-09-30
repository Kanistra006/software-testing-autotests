"""Общие фикстуры pytest: стенд, браузер, скриншот при падении теста."""
import os
from pathlib import Path

import pytest

from driver_factory import create_chrome
from stand_server import run_stand

ARTIFACTS = Path(__file__).parent / "artifacts"


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="запускать Chrome без окна")


@pytest.fixture(scope="session")
def base_url():
    """Стенд поднимается один раз на весь прогон."""
    with run_stand() as url:
        yield url


@pytest.fixture
def driver(request):
    """Новый браузер на каждый тест — тесты не зависят друг от друга."""
    headless = request.config.getoption("--headless") or os.getenv("HEADLESS") == "1"
    drv = create_chrome(headless=headless)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Если тест упал, сохранить скриншот страницы в artifacts/."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "driver" in item.fixturenames:
        ARTIFACTS.mkdir(exist_ok=True)
        item.funcargs["driver"].save_screenshot(str(ARTIFACTS / f"FAILED_{item.name}.png"))
