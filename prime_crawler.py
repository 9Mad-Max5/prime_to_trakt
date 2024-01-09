import pickle
import time
import os

from socket import gethostname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup


# script_path = os.path.abspath(sys.argv[0])

def crawl_amazon(page, username, password, totp=None, full=False):
    sel_timeout = 60
    device_id = gethostname()  # Automatisch die Hostname als Device ID verwenden
    cookie_filename = f'{device_id}_{username}_cookies.pkl'
    # driver = webdriver.Chrome(os.path.join(script_path,"chromedriver.exe"))
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")  # Optional, but can be useful
    # driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    # driver.get(page)

    # driver = webdriver.Chrome()
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--window-size=1920,1080")  

    driver = webdriver.Chrome(options=set_chrome_options())

    if os.path.exists(cookie_filename):
        load_cookies(driver, cookie_filename)
        driver.get(page)
        try:
            _ = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation-id="watch-history"]'))
            )
        except:
            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ap_email"))
                )
                login_procedure(driver, username, password, sel_timeout, totp)
            except:
                login_procedure_pw(driver, password, sel_timeout, totp)


    else:
        driver.get(page)
        login_procedure(driver, username, password, sel_timeout, totp)


    # Warte, bis das div-Element mit dem Attribut 'data-automation-id="watch-history"' vorhanden ist
    watch_history_div = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation-id="watch-history"]'))
    )

    if full:
        # Scrollen für 10 Sekunden
        scroll_duration = 10  # in Sekunden

        # Startzeitpunkt
        start_time = time.time()

        while time.time() - start_time < scroll_duration:
            # Führe JavaScript-Code aus, um um eine bestimmte Entfernung zu scrollen
            driver.execute_script('window.scrollBy(0, 500);')  # Hier 500 ist die Vertikale Scroll-Entfernung
            time.sleep(0.5)  # Wartezeit in Sekunden zwischen den Scroll-Schritten

    # Warte bis mindestens eine Checkbox gefunden wird
    checkboxes = WebDriverWait(watch_history_div, sel_timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, './/input[@type="checkbox"]'))
    )

    # Klicke jede Checkbox an
    for checkbox in checkboxes:
        checkbox.click()


    # Greife auf den HTML-Quellcode der Seite zu
    page_source = driver.page_source

    # Verwende BeautifulSoup, um die Daten zu scrapen
    soup = BeautifulSoup(page_source, 'html.parser')

    save_cookies(driver, cookie_filename)

    # Schließe den WebDriver am Ende
    driver.quit()

    return soup

def save_cookies(driver, filename):
    # Hole die Cookies vom WebDriver
    cookies = driver.get_cookies()

    # Speichere die Cookies in einer Datei
    with open(filename, 'wb') as file:
        pickle.dump(cookies, file)

# def load_cookies(driver, filename):
#     # Lade die Cookies aus der Datei
#     with open(filename, 'rb') as file:
#         cookies = pickle.load(file)

#     # Setze die Cookies im WebDriver
#     for cookie in cookies:
#         driver.add_cookie(cookie)

def load_cookies(driver, filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        print("Loading cookies from " + filename)
        cookies = pickle.load(open(filename, "rb"))

        # Enables network tracking so we may use Network.setCookie method
        driver.execute_cdp_cmd('Network.enable', {})

        # Iterate through pickle dict and add all the cookies
        for cookie in cookies:
            # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
            if 'expiry' in cookie:
                cookie['expires'] = cookie['expiry']
                del cookie['expiry']

            # Replace domain 'apple.com' with 'microsoft.com' cookies
            cookie['domain'] = cookie['domain'].replace('apple.com', 'microsoft.com')

            # Set the actual cookie
            driver.execute_cdp_cmd('Network.setCookie', cookie)

        # Disable network tracking
        driver.execute_cdp_cmd('Network.disable', {})
        return 1

    print("Cookie file " + filename + " does not exist.")
    return 0

def login_procedure(driver, username, password, sel_timeout, totp=None):
    username_textbox = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "ap_email"))
    )
    username_textbox.send_keys(username)

    Continue_button = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "continue"))
    )
    Continue_button.click()

    password_textbox = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "ap_password"))
    )
    password_textbox.send_keys(password)

    remember_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@type="checkbox" and @name="rememberMe"]')
        )
    )
    remember_checkbox.click()

    SignIn_button = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "signInSubmit"))
    )
    SignIn_button.click()

    if totp:
        totp_textbox = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
        )
        totp_textbox.send_keys(totp)

        auth_button = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_element_located((By.ID, "auth-signin-button"))
        )
        auth_button.click()

def login_procedure_pw(driver, password, sel_timeout, totp=None):
    password_textbox = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "ap_password"))
    )
    password_textbox.send_keys(password)

    remember_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@type="checkbox" and @name="rememberMe"]')
        )
    )
    remember_checkbox.click()

    SignIn_button = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "signInSubmit"))
    )
    SignIn_button.click()

    # totp not active during just pw login
    # if totp:
    #     totp_textbox = WebDriverWait(driver, sel_timeout).until(
    #         EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
    #     )
    #     totp_textbox.send_keys(totp)

    #     auth_button = WebDriverWait(driver, sel_timeout).until(
    #         EC.presence_of_element_located((By.ID, "auth-signin-button"))
    #     )
    #     auth_button.click()

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")  
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options