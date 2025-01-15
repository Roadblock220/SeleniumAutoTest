import pytest
import requests

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

URL = "https://pokemonbattle-stage.ru/"

def test_positive_login(browser):
    """
    TC-1. Positive case
    """
    browser.get(URL)
		
		# ищем по селектору инпут "Email", кликаем по нему и вводим значение email
    email_input = WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="f_email"]')))
    email_input.click()
    email_input.send_keys('PRman99@yandex.ru') # введи тут email своего тестового аккаунта на stage окружении
		
		# ищем по селектору инпут "Password", кликаем по нему и вводим значение пароля
    password_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="f_pass"]')
    password_input.click()
    password_input.send_keys('Aspirine1309') # введи тут пароль своего тестового аккаунта на stage окружении
		
		# ищем по селектору кнопку "Войти" и кликаем по ней
    enter = browser.find_element(by=By.CSS_SELECTOR, value='[class*="send_auth"]')
    enter.click()
    
    # ждем успешного входа и обновления страницы
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
		
		# ищем элемент на странице, который содержит ID тренера
    trainer_id = browser.find_element(by=By.CLASS_NAME, value='header__id-texts')
		
    # сравниваем полученный ID из кода теста с ID вашего тестового тренера
    assert trainer_id.text.replace('\n', ': ') == 'ID: 1681', 'Unexpected ID trainer' # введи тут ID своего тренера

CASES = [
    ('1', 'PRman99yandex.ru', 'Aspirine1309', ['Введите почту', '']),
    ('2', 'PRman99@yandex.ru', 'Aspirine', ['', 'Неверные логин или пароль']),
    ('3', '', 'Aspirine1309', ['Введите почту', '']),
    ('4', 'PRman99@yandex.ru', '', ['', 'Введите пароль']),
    ('5', '', '', ['Введите почту', 'Введите пароль'])
]

@pytest.mark.parametrize('case_number, email, password, alerts', CASES)
def test_negative_login(case_number, email, password, alerts, browser):
    """
    TC-2. Negative cases
    """
    logger.info(f'CASE : {case_number}')
    browser.get(URL)
		
    email_input = WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="f_email"]')))
    email_input.click()
    email_input.send_keys(email)
		
    password_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="f_pass"]')
    password_input.click()
    password_input.send_keys(password) 

    enter = browser.find_element(by=By.CSS_SELECTOR, value='[class*="send_auth"]')
    enter.click()
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '[class*="auth__error"]')))
    alerts_messages = browser.find_elements(by=By.CSS_SELECTOR, value='[class*="auth__error"]')
    alert_list = []
    for element in alerts_messages:
        alert_list.append(element.text)
    assert alert_list == alerts, 'Unexpected alerts in authentication form'