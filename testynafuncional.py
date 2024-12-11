import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_module(module):
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://msk.rt.ru/")

def teardown_module(module):
    driver.quit()


def test_home_page_loads():
    assert "Ростелеком" in driver.title


def test_main_menu_visible():
    main_menu = driver.find_element(By.CLASS_NAME, "menu")
    assert main_menu.is_displayed()


def test_connection_link():
    connection_link = driver.find_element(By.LINK_TEXT, "Подключение")
    connection_link.click()
    assert "Подключение" in driver.title


def test_search_functionality():
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Интернет" + Keys.RETURN)
    assert "Результаты поиска" in driver.page_source


def test_contact_info():
    contact_button = driver.find_element(By.LINK_TEXT, "Контакты")
    contact_button.click()
    assert "Контакты" in driver.page_source


def test_feedback_form():
    feedback_link = driver.find_element(By.LINK_TEXT, "Обратная связь")
    feedback_link.click()
    feedback_form = driver.find_element(By.ID, "feedback-form")
    assert feedback_form.is_displayed()


def test_social_links():
    social_links = driver.find_elements(By.CLASS_NAME, "social-link")
    assert len(social_links) > 0
    for link in social_links:
        assert link.is_displayed()


def test_submit_request():
    request_button = driver.find_element(By.ID, "submit-request")
    request_button.click()
    assert "Заявка" in driver.page_source


def test_tariffs_section():
    tariffs_link = driver.find_element(By.LINK_TEXT, "Тарифы")
    tariffs_link.click()
    assert "Тарифы" in driver.title


def test_coverage_map():
    coverage_map_button = driver.find_element(By.LINK_TEXT, "Карта покрытия")
    coverage_map_button.click()
    coverage_map = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "coverage-map"))
    )
    assert coverage_map.is_displayed()

if __name__ == "__main__":
    pytest.main()
