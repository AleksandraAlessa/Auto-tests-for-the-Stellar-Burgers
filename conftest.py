import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from generators import generate_unique_email
from data import DEFAULT_PASSWORD, MAIN_URL, LOGIN_URL
from locators import StellarLocators
from test_data import TEST_USER
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

@allure.step("Авторизоваться как {email}")
def login_user(driver, email, password):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located(StellarLocators.LOGIN_EMAIL)).send_keys(email)
    driver.find_element(*StellarLocators.LOGIN_PASSWORD).send_keys(password)
    driver.find_element(*StellarLocators.LOGIN_SUBMIT).click()
    wait.until(EC.url_to_be(MAIN_URL))
    wait.until(EC.visibility_of_element_located(StellarLocators.CONSTRUCTOR_BUTTON))


@pytest.fixture(scope="session")
def registered_user():
    return TEST_USER


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)

    yield driver
    driver.quit()


@pytest.fixture
def new_user():
    email = generate_unique_email()
    password = DEFAULT_PASSWORD
    name = "Тестовый Пользователь"
    return {"email": email, "password": password, "name": name}