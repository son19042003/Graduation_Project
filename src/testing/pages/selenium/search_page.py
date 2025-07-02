from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from unidecode import unidecode

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost/ecommerce"

    def load(self):
        self.driver.get(self.url)

    def extract_keyword(self, data):
        match = re.search(r"Từ khóa:\s*(.+)", data)
        return match.group(1).strip() if match else ''

    def enter_keyword(self, keyword):
        input_box = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='search']"))
        )
        input_box.clear()
        input_box.send_keys(keyword)
        return input_box

    def click_search(self):
        search_btn = self.driver.find_element(By.CSS_SELECTOR, ".ec-btn-group-form button[type='submit']")
        search_btn.click()

    def press_enter(self, element):
        element.send_keys(Keys.ENTER)

    def wait_for_load(self):
        WebDriverWait(self.driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")

    def get_product_names(self):
        product_names = self.driver.find_elements(By.CSS_SELECTOR, ".ec-pro-title")
        return [el.text.strip() for el in product_names if el.is_displayed()]

    def has_products(self):
        products = self.driver.find_elements(By.CSS_SELECTOR, ".ec-product-inner")
        return any(p.is_displayed() for p in products)

    def has_load_more_button(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "div.ec-pro-pagination button.btn-primary")
            return btn.is_displayed()
        except:
            return False

    def normalize(self, text):
        return re.sub(r"[.,:!?\"']", "", unidecode(text.lower().strip()))

    def all_products_match_keyword(self, names, keyword):
        keyword_norm = self.normalize(keyword)
        return all(keyword_norm in self.normalize(name) for name in names)

    def is_numeric(self, keyword):
        return keyword.strip().isdigit()

    def is_whitespace(self, keyword):
        return keyword.strip() == ''

    def is_special_character(self, keyword):
        return re.match(r"^[^\w\s]+$", keyword) is not None