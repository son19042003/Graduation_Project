import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import io
import sys
from pytest_html import extras

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-features=AutofillServerCommunication,AutofillKeyPressHandling,PasswordCheck,AutofillCredManBackend,OptimizationGuideModelDownloading,PasswordImport")
    options.add_argument("--password-store=basic")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 2,
        "profile.default_content_setting_values.automatic_downloads": 1,
    })
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        caplog = item.funcargs.get("caplog", None)
        if caplog:
            log_text = "\n".join(record.message for record in caplog.records)
            if log_text:
                report.extras = getattr(report, "extras", [])
                report.extras.append(extras.text(log_text))