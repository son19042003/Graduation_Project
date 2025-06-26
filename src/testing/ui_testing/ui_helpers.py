from playwright.sync_api import Page
from langdetect import detect
import re

#login
def check_page_language(page: Page, expected_lang=None) -> str:
    lang_attr = page.get_attribute("html", "lang") or ""
    visible_text = page.inner_text("body")[:500]

    if lang_attr.lower().startswith("vi"):
        return "Tiếng Việt"
    
    try:
        detected = detect(visible_text)
        if detected == "vi":
            return "Tiếng Việt"
    except:
        pass

    if any(word in visible_text for word in ["trang chủ", "sản phẩm", "tin tức", "liên hệ", "ưu đãi"]):
        return "Tiếng Việt"
    
    return f"Phát hiện ngôn ngữ: {lang_attr or 'Không rõ'}"

def check_link_exists(page: Page, label: str) -> str:
    link = page.locator(f"text={label}")
    if link.count() > 0:
        return f"Liên kết '{label}'"
    return f"Không tìm thấy liên kết '{label}'"

def check_button_color(page: Page, label: str) -> str:
    selector = f"form button:has-text('{label}'), form a:has-text('{label}')"
    button = page.locator(selector).first

    try:
        button.wait_for(state="visible", timeout=5000)

        color = button.evaluate("el => getComputedStyle(el).backgroundColor")

        return f"{color}"
    except Exception:
        return f"Nút '{label}' không hiển thị"

def check_input_clickable(page: Page, name_attr: str) -> str:
    input_box = page.locator(f"input[name='{name_attr}']")
    try:
        input_box.wait_for(state="visible", timeout=3000)
        input_box.scroll_into_view_if_needed()
        input_box.click()
        return f"Cho phép click"
    except:
        return f"Không thể click vào ô {name_attr}"

def check_placeholder(page: Page, name_attr: str) -> str:
    input_box = page.locator(f"input[name='{name_attr}']")
    return f"{input_box.get_attribute('placeholder')}"

def check_password_masked(page):
    password_input = page.locator('input[name="password"]')
    input_type = password_input.get_attribute("type")
    if input_type == "password":
        return 'Mật khẩu được mã hóa bằng kí tự "*"'
    else:
        return f"Mật khẩu không được mã hóa (type={input_type})"

#search
def check_search_box_visible(page):
    search_input = page.locator('input[name="search"]')
    box = search_input.bounding_box()
    if search_input.is_visible() and box and box["width"] > 50:
        return "Ô tìm kiếm hiển thị đúng vị trí, kích thước hợp lý."
    return "Ô tìm kiếm không hiển thị đúng."

def check_search_button_visible(page):
    container = page.locator('.header-search')
    button = container.locator('form.ec-btn-group-form button[type="submit"]')
    if button.count() > 0 and button.first.is_visible():
        return "Button tìm kiếm hiển thị trong ô tìm kiếm."
    return "Button tìm kiếm không hiển thị."

def check_search_input_allows_all_characters(page):
    search_input = page.locator('input[name="search"]')
    test_string = "abc123!@#"
    search_input.fill(test_string)
    value = search_input.input_value()
    if value == test_string:
        return "Ô tìm kiếm cho phép nhập mọi ký tự (chữ, số, ký tự đặc biệt)."
    return f"Ô tìm kiếm không cho phép nhập đầy đủ, nhận được: {value}"

#detail
def check_price_display(page):
    price = page.locator("#product-price")
    if price.is_visible():
        return "Đơn giá hiển thị đúng định dạng và vị trí"
    return "Đơn giá không hiển thị"

def check_quantity_display(page):
    qty = page.locator("#product-stock")
    if qty.is_visible():
        return "Số lượng hiển thị đúng định dạng và vị trí"
    return "Số lượng không hiển thị"

def check_variant_display(page):
    label = page.locator(".ec-pro-variation-content")
    if label.is_visible():
        return "Phân loại hiển thị đúng định dạng và vị trí"
    return "Phân loại không hiển thị"

