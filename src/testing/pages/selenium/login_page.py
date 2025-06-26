from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost/ecommerce/login"

    def load(self):
        self.driver.get(self.url)

    def email_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, "input[name='email']")

    def password_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")

    def login_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.rounded-1")

    def get_feedback_message(self):
        try:
            modal = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-modal"))
            )
            return modal.text.splitlines()[0]
        except:
            pass
        try:
            toast = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".swal2-title"))
            )
            return toast.text
        except:
            return "Không tìm thấy thông báo nào"

    @staticmethod
    def extract_credentials(data):
        email_match = re.search(r"Email:\s*([^,]+)", data)
        password_match = re.search(r"Mật khẩu:\s*(.+)", data)
        email = email_match.group(1) if email_match else ''
        password = password_match.group(1) if password_match else ''
        return email.strip(), password.strip()