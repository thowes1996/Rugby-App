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

def accept_privacy(driver):
    WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.CLASS_NAME, "css-47sehv"))
    )
    driver.find_element(By.CLASS_NAME, "css-47sehv").click()

def open_stats(driver):
    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='desktop']//a[2]//span[1]"))
        )
    driver.find_element(By.XPATH, "//div[@class='desktop']//a[2]//span[1]").click()
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cta.lazyloaded"))
    )
    driver.find_element(By.CLASS_NAME, "cta.lazyloaded").click()

def next_stat(driver, i: int):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='filter stats']"))
    )
    driver.find_element(By.XPATH, "//div[@class='filter stats']").click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"(//div[@class='list-item'][normalize-space()='{stats_list[i]}'])[1]"))
    )
    driver.find_element(By.XPATH, f"(//div[@class='list-item'][normalize-space()='{stats_list[i]}'])[1]").click()

def scrape_stats(driver):
    stats = {}
    players = driver.find_element(By.ID, "players-selector-result").text
    p = players.split("\n")
    if p[0] == "":
        return stats
    else:      
        for i in range(0, len(p), 3):
            stats[p[i + 1]] = p[i + 2]
        return stats



def pens_n_cons(driver):

    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "key-event"))
        )
    key_events = driver.find_elements(By.CLASS_NAME, "key-event")
    for i in range(1, len(key_events), 1):   
            event = driver.find_element(By.XPATH, f"(//div[@class='key-event'])[{i}]")
            if event.text == "Full Time" or event.text == "Half Time" or event.text == "Start":
                continue
            
            try:
                WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, f"(//div[@class='key-event'])[{i}]//div[@class='icon-image con']"))
                )
                print("conversion")
                name = event.find_element(By.CLASS_NAME, "name").text
                print(name)
            except TimeoutException:
                pass
            try:
                WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, f"(//div[@class='key-event'])[{i}]//div[@class='icon-image pg']"))
                )
                print("pen")
                name = event.find_element(By.CLASS_NAME, "name").text
                print(name)
            except TimeoutException:
                pass

def add_game(driver):
    game_id = int(URL[-6:])
    print(game_id)
    game_name = URL.removeprefix("https://www.rugbypass.com/live/").removesuffix(f"/?g={game_id}")
    print(game_name)

    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "team.home"))
    )
    home = driver.find_element(By.CLASS_NAME, "team.home").text.lower()
    away = driver.find_element(By.CSS_SELECTOR, "div[class='team-status'] div[class='team']").text.lower()
    print(away)
    home_query = f""" SELECT team_id FROM teams WHERE team_name = '{home}';
              """
    home_id = c.execute(home_query)
    home_id = int(home_id.fetchone()[0])
    print(home_id)
    away_query = f""" SELECT team_id FROM teams WHERE team_name = '{away}';
              """
    away_id = c.execute(away_query)
    away_id = int(away_id.fetchone()[0])
    print(away_id)

    query = """INSERT INTO games (game_id, game_name, home_id, away_id) 
                VALUES(?, ?, ?, ?);
            """
    value = (game_id, game_name, home_id, away_id)
    try:
        c.execute(query, value)
    except sqlite3.IntegrityError:
        quit()
    connect.commit()

if __name__ == '__main__':

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    chrome_options = Options()
    chrome_options.add_argument('-ignore-certificate-errors')

    connect = sqlite3.connect('C:/Users/thowes/Desktop/Projects/Rugby-App/player-stats.db')

    c = connect.cursor()
    URL = "https://www.rugbypass.com/live/bristol-vs-gloucester/?g=939003"
    driver.get(URL)
    stats_list = ["Carries", "Kicks", "Passes", "Metres Carried", "Line Breaks", "Offloads", "Defenders Beaten", "Try Assists", "Tries", "Turnovers Lost", "Carries Per Minute", "Tackles Made", "Tackles Missed", "Tackles Completed", "Dominant Tackles", "Turnovers Won", "Ruck Turnovers", "Lineouts Won", "Total Tackles Per Minute", "Red Cards", "Yellow Cards", "Penalties Conceded"]

    driver.set_window_position(2000,0)
    driver.maximize_window()
    accept_privacy(driver)
    add_game(driver)
    # pens_n_cons()
    # open_stats()
    # print(stats_list[0])
    # stats = scrape_stats()
    # print(stats)
    # for i in range(1, len(stats_list), 1):    
    #     next_stat(driver, i)
    #     time.sleep(1)
    #     print(stats_list[i] + ":")
    #     newstats = scrape_stats()
    #     print(newstats)

    connect.close()
    driver.quit()