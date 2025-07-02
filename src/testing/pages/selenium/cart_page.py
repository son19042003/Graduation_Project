from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from src.testing.pages.selenium.utils import safe_click, extract_number, normalize

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost/ecommerce/cart"

    def load(self):
        self.driver.get(self.url)

    def get_cart_rows(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "#cart_main tr")

    def get_quantity_input(self, row):
        return row.find_element(By.CSS_SELECTOR, "input.cart-plus-minus")
    
    def get_quantity(self, row):
        input_element = self.get_quantity_input(row)
        value = input_element.get_attribute("value")
        try:
            return int(value.strip()) if value else 1
        except:
            return 1
    
    def get_price(self, row):
        price = row.find_element(By.CSS_SELECTOR, ".ec-cart-pro-price .amount").text
        return extract_number(price)

    def get_row_total(self, row):
        try:
            text = row.find_element(By.CSS_SELECTOR, ".ec-cart-pro-subtotal").text
            return extract_number(text)
        except:
            return 0

    def get_cart_total(self):
        try:
            text = self.driver.find_element(By.ID, "order-total-amount").text
            return extract_number(text)
        except:
            return 0

    def click_checkout(self):
        element = self.driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[href*='checkout']")
        safe_click(self.driver, element)

    def click_continue_shopping(self):
        element = self.driver.find_element(By.LINK_TEXT, "Tiếp tục mua sắm")
        safe_click(self.driver, element)

    def delete_first_product(self):
        self.get_cart_rows()[0].find_element(By.CSS_SELECTOR, ".ec-cart-pro-remove button").click()

    def is_cart_empty(self):
        try:
            return "trống" in self.driver.page_source.lower()
        except:
            return False

    def normalize_currency(self, text):
        return re.sub(r"[^\d]", "", text)

    def perform_action(self, driver, test_case):
        desc = test_case['Mô tả'].lower()
        data_test = test_case.get('Dữ liệu test') or ''
        expected = (test_case.get("Kỳ vọng") or "").lower()

        rows = self.get_cart_rows()

        if "số lượng" in data_test.lower():
            numbers = [int(s.split(":")[1].strip()) for s in data_test.split(",")]
            actual_qtys = []
            for i, qty in enumerate(numbers):
                input_box = self.get_quantity_input(rows[i])
                input_box.clear()
                input_box.send_keys(str(qty))
                input_box.send_keys(Keys.TAB)
                driver.implicitly_wait(1)

                actual = input_box.get_attribute("value") or "1"
                try:
                    actual_qtys.append(int(actual.strip()))
                except ValueError:
                    actual_qtys.append(1)

            if "tổng tiền sản phẩm" in expected:
                total = self.get_row_total(rows[0])
                multi_price = self.get_price(rows[0]) * self.get_quantity(rows[0])
                if total == multi_price:
                    return f"Tổng tiền sản phẩm là là hợp lệ"
                return f'Tổng tiền sản phẩm không hợp lệ'
            elif "tổng tiền" in expected:
                total_cart = self.get_cart_total()
                total_product = 0
                for row in rows:
                    total_product += self.get_row_total(row)
                if total_cart == total_product:
                    return f"Tổng tiền hiển thị chính xác"
                else:
                    return "Tổng tiền hiển thị không chính xác"

            if any(q == 0 for q in numbers):
                if any(a == 0 for a in actual_qtys):
                    return "vẫn giảm về 0"
                else:
                    return "Số lượng sản phẩm tối thiểu là 1"

            if any(q > 99 for q in numbers):
                if any(a > 99 for a in actual_qtys):
                    return "vượt số lượng tồn kho"
                else:
                    return "Số lượng sản phẩm không vượt quá tồn kho"
            else:
                return "Số lượng sản phẩm hợp lệ"

        if "xóa" in desc:
            self.delete_first_product()
            driver.implicitly_wait(1)
            return "Sản phẩm được xóa khỏi giỏ hàng"

        if "thanh toán" in desc:
            self.click_checkout()
            WebDriverWait(driver, 3).until(EC.url_contains("checkout"))
            current_url = driver.current_url
            if "checkout" in current_url:
                return "Chuyển hướng đến trang thanh toán"
            else:
                return f"Chuyển hướng thất bại. URL hiện tại: {current_url}"

        if "tiếp tục mua sắm" in desc:
            self.click_continue_shopping()
            WebDriverWait(driver, 3).until(EC.url_changes(self.url))
            current_url = driver.current_url
            if "product" in current_url:
                return "Chuyển hướng đến trang sản phẩm"
            else:
                return f"Chuyển hướng thất bại. URL hiện tại: {current_url}"

        if "giỏ hàng trống" in desc:
            return "Hiển thị thông báo 'Giỏ hàng của bạn đang trống'" if self.is_cart_empty() else "Giỏ hàng không trống"

        return "Không rõ hành động test"