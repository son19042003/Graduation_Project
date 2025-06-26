import pytest
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.testing.excel_reader import read_test_cases, write_test_result
from unidecode import unidecode

def get_dynamic_message(driver):
    try:
        toast = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".swal2-title"))
        )
        return toast.text
    except:
        return 'Không tìm thấy thông báo nào'
    
detail_cases = [tc for tc in read_test_cases("Test") if tc.get("Loại test case", "") == "Chức năng"]

@pytest.mark.parametrize("test_case", detail_cases)
def test_product_detail_function(driver, test_case):
    row_number = test_case.get('_row')
    try:
        driver.get("http://localhost/ecommerce/product/street-life-mens-frayed-hem-denim-shorts-with-pockets-65f99c45d0916-105")

        atc_btn = driver.find_element(By.CSS_SELECTOR, "button#add-Product-To-Cart")
        container = driver.find_element(By.CLASS_NAME, "ec-single-qty")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        atc_btn.click()
        msg = get_dynamic_message(driver)
        print(f"Thông báo: {msg}")

    except Exception as e:
        actual = str(e)
        result = 'Fail'
        print(f"Lỗi test case {test_case.get('ID')}: {actual}")
        pytest.fail(f"Lỗi test case {test_case.get('ID')}: {actual}")