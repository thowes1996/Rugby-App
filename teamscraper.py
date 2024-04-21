from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException
import sqlite3
from statscraper import accept_privacy

prem_teams = ["bath", "bristol", "exeter-chiefs", "gloucester", "harlequins", "leicester", "newcastle", "northampton", "sale", "saracens"]
def next_team(driver, i: int):
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='https://www.rugbypass.com/teams/{prem_teams[i]}/']"))
        )
    driver.find_element(By.XPATH, f"//a[@href='https://www.rugbypass.com/teams/{prem_teams[i]}/']").click()

def get_players(driver, i):
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "player-col"))
        )
    players = driver.find_elements(By.CLASS_NAME, "player-col")
    for player in players:
        name = player.find_element(By.CLASS_NAME, "name").text
        position = player.find_element(By.CLASS_NAME, "position").text
        if position == 'Flanker 7':
            position = 'Openside Flanker'
        if position == 'Centre 13':
            position = 'Outside Centre'
        if position == 'Lock 4':
            position == 'Lock'
        if position[-4:] == 'Wing':
            position == 'Wing'
        if position[-4:] == 'Prop':
            position = 'Prop'
        query = """INSERT INTO players (player_name, position, team_id)
                    VALUES (?, ?, ?);
                """
        values = (name, position, i + 1)
        c.execute(query, values)
    connect.commit()

if __name__ == '__main__':
    service = Service(executable_path="C:/Users/thowes/Desktop/Projects/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    chrome_options = Options()
    chrome_options.add_argument('-ignore-certificate-errors')

    URL = "https://www.rugbypass.com/premiership/teams/"
    driver.get(URL)

    driver.set_window_position(2000, 0)
    driver.maximize_window()
    connect = sqlite3.connect('C:/Users/thowes/Desktop/Projects/Rugby-App/player-stats.db')
    c = connect.cursor()

    accept_privacy(driver)
    query = """INSERT INTO teams (team_name)
                VALUES(?);"""
    for i in range(0, len(prem_teams), 1):
        value = (prem_teams[i],)
        try:
            c.execute(query, value)
        except sqlite3.IntegrityError:
            quit()
    
    connect.commit()
    for i in range(0, len(prem_teams), 1):
        next_team(driver, i)
        get_players(driver, i)
        driver.back()        
       