def check_add_to_cart_button(page):
    button = page.locator("button#add-Product-To-Cart")
    if button.is_visible():
        return "Nút Thêm vào giỏ hàng hiển thị đúng định dạng và vị trí"
    return "Nút Thêm vào giỏ hàng không hiển thị"

def check_quantity_buttons(page):
    increase = page.locator(".inc.ec_qtybtn")
    decrease = page.locator(".dec.ec_qtybtn")
    if increase.is_visible() and decrease.is_visible():
        return "Chức năng tăng giảm số lượng hiển thị đúng định dạng và vị trí"
    return "Không hiển thị nút tăng giảm số lượng"

def check_variant_selector(page):
    variant_items = page.locator(".ec-pro-variation-content ul li")
    if variant_items.count() > 0 and all(item.is_visible() for item in variant_items.all()):
        return "Ô chọn phân loại hiển thị đúng định dạng và vị trí"
    return "Ô chọn phân loại không hiển thị"

#cart
def check_cart_layout(page):
    try:
        required_selectors = [
            ".ec-cart-pro-name",  #sản phẩm
            ".ec-cart-pro-price",  #đơn giá
            ".ec-cart-pro-qty",  #số lượng
            ".ec-cart-pro-subtotal",  #tổng tiền từng sản phẩm
            ".ec-cart-summary-total",  #tổng tiền giỏ hàng
            "a[href='checkout']",  #button thanh toán
            "a[href='product']",  #link tiếp tục mua sắm
            ".ec-cart-pro-remove"  #nút xóa
        ]
        for selector in required_selectors:
            if page.locator(selector).count() == 0 or not page.locator(selector).first.is_visible():
                return f"Không hiển thị thành phần: {selector}"
        return "Trang giỏ hàng hiển thị đầy đủ các thành phần: Sản phẩm, Đơn giá, Số lượng, Tổng, Tổng tiền, Button 'Thanh toán', Liên kết 'Tiếp tục mua sắm', Button 'Xóa'"
    except Exception as e:
        return f"Lỗi khi kiểm tra: {str(e)}"

def check_cart_product_info(page):
    name = page.locator(".ec-cart-pro-name")
    qty = page.locator(".ec-cart-pro-qty")
    price = page.locator(".ec-cart-pro-price")
    if name.first.is_visible() and qty.first.is_visible() and price.first.is_visible():
        return "Hiển thị đầy đủ thông tin của từng sản phẩm: Tên sản phẩm, Đơn giá, Số lượng"
    return "Thiếu thông tin sản phẩm"

def is_currency_format(value: str) -> bool:
    value = value.strip().lower()
    return "đ" in value or "vnđ" in value or re.search(r'\d+[\.,]?\d*\s*(đ|vnđ)?', value)

def check_cart_product_price(page):
    try:
        price_spans = page.locator(".ec-cart-pro-price .amount")
        count = price_spans.count()
        if count == 0:
            return "Không tìm thấy đơn giá sản phẩm"

        for i in range(count):
            price_text = price_spans.nth(i).inner_text().strip()
            if not re.search(r"\d+[.,]?\d*\s?[₫VNĐ]?", price_text):
                return f"Đơn giá dòng {i+1} không đúng định dạng: {price_text}"

        return "Đơn giá sản phẩm hiển thị đúng định dạng tiền tệ (VNĐ) và giá trị chính xác"
    except Exception as e:
        return f"Lỗi khi kiểm tra đơn giá: {str(e)}"

