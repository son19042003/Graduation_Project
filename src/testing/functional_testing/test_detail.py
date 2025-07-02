import pytest
from src.testing.excel_reader import read_test_cases, write_test_result
from src.testing.pages.selenium.detail_page import ProductDetailPage
from src.testing.pages.selenium.login_page import LoginPage
from src.testing.pages.selenium.utils import *
import logging

logger = logging.getLogger(__name__)

detail_cases = [tc for tc in read_test_cases("Detail") if tc.get("Loại test case", "") == "Chức năng"]



@pytest.mark.parametrize("test_case", detail_cases)
def test_product_detail_function(driver, test_case, caplog):
    with caplog.at_level(logging.INFO):
        row_number = test_case.get('_row')
        try:
            page = ProductDetailPage(driver)
            data_input = test_case.get('Dữ liệu test') or ''
            email, password, variant, quantity = page.extract_credentials(data_input)

            if "thành công" in test_case.get('Mô tả', '').lower():
                login = LoginPage(driver)
                login.load()
                
                safe_type(driver, login.email_input(), email)
                safe_type(driver, login.password_input(), password)

                safe_click(driver, login.login_button())

                try:
                    dismiss_password_warning(driver)
                except:
                    pass
                
            page.load()
            page.wait_until_loaded()

            expected = test_case.get('Kỳ vọng', '')
            #expected = normalize(expected_raw)
            description = test_case.get('Mô tả', '')

            atc_btn = page.get_add_to_cart_button()
            variant_btn = page.get_variant_button()
            qty_input = page.get_quantity_input()
            stock = page.get_stock_quantity()

            result = 'Fail'
            actual = ''

            if not data_input:
                if "tăng" in expected and page.check_click_plus():
                    result = 'Pass'
                    actual = expected
                elif "giảm" in expected and page.check_click_minus():
                    result = 'Pass'
                    actual = expected
                elif "dưới 1" in expected and not page.check_click_minus_under_1():
                    result = 'Pass'
                    actual = expected
                elif "là 1" in expected and page.check_default_quantity():
                    result = 'Pass'
                    actual = expected
                elif "vượt" in expected:
                    set_quantity(driver, stock + 10)
                    val = int(qty_input.get_attribute("value"))
                    if val <= stock:
                        result = 'Pass'
                        actual = expected
                    else:
                        actual = f"Số lượng hiển thị: {val}"
                elif "phân loại được chọn" in expected.lower() and page.check_click_variant():
                    result = 'Pass'
                    actual = expected
                elif "chưa chọn phân loại" in description.lower():
                    safe_click(driver, atc_btn)
                    msg = page.get_feedback_message()
                    #msg = normalize(msg_raw)
                    if "chọn phân loại" in msg:
                        result = 'Pass'
                        actual = expected
                    else:
                        actual = msg_raw
            else:
                if variant:
                    safe_click(driver, variant_btn)
                if quantity:
                    set_quantity(driver, quantity)

                safe_click(driver, atc_btn)
                msg_raw = page.get_feedback_message()
                msg = normalize(msg_raw)
                if expected in msg or msg in expected:
                    result = 'Pass'
                    actual = expected
                else:
                    actual = msg_raw

            logger.info(f"TC: {test_case.get('ID')} - {test_case.get('Mô tả')}: {actual} - {result}")
            if row_number:
                write_test_result("Detail", row_number, actual, result)

        except Exception as e:
            actual = str(e)
            result = 'Fail'
            logger.info(f"Lỗi test case {test_case.get('ID')}: {actual}")
            if row_number:
                write_test_result("Detail", row_number, actual, result)
            pytest.fail(f"Lỗi test case {test_case.get('ID')}: {actual}")