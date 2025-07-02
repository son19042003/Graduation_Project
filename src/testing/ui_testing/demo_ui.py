import pytest
from playwright.sync_api import sync_playwright
from src.testing.excel_reader import read_test_cases, write_test_result
from ui_test_handlers import UI_TEST_HANDLERS
import re
import logging

def normalize_text(text):
    text = text.strip()
    text = text.lower()
    text = text.replace("'", "").replace('"', "")
    text = re.sub(r"[.,!?;:]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def run_test_case_ui(page, test_case):
    desc = test_case["Mô tả"].lower()
    expected = normalize_text(test_case["Kỳ vọng"].strip('" '))

    for pattern, handler in UI_TEST_HANDLERS:
        if re.search(pattern, desc):
            actual_raw = handler(page, test_case)
            actual = normalize_text(actual_raw)
                
            if expected in actual or actual in expected:
                result = "Pass"
                actual = expected
            else:
                result = "Fail"
            return actual, result
    return "Không hỗ trợ mô tả", "Skip"

logger = logging.getLogger(__name__)

ui_test_cases = [tc for tc in read_test_cases('Demo') if tc["Loại test case"] == "UI"]
@pytest.mark.parametrize("test_case", ui_test_cases)
def test_ui_login(test_case, caplog):
    with caplog.at_level(logging.INFO):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto('http://localhost/ecommerce')
            
            actual, result = run_test_case_ui(page, test_case)
            logger.info(f"{test_case['ID']} - {test_case['Mô tả']}: {actual} - {result}")

            write_test_result(
                sheet_name="Demo",
                row_number=test_case["_row"],
                actual=actual,
                result=result
            )

            browser.close()