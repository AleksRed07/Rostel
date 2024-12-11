import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


BASE_URL = "https://www.rt.ru/"


def test_main_page_loads(driver):
    driver.get(BASE_URL)
    assert "Ростелеком" in driver.title

def test_navigation_links(driver):
    driver.get(BASE_URL)
    links = driver.find_elements(By.CSS_SELECTOR, "header a")
    assert len(links) > 0
    for link in links:
        href = link.get_attribute("href")
        assert href is not None

def test_contact_form_submit(driver):
    driver.get(BASE_URL)
    contact_button = driver.find_element(By.LINK_TEXT, "Контакты")
    contact_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "contact-form"))
    )
    name_field = driver.find_element(By.NAME, "name")
    name_field.send_keys("Тест")
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys("test@example.com")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert success_message.is_displayed()


def test_logo_visibility(driver):
    driver.get(BASE_URL)
    logo = driver.find_element(By.CLASS_NAME, "site-logo")
    assert logo.is_displayed()

def test_adaptive_layout(driver):
    driver.set_window_size(375, 812)  # Размер экрана для смартфона
    driver.get(BASE_URL)
    menu = driver.find_element(By.CLASS_NAME, "mobile-menu")
    assert menu.is_displayed()


def test_page_load_time(driver):
    driver.get(BASE_URL)
    navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
    load_event_end = driver.execute_script("return window.performance.timing.loadEventEnd")
    load_time = load_event_end - navigation_start
    assert load_time < 3000


def test_https_connection(driver):
    driver.get(BASE_URL)
    assert "https" in driver.current_url

def test_sql_injection_protection(driver):
    driver.get(BASE_URL + "search?q=1' OR '1'='1")
    no_error = driver.find_elements(By.CSS_SELECTOR, ".error-message")
    assert len(no_error) == 0

def test_xss_protection(driver):
    driver.get(BASE_URL)
    script = "<script>alert('XSS')</script>"
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(script)
    search_box.submit()
    alerts = driver.find_elements(By.CSS_SELECTOR, "alert")
    assert len(alerts) == 0


def test_navigation_to_news(driver):
    driver.get(BASE_URL)
    news_link = driver.find_element(By.LINK_TEXT, "Новости")
    news_link.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "news-list"))
    )
    assert "Новости" in driver.title

def test_footer_links(driver):
    driver.get(BASE_URL)
    footer_links = driver.find_elements(By.CSS_SELECTOR, "footer a")
    for link in footer_links:
        href = link.get_attribute("href")
        assert href.startswith("http")
