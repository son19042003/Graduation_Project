def test_login_valid(driver):
    driver.get('')
    driver.find_element().send_keys()
    driver.find_element().send_keys()
    driver.find_element().click()
    assert 'dasboard' in driver.current_url

def test_login_invalid(driver):
    driver.get('')
    driver.find_element().send_keys()
    driver.find_element().send_keys()
    driver.find_element().click()
    error = driver.find_element().text
    assert 'Invalid' in error