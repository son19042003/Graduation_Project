import pytest
from selenium.webdriver.common.by import By
from src.testing.pages.selenium.cart_page import CartPage
from src.testing.pages.selenium.login_page import LoginPage
from src.testing.pages.selenium.utils import *
from src.testing.excel_reader import read_test_cases, write_test_result
import logging

logger = logging.getLogger(__name__)

cart_test_cases = [tc for tc in read_test_cases('Demo2') if tc["Loại test case"] == "Chức năng"]

@pytest.fixture(scope="function", autouse=True)
def login_before_cart_test(driver):
    login_page = LoginPage(driver)
    login_page.load()
    safe_type(driver, login_page.email_input(), "tester1@gmail.com")
    safe_type(driver, login_page.password_input(), "123456")
    safe_click(driver, login_page.login_button())
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ec-main-slider"))
    )
    dismiss_password_warning(driver)

@pytest.mark.parametrize('test_case', cart_test_cases)
def test_cart(driver, test_case, caplog):
    with caplog.at_level(logging.INFO):
        row_number = test_case['_row']
        page = CartPage(driver)

        try:
            page.load()
            action_result = page.perform_action(driver, test_case)
            expected = test_case["Kỳ vọng"]
            
            if normalize(expected) in normalize(action_result) or normalize(action_result) in normalize(expected):
                result = "Pass"
                action_result = expected
            else:
                result = "Fail"

            logger.info(f"TC: {test_case.get('ID')} - {test_case.get('Mô tả')}: {action_result} - {result}")

            write_test_result('Demo2', row_number, action_result, result)

        except Exception as e:
            if row_number is not None:
                write_test_result('Demo2', row_number, str(e), 'Fail')
            pytest.fail(f"Lỗi test case: {str(e)}")