from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException
import sqlite3

service = Service(executable_path="C:/Users/tomho/Desktop/Projects/chromedriver.exe")
driver = webdriver.Chrome(service=service)
chrome_options = Options()
chrome_options.add_argument('-ignore-certificate-errors')

URL = "https://www.all.rugby/transfers/premiership-2023"

driver.get(URL)

def accept_privacy(driver):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='sd-cmp']/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]"))
    )
    driver.find_element(By.XPATH, "//*[@id='sd-cmp']/div[2]/div/div/div/div/div/div/div[2]/div[2]/button[2]").click()

def add_player(name: str, pos: str, team: str, i: int):
    player_query = f"""SELECT player_name FROM players WHERE player_name LIKE "%{name}%" AND team_id IN 
                            (SELECT team_id FROM teams WHERE team_name = '{team}');
                             """
    row = c.execute(player_query)
    player_name = row.fetchone()
    if player_name is None:      
        player_add = f"""INSERT INTO players (player_name, position, team_id)
                            VALUES (?, ?, ?);
                        """
        values = (name, pos, (i + 1))
        c.execute(player_add, values)
        print(name)
        print(pos)
        print("added")
    else:
        player_name_found = str(player_name[0])
        print(name)
        print(pos)
        print("found")
        
    # if name.casefold() == player_name_found.casefold():
    #     return
    # else:

    #     return
    
    




if __name__ == '__main__':
    driver.set_window_position(2000, 0)
    driver.maximize_window()
    connect = sqlite3.connect('C:/Users/tomho/Desktop/Projects/player-stats.db')
    c = connect.cursor()
    accept_privacy(driver)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mutations"))
    )
    transfers = driver.find_elements(By.CLASS_NAME, "mutations")
    prem_teams = ['bath', 'bristol', 'exeter-chiefs', 'gloucester', 'harlequins', 'leicester', 'newcastle', 'northampton', 'sale', 'saracens']
    i = 0
    counter = 0
    for transfer in transfers:
        pro_transfers = transfer.text.replace("Players IN", "").replace("Academy", "").replace("Players OUT", "").replace("Gone during season", "").replace("Pro\n", "")
        pro_transfers = pro_transfers.split("\n")
        print(f"***\n{prem_teams[i]}\n***")
        for player in pro_transfers:
            if player == '':
                continue
            player = player.split(",")
            position = player[1].strip().replace("-", " ").title()
            player_name = player[0].lower().title().replace("(1)", "").replace("(*)", "")
            # print(player_name)
            # print(position)
            add_player(player_name, position, prem_teams[i], i)        
        counter += 1
        if counter == 2:
            counter = 0
            i += 1
        connect.commit()
    connect.close()
    