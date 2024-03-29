import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import browser, driver_version, webdriver_path
from dotenv import load_dotenv
load_dotenv()


def setup_driver(browser, driver_version, webdriver_path):
    if browser == "chrome":
        from webdriver_manager.chrome import ChromeDriverManager

        try:
            driver = webdriver.Chrome(
                ChromeDriverManager(
                    driver_version,
                    cache_valid_range=183).install())
        except BaseException:
            print("Webdriver Manager Failed, setting up webdriver manually")
            if webdriver_path is not None:
                driver = webdriver.Chrome(webdriver_path)
            else:
                raise "Manual Webdriver Path is none, please input the webdriver path in setting file"
    elif browser == "firefox":
        from webdriver_manager.firefox import GeckoDriverManager

        try:
            driver = webdriver.Firefox(
                executable_path=GeckoDriverManager(
                    driver_version,
                    cache_valid_range=183).install())
        except BaseException:
            print("Webdriver Manager Failed, setting up webdriver manually")
            if webdriver_path is not None:
                driver = webdriver.Firefox(webdriver_path)
            else:
                raise "Manual Webdriver Path is none, please input the webdriver path in setting file"
    elif browser == "edge":
        from webdriver_manager.microsoft import EdgeChromiumDriverManager

        try:
            driver = webdriver.Edge(
                EdgeChromiumDriverManager(
                    driver_version,
                    cache_valid_range=183).install())
        except BaseException:
            print("Webdriver Manager Failed, setting up webdriver manually")
            if webdriver_path is not None:
                driver = webdriver.Edge(webdriver_path)
            else:
                raise "Manual Webdriver Path is none, please input the webdriver path in setting file"
    elif browser == "opera":
        from webdriver_manager.opera import OperaDriverManager

        try:
            driver = webdriver.Opera(
                executable_path=OperaDriverManager(
                    driver_version,
                    cache_valid_range=183).install())
        except BaseException:
            print("Webdriver Manager Failed, setting up webdriver manually")
            if webdriver_path is not None:
                driver = webdriver.Opera(webdriver_path)
            else:
                raise "Manual Webdriver Path is none, please input the webdriver path in setting file"
    elif browser == "chromium":
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.utils import ChromeType

        try:
            driver = webdriver.Chrome(
                ChromeDriverManager(
                    driver_version,
                    cache_valid_range=183,
                    chrome_type=ChromeType.CHROMIUM).install())
        except BaseException:
            print("Webdriver Manager Failed, setting up webdriver manually")
            if webdriver_path is not None:
                driver = webdriver.Chrome(webdriver_path)
            else:
                raise "Manual Webdriver Path is none, please input the webdriver path in setting file"
    elif browser == "ie":
        from webdriver_manager.microsoft import IEDriverManager

        try:
            driver = webdriver.Ie(
                IEDriverManager(
                    driver_version,
                    cache_valid_range=183).install())
        except BaseException:
            print("Webdriver Manager Failed, setting up webdriver manually")
            if webdriver_path is not None:
                driver = webdriver.Ie(webdriver_path)
            else:
                raise "Manual Webdriver Path is none, please input the webdriver path in setting file"
    else:
        raise "Browser not recognizable, please check the supported browser and the browser spelling in settings file"

    return driver


def setup_timeout(timeout):
    driver.wait = WebDriverWait(driver, timeout)


def wait_until(By, selector, conditions):
    driver.wait.until(
        conditions((By, selector))
    )


def click_button(selector, By):
    wait_until(By, selector, EC.presence_of_all_elements_located)
    wait_until(By, selector, EC.visibility_of_any_elements_located)

    driver.wait.until(
        EC.element_to_be_clickable((By, selector))
    ).click()


def send_form(keys, selector, By):
    driver.wait.until(
        EC.element_to_be_clickable((By, selector))
    ).send_keys(keys)


def login(username, password):
    '''
    Login to apps.unnes, only accept using Google auth.

    please fill username and password in .env file
    '''

    driver.get("https://apps.unnes.ac.id/")
    window_before = driver.window_handles[0]
    click_button("g-signin2", By.CLASS_NAME)

    # switch to login window
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    send_form(username, '//input[@type="email"]', By.XPATH)
    click_button(
        '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div',
        By.XPATH)

    # time.sleep(10)
    # isi password
    send_form(password, "//input[@type='password']", By.XPATH)

    # next
    click_button(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div",
        By.XPATH)
    driver.switch_to.window(window_before)

# go to elena dashboard


def elena():
    """
    go to active semester
    """
    click_button(
        "//a[contains(@href, 'https://apps.unnes.ac.id/30')]",
        By.XPATH)
    wait_until(By.CLASS_NAME, "xcomponent-outlet",
               EC.visibility_of_any_elements_located)
    driver.switch_to.frame(
        driver.find_element_by_class_name("xcomponent-component-frame"))
    wait_until(
        By.CLASS_NAME,
        "authfy-login",
        EC.visibility_of_any_elements_located)
    click_button(
        "//input[contains(@class, 'btn btn-lg btn-primary')]",
        By.XPATH)
    click_button(
        "//input[contains(@class, 'btn btn-lg btn-primary')]",
        By.XPATH)


if __name__ == "__main__":
    USERNAME = os.getenv("EMAIL_ELENA")
    PASSWORD = os.getenv("PASSWORD_ELENA")

    driver = setup_driver(browser, driver_version, webdriver_path)
    setup_timeout(60 * 5)
    login(USERNAME, PASSWORD)
    elena()
