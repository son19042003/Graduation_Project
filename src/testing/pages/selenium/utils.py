from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from unidecode import unidecode

def hide_obstructions(driver):
    selectors = [".swal2-container", ".swal2-popup", ".toast", ".overlay", ".modal", ".alert", "div[role='dialog']", "div[aria-label='Change your password']"]
    for selector in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("arguments[0].style.display = 'none';", el)
        except:
            continue

def safe_click(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
        hide_obstructions(driver)
        try:
            element.click()
        except Exception:
            driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        raise Exception(f"Lỗi khi click phần tử: {e.__class__.__name__}: {str(e)}")

def safe_type(driver, element, text):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        WebDriverWait(driver, 5).until(EC.visibility_of(element))
        hide_obstructions(driver)
        element.clear()
        element.send_keys(text)
    except Exception as e:
        raise Exception(f"Lỗi khi nhập liệu: {str(e)}")

def normalize(text):
    text = unidecode(text.lower().strip())
    text = re.sub(r'[.,:!?\"\'’“”]', '', text)
    return text

def set_quantity(driver, value):
        try:
            qty_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.qty-input"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", qty_input)
            qty_input.clear()
            qty_input.send_keys(str(value))
            
            body = driver.find_element(By.TAG_NAME, "body")
            body.click()
        except Exception as e:
            raise Exception(f"Lỗi khi set số lượng: {str(e)}")
        
def extract_number(text):
    """Trích xuất số nguyên từ chuỗi chứa tiền VNĐ."""
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else 0

def dismiss_password_warning(driver):
    driver.execute_script("""
        const modals = document.querySelectorAll('div[role="dialog"], [aria-label*="password"]');
        modals.forEach(el => el.remove());
    """)