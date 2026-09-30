"""Общие фикстуры pytest: стенд, браузер, Page Object, скриншот при падении."""
import os
from pathlib import Path

import pytest

from driver_factory import create_chrome
from pages.contact_page import ContactPage
from stand_server import run_stand

ARTIFACTS = Path(__file__).parent / "artifacts"


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="запускать Chrome без окна")


def _headless(config) -> bool:
    return config.getoption("--headless") or os.getenv("HEADLESS") == "1"


@pytest.fixture(scope="session")
def base_url():
    with run_stand() as url:
        yield url


@pytest.fixture
def driver(request):
    """Новый браузер на каждый тест."""
    drv = create_chrome(headless=_headless(request.config))
    yield drv
    drv.quit()


@pytest.fixture
def contact_page(driver, base_url) -> ContactPage:
    """Открытая форма обратной связи."""
    return ContactPage(driver, base_url).open()


@pytest.fixture(scope="module")
def shared_driver(request):
    """Один браузер на модуль — для массового прогона матрицы решений (96 комбинаций)."""
    drv = create_chrome(headless=_headless(request.config))
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Если тест упал, сохранить скриншот страницы в artifacts/."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver") or item.funcargs.get("shared_driver")
        if drv:
            ARTIFACTS.mkdir(exist_ok=True)
            drv.save_screenshot(str(ARTIFACTS / f"FAILED_{item.name}.png"))
