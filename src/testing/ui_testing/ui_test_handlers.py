import re
from ui_helpers import *

UI_TEST_HANDLERS = [
    (r"ngôn ngữ hiển thị", lambda page, case: check_page_language(page)),
    (r"liên kết.*\"([^\"]+)\"", lambda page, case: check_link_exists(page, re.search(r'"(.*?)"', case["Mô tả"]).group(1))),
    (r"màu nền nút.*\"([^\"]+)\"", lambda page, case: check_button_color(page, re.search(r'"(.*?)"', case["Mô tả"]).group(1))),
    (r"(click.*ô.*email|ô.*email.*click)", lambda page, case: check_input_clickable(page, "email")),
    (r"(click.*ô.*mật khẩu|ô.*mật khẩu.*click)", lambda page, case: check_input_clickable(page, "password")),
    (r"placeholder.*ô.*email", lambda page, case: check_placeholder(page, "email")),
    (r"placeholder.*ô.*mật khẩu", lambda page, case: check_placeholder(page, "password")),
    (r"mật khẩu.*(mã hóa|ẩn|hiển thị dạng \*)", lambda page, case: check_password_masked(page)),

    (r"placeholder.*ô tìm kiếm", lambda page, case: check_placeholder(page, "search")),
    (r"(hiển thị|tồn tại).*ô tìm kiếm", lambda page, case: check_search_box_visible(page)),
    (r"(hiển thị|tồn tại).*button tìm kiếm", lambda page, case: check_search_button_visible(page)),
    (r"(ô tìm kiếm.*nhập|nhập.*ô tìm kiếm)", lambda page, case: check_search_input_allows_all_characters(page)),

    (r"hiển thị đơn giá", lambda page, case: check_price_display(page), lambda tc: tc["Chức năng"] == "Xem chi tiết sản phẩm"),
    (r"hiển thị số lượng", lambda page, case: check_quantity_display(page), lambda tc: tc["Chức năng"] == "Xem chi tiết sản phẩm"),
    (r"hiển thị phân loại", lambda page, case: check_variant_display(page), lambda tc: tc["Chức năng"] == "Xem chi tiết sản phẩm"),
    (r"hiển thị nút thêm vào giỏ hàng", lambda page, case: check_add_to_cart_button(page), lambda tc: tc["Chức năng"] == "Xem chi tiết sản phẩm"),
    (r"hiển thị chức năng tăng giảm số lượng", lambda page, case: check_quantity_buttons(page), lambda tc: tc["Chức năng"] == "Xem chi tiết sản phẩm"),
    (r"hiển thị ô chọn phân loại", lambda page, case: check_variant_selector(page), lambda tc: tc["Chức năng"] == "Xem chi tiết sản phẩm"),
    (r"ngôn ngữ hiển thị", lambda page, case: check_page_language(page), lambda tc: tc["Chức năng"] == "Xem chi tiết sản phẩm"),

    (r"hiển thị.*(giao diện chung trang giỏ hàng|các cột)", lambda page, case: check_cart_layout(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),
    (r"hiển thị thông tin sản phẩm.*giỏ hàng", lambda page, case: check_cart_product_info(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),
    (r"hiển thị đơn giá sản phẩm", lambda page, case: check_cart_product_price(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),
    (r"hiển thị số lượng sản phẩm", lambda page, case: check_cart_product_quantity(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),
    (r"hiển thị tổng tiền. *của từng sản phẩm", lambda page, case: check_cart_product_total(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),
    (r"hiển thị tổng tiền", lambda page, case: check_cart_grand_total(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),
    (r"hiển thị button.*thanh toán", lambda page, case: check_cart_checkout_button(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),
    (r"hiển thị button.*xóa", lambda page, case: check_cart_remove_button(page), lambda tc: tc["Chức năng"] == "Giỏ hàng"),

    (r"giao diện trang thanh toán", lambda page, case: check_payment_layout(page), lambda tc: tc["Chức năng"] == "Thanh toán"),
    (r"nhãn các trường chi tiết thanh toán", lambda page, case: check_payment_labels(page), lambda tc: tc["Chức năng"] == "Thanh toán"),
    (r"placeholder các trường chi tiết thanh toán", lambda page, case: check_payment_placeholders(page), lambda tc: tc["Chức năng"] == "Thanh toán"),
    (r"hiển thị tóm tắt đơn hàng", lambda page, case: check_order_summary(page), lambda tc: tc["Chức năng"] == "Thanh toán"),
    (r"hiển thị phương thức thanh toán", lambda page, case: check_payment_methods(page), lambda tc: tc["Chức năng"] == "Thanh toán"),
    (r"radio button.*phương thức thanh toán", lambda page, case: check_payment_radio_buttons(page), lambda tc: tc["Chức năng"] == "Thanh toán"),
    (r"nút đặt hàng", lambda page, case: check_order_button(page), lambda tc: tc["Chức năng"] == "Thanh toán"),
]
