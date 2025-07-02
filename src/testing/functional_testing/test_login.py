import pytest
from src.testing.excel_reader import read_test_cases, write_test_result
from selenium.webdriver.common.by import By
from src.testing.pages.selenium.login_page import LoginPage
from src.testing.pages.selenium.utils import *
import logging

logger = logging.getLogger(__name__)

func_test_cases = [tc for tc in read_test_cases('Login') if tc["Loại test case"] == "Chức năng"]

@pytest.mark.parametrize('test_case', func_test_cases)
def test_login(driver, test_case, caplog):
    with caplog.at_level(logging.INFO):
        row_number = test_case['_row']
        page = LoginPage(driver)

        try:
            page.load()
            email, password = page.extract_credentials(test_case['Dữ liệu test'])

            safe_type(driver, page.email_input(), email)
            safe_type(driver, page.password_input(), password)
            safe_click(driver, page.login_button())

            msg = page.get_feedback_message()
            msg_normalized = normalize(msg)
            expected = normalize(test_case['Kỳ vọng'])

            if msg_normalized in expected or expected in msg_normalized:
                actual_result = test_case['Kỳ vọng']
                result = 'Pass'
            else:
                actual_result = f'Hiển thị thông báo "{msg}"'
                result = 'Fail'

            logger.info(f"{test_case['ID']} - {test_case['Mô tả']}: {actual_result} - {result}")

            if row_number is not None:
                write_test_result('Login', row_number, actual_result, result)

        except Exception as e:
            if row_number is not None:
                write_test_result('Login', row_number, str(e), 'Fail')
            pytest.fail(f"Lỗi test case: {str(e)}")