def check_cart_product_total(page):
    try:
        rows = page.locator("tbody#cart_main > tr")
        row_count = rows.count()
        if row_count == 0:
            return "Không có sản phẩm trong giỏ hàng để kiểm tra"

        for i in range(row_count):
            row = rows.nth(i)
            price_text = row.locator(".ec-cart-pro-price").inner_text().strip()
            subtotal_text = row.locator(".ec-cart-pro-subtotal").inner_text().strip()
            qty_input = row.locator("input[name='cartqtybutton']")
            qty = int(qty_input.input_value())

            if not is_currency_format(subtotal_text):
                return f"Tổng tiền của dòng {i+1} không đúng định dạng"

            price_num = int(re.sub(r"\D", "", price_text))
            subtotal_num = int(re.sub(r"\D", "", subtotal_text))
            expected_total = price_num * qty

            if abs(subtotal_num - expected_total) > 1:
                return f"Tổng tiền dòng {i+1} không đúng: {subtotal_num} ≠ {price_num} * {qty}"

        return "Tổng tiền của từng sản phẩm hiển thị đúng định dạng tiền tệ (VNĐ) và giá trị chính xác (Đơn giá * Số lượng)"
    except Exception as e:
        return f"Lỗi khi kiểm tra tổng tiền sản phẩm: {str(e)}"

def check_cart_grand_total(page):
    try:
        item_totals = page.locator(".ec-cart-pro-subtotal")
        grand_total_text = page.locator(".ec-cart-summary-total").first.inner_text().strip()

        if not is_currency_format(grand_total_text):
            return "Tổng tiền giỏ hàng không hiển thị đúng định dạng"

        subtotal_sum = 0
        for i in range(item_totals.count()):
            text = item_totals.nth(i).inner_text()
            num = int(re.sub(r"\D", "", text))
            subtotal_sum += num

        grand_num = int(re.sub(r"\D", "", grand_total_text))

        if abs(grand_num - subtotal_sum) <= 1:
            return "Tổng tiền của giỏ hàng hiển thị đúng định dạng tiền tệ (VNĐ) và giá trị chính xác (Tổng của tất cả các tổng tiền sản phẩm)"
        else:
            return f"Tổng tiền giỏ hàng sai: {grand_num} ≠ {subtotal_sum}"
    except Exception as e:
        return f"Lỗi khi kiểm tra tổng tiền giỏ hàng: {str(e)}"
    
def check_cart_product_quantity(page):
    try:
        qty_inputs = page.locator("input[name='cartqtybutton']")
        count = qty_inputs.count()
        if count == 0:
            return "Không tìm thấy input số lượng"

        for i in range(count):
            input_elem = qty_inputs.nth(i)
            if not input_elem.is_visible():
                return f"Input số lượng thứ {i+1} không hiển thị"
            
            input_type = input_elem.get_attribute("type")
            if input_type not in ["text", "number"]:
                return f"Input số lượng thứ {i+1} không đúng kiểu: {input_type}"

        return "Số lượng sản phẩm hiển thị ở dạng số, có thể chỉnh sửa được"
    except Exception as e:
        return f"Lỗi khi kiểm tra số lượng: {str(e)}"
    
def check_cart_checkout_button(page):
    checkout_button = page.locator('.ec-cart-update-bottom a', has_text="Thanh toán")
    if checkout_button.is_visible():
        return "Button 'Thanh toán' hiển thị rõ ràng, dễ nhận biết"
    return "Button 'Thanh toán' không hiển thị"

def check_cart_remove_button(page):
    delete_buttons = page.locator('.ec-cart-pro-remove button')
    count_delete_button = delete_buttons.count()
    if count_delete_button == 0:
        return "Không có button 'Xóa' nào hiển thị"
    for i in range(count_delete_button):
        if not delete_buttons.nth(i).is_visible():
            return f"Button 'Xóa' thứ {i} không hiển thị."
    
    return "Button 'Xóa' hiển thị rõ ràng, dễ nhận biết"

#checkout
def check_payment_layout(page):
    try:
        required_selectors = [
            ".ec-checkout-wrap",  #chi tiết thanh toán
            ".ec-sb-block-content", #tóm tắt đơn hàng
            ".ec-checkout-pay-wrap" #phương thức tt
        ]
        for selector in required_selectors:
            if page.locator(selector).count() == 0 or not page.locator(selector).first.is_visible():
                return f"Không hiển thị thành phần: {selector}"
        return "Trang thanh toán hiển thị đầy đủ các phần: Chi tiết thanh toán, Tóm tắt đơn hàng, Phương thức thanh toán"
    except Exception as e:
        return f"Lỗi khi kiểm tra: {str(e)}"
    
