from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException
import sqlite3
import sys
from statscraper import accept_privacy

def next_team(driver):
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "teams-grid"))
        )
    teams = driver.find_elements(By.CLASS_NAME, "teams-grid")

    for team in teams:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "https://www.rugbypass.com/teams/"))
        )
        team.find_element(By.PARTIAL_LINK_TEXT, "www.rugbypass.com").click()
        time.sleep(2)
        driver.back()


if __name__ == '__main__':
    service = Service(executable_path="C:/Users/thowes/Desktop/Projects/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    chrome_options = Options()
    chrome_options.add_argument('-ignore-certificate-errors')

    connect = sqlite3.connect('player-stats.db')

    c = connect.cursor()
    URL = "https://www.rugbypass.com/premiership/teams/"
    driver.get(URL)

    driver.set_window_position(2000, 0)
    driver.maximize_window()

    # def next_team(driver, i: int):
    #     teams.find
    accept_privacy(driver)

    next_team(driver)
    # for i in range(0, len(teams), 1):
    #     next_team(driver, i)
       


