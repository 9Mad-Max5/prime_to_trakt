import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from getpass import getpass

from credentials import *
from time import sleep
import time

page = "https://www.amazon.com/gp/video/settings/watch-history"

# Pfad zum aktuellen Skript
script_path = os.path.abspath(sys.argv[0])
sel_timeout = 60


def crawl_amazon(page, username, password, otp=None):
    # driver = webdriver.Chrome(os.path.join(script_path,"chromedriver.exe"))
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")  # Optional, but can be useful
    # driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    # driver.get(page)

    # SignIn_button = driver.find_element_by_xpath('//*[@id="nav-link-accountList"]/span')
    # SignIn_button.click()

    driver = webdriver.Chrome()
    driver.get(page)
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

    otp_textbox = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
    )
    otp_textbox.send_keys(otp)

    auth_button = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "auth-signin-button"))
    )
    auth_button.click()

    # Warte, bis das div-Element mit dem Attribut 'data-automation-id="watch-history"' vorhanden ist
    watch_history_div = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation-id="watch-history"]'))
    )

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

    # Hier kannst du nun bs4 verwenden, um die Daten von der Seite zu extrahieren
    # Beispiel: Finde alle Links auf der Seite
    # links = soup.find_all('a')
    # for link in links:
    #     print(link.get('href'))

    # Schließe den WebDriver am Ende
    driver.quit()

    return soup

