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
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "players-selector-result"))
    )
    players = driver.find_element(By.ID, "players-selector-result").text
    p = players.split("\n")
    if p[0] == "":
        return stats
    else:      
        for i in range(0, len(p), 3):
            stats[p[i + 1]] = p[i + 2]
        return stats



def pens_n_cons(driver):
    penalties = {}
    conversions = {}
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
                name = event.find_element(By.CLASS_NAME, "name").text
                if name not in conversions:
                    conversions[name] = 1
                else:
                    conversions[name] += 1

            except TimeoutException:
                pass
            try:
                WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, f"(//div[@class='key-event'])[{i}]//div[@class='icon-image pg']"))
                )
                name = event.find_element(By.CLASS_NAME, "name").text
                if name not in penalties:
                    penalties[name] = 1
                else:
                    penalties[name] += 1
            except TimeoutException:
                pass

    return penalties, conversions

def add_game(driver, game_id, game_name):
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "team.home"))
    )
    home = driver.find_element(By.CLASS_NAME, "team.home").text.lower()
    away = driver.find_element(By.CSS_SELECTOR, "div[class='team-status'] div[class='team']").text.lower()
    home_query = f""" SELECT team_id FROM teams WHERE team_name LIKE '{home}';
                    """
    home_id = c.execute(home_query)
    home_id = int(home_id.fetchone()[0])
    away_query = f""" SELECT team_id FROM teams WHERE team_name LIKE '{away}';
                    """
    away_id = c.execute(away_query)
    away_id = int(away_id.fetchone()[0])

    home_score = int(driver.find_element(By.CLASS_NAME, "home-score").text)
    away_score = int(driver.find_element(By.CLASS_NAME, "away-score").text)
    print(home_score, away_score)
    if home_score > away_score:
        result = "home"
    elif away_score > home_score:
        result = "away"
    else:
        result = "draw"

    game_query = """INSERT INTO games (game_id, game_name, home_id, away_id, home_score, away_score, result) 
                VALUES(?, ?, ?, ?, ?, ?, ?);
            """
    value = (game_id, game_name, home_id, away_id, home_score, away_score, result)
    try:
        c.execute(game_query, value)
    except sqlite3.IntegrityError:
        quit()
    connect.commit()
    return home, away

def add_stat(players: dict, stat: str):
    player_query = f"""SELECT player_name FROM players WHERE player_id IN (SELECT player_id FROM stats WHERE game_id = {game_id});
                    """
    player_entry = f"""INSERT INTO stats (player_id, game_id) VALUES (? , ?);"""

    
    players_in_stats = c.execute(player_query)
    players_in_stats = players_in_stats.fetchall()
    players_added = []
    for i in players_in_stats:
        for item in i:
            players_added.append(str(item).casefold())
    for player in players:
        player_id_query = f"""SELECT player_id FROM players WHERE player_name LIKE "%{player}%" AND team_id IN 
                            (SELECT team_id FROM teams WHERE team_name = '{home}' or team_name = '{away}');
                             """
        id = c.execute(player_id_query)
        player_id = id.fetchone()
        if player_id is None:
            continue
        else:
            player_id = int(player_id[0])
        if player.casefold() not in players_added and player_id not in added_ids:
                values = player_id, game_id
                c.execute(player_entry, values)
                players_added.append(player)
                added_ids.append(player_id)
        stat_entry = f"""UPDATE stats SET {stat} = {players[player]} WHERE game_id = {game_id} 
                            AND player_id = {player_id};
                    """
        c.execute(stat_entry)
    connect.commit()

def stats_to_db(driver):
    stats[stats_list[0]] = scrape_stats(driver)
    current_stat = stats[stats_list[0]]
    add_stat(current_stat, stats_list_sql[0])

    for i in range(1, len(stats_list), 1):    
        next_stat(driver, i)
        stat = stats_list_sql[i - 1]
        stats[stats_list[i - 1]] = scrape_stats(driver)
        current_stat = stats[stats_list[i - 1]]
        add_stat(current_stat, stat)
    
    stats["penalties"] = penalties
    stats["conversions"] = conversions
    add_stat(stats["penalties"], "penalties")
    add_stat(stats["conversions"], "conversions")
    
if __name__ == '__main__':

    service = Service(executable_path="C:/Users/tomho/Desktop/Projects/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    chrome_options = Options()
    chrome_options.add_argument('-ignore-certificate-errors')

    connect = sqlite3.connect('C:/Users/tomho/Desktop/Projects/player-stats.db')

    c = connect.cursor()
    URL = "https://www.rugbypass.com/premiership/fixtures-results/"
    driver.get(URL)
    stats_list = ["Carries", "Kicks", "Passes", "Metres Carried", "Line Breaks", "Offloads", "Defenders Beaten", "Try Assists", "Tries", "Turnovers Lost", "Carries Per Minute", "Tackles Made", "Tackles Missed", "Tackles Completed", "Dominant Tackles", "Turnovers Won", "Ruck Turnovers", "Lineouts Won", "Total Tackles Per Minute", "Red Cards", "Yellow Cards", "Penalties Conceded"]
    stats_list_sql = []
    for stat in stats_list:
        stats_list_sql.append(stat.lower().removeprefix("total ").replace(" ", "_"))
    
    driver.set_window_position(2000,0)
    driver.maximize_window()
    accept_privacy(driver)
    for i in range(938938, 939031, 1):
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"div[data-id='{i}']"))
        )
        driver.find_element(By.CSS_SELECTOR, f"div[data-id='{i}']").click()       
        URL = driver.current_url       
        game_id = int(URL[-6:])
        game_name = URL.removeprefix("https://www.rugbypass.com/live/").removesuffix(f"/?g={game_id}")
        stats = {}
        home, away = add_game(driver, game_id, game_name)
        penalties, conversions = pens_n_cons(driver)
        open_stats(driver)
        added_ids = []
        stats_to_db(driver)
        driver.back()
        driver.back()
    connect.close()
    driver.quit()