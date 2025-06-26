import pytest
from src.testing.excel_reader import read_test_cases, write_test_result
from src.testing.pages.selenium.search_page import SearchPage

search_cases = [tc for tc in read_test_cases("Search") if tc["Loại test case"] == "Chức năng"]

@pytest.mark.parametrize("test_case", search_cases)
def test_search(driver, test_case):
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

        if page.is_numeric(keyword) and (product_exist or load_more):
            actual = "Cho phép tìm kiếm với ký tự số"
            result = "Pass"
        elif page.is_special_character(keyword) and (product_exist or load_more):
            actual = "Cho phép tìm kiếm với ký tự đặc biệt"
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

        print(f"TC: {test_case['ID']} - {test_case['Mô tả']}: {actual} - {result}")
        if row_number:
            write_test_result("Search", row_number, actual, result)

    except Exception as e:
        pytest.fail(f"Lỗi test case {test_case['ID']}: {str(e)}")