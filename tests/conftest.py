import pytest
from selenium import webdriver
import time
driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")      ## decorator to create fixture and can be used on class level
def setup(request):     ## request is predefined object, which will be auto populated by pytest
    global driver
    browser_name=request.config.getoption("browser_name")   #pytest --browser_name "firefox"

     # parameter which can be passed with pytest command
    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "IE":
        print("IE driver")
    else:
        driver = webdriver.Chrome()

    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()

    request.cls.driver = driver         ## request => to class which is using fixture
    '''
        request is a parameter in fixture.. cls is property in request which will be auto populated with the class name whoever using fixture
        we are injecting driver into base class so that base class can use self.driver and its childs as well
        you can just change driver to myDriver or something but in base class you need to use self.myDriver or self.something
    '''
    yield
    driver.close()


# This hook is used to take automatically screenshot and place in HTML report
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    global driver
    driver.get_screenshot_as_file(name)

