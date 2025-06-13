import pytest
from selenium.webdriver.common.by import By
from excel_reader import read_test_cases, write_test_result
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_credentials(data):
    email_match = re.search(r"Email:\s*([\w\.-]+@[\w\.-]+)", data)
    password_match = re.search(r"Mật khẩu:\s*(.+)", data)

    email = email_match.group(1) if email_match else ''
    password = password_match.group(1) if password_match else ''
    return email.strip(), password.strip()

def get_dynamic_error_message(driver):
    try:
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'swal2-toast-shown swal2-shown'))
        )
        return error_element.text
    except:
        return 'Không tìm thấy thông báo lỗi'

@pytest.mark.parametrize('test_case', read_test_cases('Login'))
def test_login(driver, test_case):
    driver.get('http://localhost/ecommerce/login')
    row_number = test_case['_row']
    try:
        email_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.CLASS_NAME, 'btn btn-primary rounded-1')

        if test_case['Loại test case'] == 'UI':
            element = driver.find_element(By.XPATH, test_case['Mô tả'])
            actual = element.text if element else 'Không tìm thấy phần tử'
            result = 'Pass' if actual == test_case['Kỳ vọng'] else 'Fail'
        elif test_case['Loại test case'] == 'Chức năng':
            email, password = extract_credentials(test_case['Dữ liệu test'])
            email_input.send_keys(email)
            password_input.send_keys(password)
            login_button.click()

            expected_result = test_case['Kỳ vọng']
            actual_result = get_dynamic_error_message(driver) or driver.current_url
            result = 'Pass' if actual_result == expected_result else 'Fail'
        else:
            actual_result, result = 'Không xác định', 'Fail'
        
        write_test_result('Login', row_number, actual_result, result)

    except Exception as e:
        write_test_result('Login', row_number, str(e), 'Fail')
        pytest.fail(f"Lỗi test case: {str(e)}")
