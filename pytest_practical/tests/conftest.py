"""
This is the configuration file for Pytest solution and it contains
different runtime parameters.

We can also define universal fixtures which can be used across project.
"""
import pytest
import logging
import os
from datetime import datetime
from py.xml import html
from pytest_practical.data_providers import logger_util

logger = logging.getLogger("root")

root_dir = os.getcwd()
os.chdir(root_dir)
main_project_dir = os.getcwd()


@pytest.yield_fixture(scope="class")
def setup(request, env, log_level):
    """

    This function is used as a fixture to set the value for log_level, and env.

    in pytest 2.4 and above, we yield is used instead of return statement
    to provide a fixture value while otherwise fully supporting all other fixture features.
    :param request:
    :param env:
    :param log_level:
    :return:

    """
    global logger

    logger = logger_util.log_message(log_level, "root")

    test_data_dir = main_project_dir + '\\testdata'
    directory = test_data_dir + '\\' + env

    if request.cls is not None:
        request.cls.directory = directory

    yield directory


def pytest_addoption(parser):
    """
    This function is used to add various parameters which is used for test execution.
    :param parser:
    :return:
    """
    parser.addoption("--log_level", help="Set the level of logging", default="INFO")
    parser.addoption("--env", help="Choose environment 'dev/qa/stage'", default="qa")


@pytest.fixture(scope="session")
def log_level(request):
    """
    Fixture to set the value for log_level.
    :param request:
    :return:
    """
    return request.config.getoption("--log_level")


@pytest.fixture(scope="session")
def env(request):
    """
    Fixture to set the value for env.

    :param request:
    :return:
    """
    return request.config.getoption("--env")


def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.now(), class_='col-time'))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
