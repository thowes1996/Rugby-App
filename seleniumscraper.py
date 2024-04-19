from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

chrome_options = Options()
chrome_options.add_argument('-ignore-certificate-errors')


URL = "https://www.rugbypass.com/live/exeter-chiefs-vs-sale/stats/?g=939007"
driver.get(URL)
driver.set_window_position(2000,0)
driver.maximize_window()

stats_list = ["Carries", "Kicks", "Passes", "Metres Carried", "Line Breaks", "Offloads", "Defenders Beaten", "Try Assists", "Tries", "Turnovers Lost", "Carries Per Minute", "Tackles Made", "Tackles Missed", "Tackles Completed", "Dominant Tackles", "Turnovers Won", "Ruck Turnovers", "Lineouts Won", "Total Tackles Per Minute", "Red Cards", "Yellow Cards", "Penalties Conceded"]

def accept_privacy(driver = driver):
    WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.CLASS_NAME, "css-47sehv"))
    )
    driver.find_element(By.CLASS_NAME, "css-47sehv").click()

def open_stats(driver=driver):
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

def scrape_stats(driver=driver):
    stats = {}
    players = driver.find_element(By.ID, "players-selector-result").text
    p = players.split("\n")
    if p[0] == "":
        return stats
    else:      
        for i in range(0, len(p), 3):
            stats[p[i + 1]] = p[i + 2]
        return stats


def pens_n_cons(driver=driver):
    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='desktop']//a[1]//span[1]"))
        )
    driver.find_element(By.XPATH, "//div[@class='desktop']//a[1]//span[1]").click()

    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "key-event"))
        )
    key_events = driver.find_elements(By.CLASS_NAME, "key-event")
    for i in range(1, len(key_events), 1):    
        event = driver.find_element(By.XPATH, f"(//div[@class='key-event'])[{i}]")
        if event.text == "Full Time":
            continue
        name = event.find_element(By.CLASS_NAME, "name").text
        if event.find_element(By.CLASS_NAME, "icon-image.con"):
            print("conversion")
            print(name)
#     players = []
#     for event in key_events:
#         details = event.text.split("\n")  
#         players.append(details[0])
#     score = []         
#     penalties = {}
#     conversions = {}
#     i = 0
#     for event in key_events:    
#         if event.text == "Full Time" or event.text == "Half Time" or event.text == "Start":
#             continue
#         details = event.text.split("\n")
#         player = details[0]
#         if player not in penalties:
#             penalties[player] = 0
#         if player not in conversions:
#             conversions[player] = 0
#         values = details[1].split(" ")
#         if len(values) == 3:
#             value = int(values[0])
#             score.append(value)
#             if i > 0:
#                 if score[i] - score[i - 1] == -2:
#                     conversions[players[i - 1]] += 1
#                     print(conversions)
                    
#                 if score[i] - score[i - 1] == -3:
#                     penalties[players[i - 1]] += 1
#                     print(penalties)
#             print(i)
#             i += 1
            

#     if score[i - 1] == 3:
#         print(f"pen by: {players[i - 1]}")
#     if score[i - 1] == 2:
#         print(f"con by: {players[i - 1]}")

accept_privacy()
# open_stats()
# stats = scrape_stats()
# print(stats)

# for i in range(1, len(stats_list), 1):    
#     next_stat(driver, i)
#     time.sleep(1)
#     print(stats_list[i] + ":")
#     newstats = scrape_stats()
#     print(newstats)

pens_n_cons()

time.sleep(10)

driver.quit()









# WebDriverWait(driver, 2).until(
#     EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/main[1]/div[3]/div[1]/div[3]/div[1]/section[1]/div[1]/div[1]/span[1]"))
# )
# driver.find_element(By.XPATH, "/html[1]/body[1]/main[1]/div[3]/div[1]/div[3]/div[1]/section[1]/div[1]/div[1]/span[1]").click()
# WebDriverWait(driver, 2).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "list-item"))
# )
# stats = driver.find_elements(By.CLASS_NAME, "list-item")
# for stat in stats:
#     stat.click()
#     players = scrape_stats()
#     print(players)

# players = scrape_stats()
# print(players)

driver.quit()