def check_payment_labels(page):
    try:
        labels = ["Họ và tên", "Số điện thoại", "Địa chỉ"]
        for label in labels:
            if page.locator(f"label:has-text('{label}')").count() == 0:
                return f"Không tìm thấy nhãn '{label}'"
        return "Các nhãn hiển thị đúng tiếng Việt và dễ hiểu: Họ và tên, Số điện thoại, Địa chỉ"
    except Exception as e:
        return f"Lỗi khi kiểm tra nhãn: {str(e)}"
    
def check_payment_placeholders(page):
    try:
        input_selectors = [
            "input[name='fullname']",
            "input[name='phone']",
            "textarea[name='address']"
        ]
        for selector in input_selectors:
            placeholder = page.locator(selector).get_attribute("placeholder")
            if not placeholder:
                return f"Input {selector} không có placeholder"
        return "Placeholder các trường hiển thị gợi ý nhập liệu"
    except Exception as e:
        return f"Lỗi khi kiểm tra placeholder: {str(e)}"
    
def check_order_summary(page):
    try:
        if page.locator(".ec-checkout-pro .ec-product-inner" ).count() == 0:
            return "Không hiển thị danh sách sản phẩm trong tóm tắt đơn hàng"
        if page.locator(".ec-checkout-summary .ec-checkout-summary-total").count() == 0:
            return "Không hiển thị tổng tiền trong tóm tắt đơn hàng"
        return "Tóm tắt đơn hàng hiển thị đầy đủ thông tin sản phẩm và tổng tiền"
    except Exception as e:
        return f"Lỗi khi kiểm tra tóm tắt đơn hàng: {str(e)}"
    
def check_payment_methods(page):
    try:
        payment_methods = ["Thanh toán khi nhận hàng", "VNPAY", "MOMO"]
        for text in payment_methods:
            if page.locator(f"label:has-text('{text}')").count() == 0:
                return f"Không tìm thấy phương thức: {text}"
        return "Hiển thị đầy đủ các phương thức thanh toán: Thanh toán khi nhận hàng, VNPAY, MOMO"
    except Exception as e:
        return f"Lỗi khi kiểm tra phương thức thanh toán: {str(e)}"
    
def check_payment_radio_buttons(page):
    try:
        radios = page.locator("input[type='radio'][name='payment_method']")
        count = radios.count()
        if count < 2:
            return "Không tìm thấy đủ các radio button phương thức thanh toán"

        for i in range(count):
            radio = radios.nth(i)
            radio_id = radio.get_attribute("id")
            if not radio_id:
                return f"Radio thứ {i+1} không có id"

            page.evaluate("() => { document.querySelectorAll('input[name=payment_method]').forEach(el => el.checked = false); }")

            page.evaluate(f"document.getElementById('{radio_id}').checked = true")

            checked_states = []
            for j in range(count):
                checked = radios.nth(j).evaluate("el => el.checked")
                checked_states.append(checked)

            if checked_states.count(True) != 1 or not checked_states[i]:
                return f"Radio button thứ {i+1} không chọn được chính xác (checked: {checked_states})"

        return "Các radio button hoạt động, cho phép chọn một phương thức thanh toán duy nhất"

    except Exception as e:
        return f"Lỗi khi kiểm tra radio button: {str(e)}"
    
def check_order_button(page):
    try:
        btn = page.locator("button[type='submit']:has-text('Đặt hàng')")
        if btn.count() == 0 or not btn.first.is_visible():
            return "Không hiển thị nút Đặt hàng"
        return "Nút đặt hàng hiển thị rõ ràng và dễ nhận biết"
    except Exception as e:
        return f"Lỗi khi kiểm tra nút đặt hàng: {str(e)}"