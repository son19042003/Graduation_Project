import pytest
from src.testing.excel_reader import read_test_cases, write_test_result
from src.testing.pages.selenium.search_page import SearchPage
import logging

logger = logging.getLogger(__name__)

demo_cases = [tc for tc in read_test_cases("Demo") if tc["Loại test case"] == "Chức năng"]

@pytest.mark.parametrize("test_case", demo_cases)
def test_search(driver, test_case, caplog):
    with caplog.at_level(logging.INFO):
        row_number = test_case['_row']
        page = SearchPage(driver)

        try:
            page.load()
            keyword = page.extract_keyword(test_case['Dữ liệu test'])
            desc = test_case["Mô tả"].lower()
            expected = test_case["Kỳ vọng"]

            search_input = page.enter_keyword(keyword)
            if "nhấn enter" in desc:
                page.press_enter(search_input)
            else:
                page.click_search()

            page.wait_for_load()

            product_names = page.get_product_names()
            product_exist = page.has_products()
            load_more = page.has_load_more_button()

            result = 'Fail'
            actual = ''

            keyword = page.extract_keyword(test_case['Dữ liệu test'])
            print(f"[DEBUG] Keyword: '{keyword}'")
            print(f"[DEBUG] is_special_character: {page.is_special_character(keyword)}")
            print(f"[DEBUG] is_numeric: {page.is_numeric(keyword)}")
            print(f"[DEBUG] is_whitespace: {page.is_whitespace(keyword)}")
            if page.is_numeric(keyword):
                if product_exist or load_more:
                    actual = "Hệ thống cho phép tìm kiếm với ký tự số, có kết quả trả về"
                else:
                    actual = "Hệ thống xử lý từ khóa số nhưng không tìm thấy sản phẩm"
                result = "Pass"
            elif page.is_special_character(keyword):
                if product_exist or load_more:
                    actual = "Hệ thống cho phép tìm kiếm với ký tự đặc biệt, có kết quả trả về"
                else:
                    actual = "Hệ thống xử lý từ khóa đặc biệt nhưng không tìm thấy sản phẩm"
                result = "Pass"
            elif page.is_whitespace(keyword):
                if product_exist:
                    actual = expected
                    result = "Pass"
                else:
                    actual = "Không hiển thị sản phẩm"
                    result = "Fail"
            else:
                if product_exist:
                    if page.all_products_match_keyword(product_names, keyword):
                        actual = expected
                        result = "Pass"
                    else:
                        actual = "Vẫn tìm được sản phẩm"
                else:
                    actual = "Không tìm được sản phẩm"
                    if ("không hiển thị" in expected.lower() or "không tìm thấy" in expected.lower()):
                        result = "Pass"

            logger.info(f"TC: {test_case['ID']} - {test_case['Mô tả']}: {actual} - {result}")
            if row_number:
                write_test_result("Demo", row_number, actual, result)

        except Exception as e:
            pytest.fail(f"Lỗi test case {test_case['ID']}: {str(e)}")