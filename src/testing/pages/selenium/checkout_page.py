from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
from .utils import *

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost/ecommerce/checkout"

    def load(self):
        self.driver.get(self.url)

    def fill_fullname(self, value):
        el = self.driver.find_element(By.NAME, "fullname")
        safe_type(self.driver, el, value)

    def fill_phone(self, value):
        el = self.driver.find_element(By.NAME, "phone")
        safe_type(self.driver, el, value)

    def fill_address(self, value):
        el = self.driver.find_element(By.NAME, "address")
        el.clear()
        el.send_keys(value)

    def select_payment_method(self, method_text):
        method_text = method_text.strip().lower()
        if "vnpay" in method_text:
            el = self.driver.find_element(By.CSS_SELECTOR, 'label[for="vnpay"]')
        elif "momo" in method_text:
            el = self.driver.find_element(By.CSS_SELECTOR, 'label[for="momo"]')
        else:
            el = self.driver.find_element(By.CSS_SELECTOR, 'label[for="cash_on_delivery"]')
        safe_click(self.driver, el)

    def click_order_button(self):
        el = self.driver.find_element(By.CSS_SELECTOR, ".ec-check-order-btn button[type='submit']")
        safe_click(self.driver, el)
        
    def get_feedback_message(self):
        try:
            toast = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "swal2-toast"))
            )
            return toast.text.strip()
        except:
            try:
                title = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "swal2-title"))
                )
                return title.text.strip()
            except:
                return "Không tìm thấy thông báo nào"

        
    @staticmethod
    def extract_checkout_fields(data):
        fullname_match = re.search(r"Họ và tên\s*:\s*([^,]+)", data, re.IGNORECASE)
        phone_match = re.search(r"Số điện thoại\s*:\s*([^,]+)", data, re.IGNORECASE)
        address_match = re.search(r"Địa\s*(?:chỉ|chi)?\s*:\s*([^,]+)", data, re.IGNORECASE)
        payment_match = re.search(r"Phương thức thanh toán\s*:\s*([^,]+)", data, re.IGNORECASE)

        fullname = fullname_match.group(1).strip() if fullname_match else ''
        phone = phone_match.group(1).strip() if phone_match else ''
        address = address_match.group(1).strip() if address_match else ''
        payment_method = payment_match.group(1).strip() if payment_match else ''

        return fullname, phone, address, payment_method

    def perform_action(self, driver, test_case):
        self.load()

        data = (test_case.get("Dữ liệu test") or "").lower()
        expected = (test_case.get("Kỳ vọng") or "").lower()

        fullname, phone, address, payment_method = self.extract_checkout_fields(data)
        print(f"[Extracted] fullname: {fullname}, phone: {phone}, address: {address}, payment: {payment_method}")

        self.fill_fullname(fullname)
        self.fill_phone(phone)
        self.fill_address(address)
        self.select_payment_method(payment_method)

        self.click_order_button()
        msg = self.get_feedback_message()

        WebDriverWait(driver, 3).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        current_url = driver.current_url.lower()

        if any(k in expected for k in ["thành công", "lỗi", "thông báo"]):
            if normalize(msg) in normalize(expected) or normalize(expected) in normalize(msg):
                return expected
            return msg
        else:
            if 'vnpay' in current_url:
                return 'Chuyển hướng đến trang thanh toán VNPAY'
            elif 'momo' in current_url:
                return 'Chuyển hướng đến trang thanh toán MOMO'
            return msg