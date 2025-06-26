from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.testing.pages.selenium.utils import safe_click
import re

class ProductDetailPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost/ecommerce/product/street-life-mens-frayed-hem-denim-shorts-with-pockets-65f99c45d0916-105"

    def load(self):
        self.driver.get(self.url)

    def wait_until_loaded(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.qty-input")))

    def get_quantity_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, "input.qty-input")

    def get_add_to_cart_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "button#add-Product-To-Cart")

    def get_variant_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".ec-pro-variation-content li")

    def get_stock_quantity(self):
        return int(self.driver.find_element(By.CSS_SELECTOR, "#product-stock").text)

    def get_feedback_message(self):
        try:
            toast = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".swal2-title"))
            )
            return toast.text
        except:
            return 'Không tìm thấy thông báo nào'

    def check_click_plus(self):
        plus = self.driver.find_element(By.CSS_SELECTOR, ".dec.ec_qtybtn")
        qty = self.get_quantity_input()
        before = int(qty.get_property("value"))
        safe_click(self.driver, plus)
        after = int(qty.get_property("value"))
        return after == before + 1

    def check_click_minus(self):
        minus = self.driver.find_element(By.CSS_SELECTOR, ".inc.ec_qtybtn")
        qty = self.get_quantity_input()
        qty.clear()
        qty.send_keys('2')
        before = int(qty.get_property("value"))
        safe_click(self.driver, minus)
        after = int(qty.get_property("value"))
        return after == before - 1
    
    def check_click_minus_under_1(self):
        minus = self.driver.find_element(By.CSS_SELECTOR, ".inc.ec_qtybtn")
        qty = self.get_quantity_input()
        before = int(qty.get_property("value"))
        safe_click(self.driver, minus)
        after = int(qty.get_property("value"))
        return after == before - 1

    def check_default_quantity(self):
        return int(self.get_quantity_input().get_attribute("value")) == 1

    def check_click_variant(self):
        variant = self.get_variant_button()
        safe_click(self.driver, variant)
        return "active" in variant.get_attribute("class")

    @staticmethod
    def extract_credentials(data):
        if not data:
            return '', '', '', ''
        email_match = re.search(r"Email:\s*([^,]+)", data)
        password_match = re.search(r"Password:\s*([^,]+)", data)
        variant_match = re.search(r"Chọn phân loại:\s*([^,]+)", data)
        quantity_match = re.search(r"Số lượng:\s*([^,]+)", data)
        return (
            email_match.group(1).strip() if email_match else '',
            password_match.group(1).strip() if password_match else '',
            variant_match.group(1).strip() if variant_match else '',
            quantity_match.group(1).strip() if quantity_match else ''
        )