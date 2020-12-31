from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located
import time 
import datetime
import random 
import pandas as pd
import pyautogui
import itertools

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
options = Options()
options.add_argument("user-data-dir=C:\\Users\\hansu\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")
options.add_argument("profile-directory=Profile 3")
driver = Chrome(executable_path=PATH, options=options)
driver.get("https://youtube.com")

create = driver.find_element_by_xpath("//button[@aria-label='Create']").click()
upload_video = driver.find_element_by_xpath("//a[@href='/upload']")
upload_video.click() 

select_files = driver.find_element_by_xpath("//ytcp-button[@id='select-files-button']").click()
time.sleep(random.randint(2, 4))
pyautogui.write("C:\\Users\\hansu\\Downloads\\BLESSING-Snippet.mp4")
pyautogui.press("enter")
time.sleep(random.randint(5, 10))

tubebuddy = driver.find_element_by_xpath("//div[@id='tb-upload-studio-menu-dropdown-button']").click() 
create_new_optimization = driver.find_element_by_xpath("//a[@id='tb-upload-studio-new-optimization']").click() 
time.sleep(random.randint(1, 3))
target_keyword = driver.find_element_by_xpath("//input[@placeholder='Enter your Target Keyword']")
keyword_explorer = driver.find_element_by_xpath("//a[@class='tb-seo-studio-step-1-option']").click() 
time.sleep(random.randint(1, 3))
launch_keyword_explorer = driver.find_element_by_xpath("//button[@class='tb-btn tb-btn-blue tb-width250']").click() 

keyword_search_bar = driver.find_element_by_xpath("//input[@id='tb-tag-explorer-input']")

melodic_rap_dict = {}

melodic_rap_dict['acoustic_melodic_producers_tier1'] = ['Tntxd', 'Drumdummie', 'TahjMoneyy', 'Zaytoven', 'JTK', 'DubbaAA']

melodic_rap_dict['acoustic_melodic_producers_tier2'] = ['BjBeatz, SephgottheWaves', 'Mookgotthekeysjumpin', 'TNK a Monstah', 
                                                        'DJ Ayo', 'Pooh Beatz', 'TouchOfTrent', 'Prod by Dmac', 'Plutobrazy', 'Yung Lando']

melodic_rappers_south = ['Rod Wave', 'NBA YoungBoy', 'Lil Poppa', 'Slatt Zy', 'Polo G', 'OMB Peezy', 'Yungeen Ace', 'BBG Baby Joe', 
                         'FG Famous', 'Lil Tjay', 'Roddy Ricch', 'Quando Rondo', 'JayDaYoungan', 'Lil Zay Osama', 'GBF King', 
                         'Lil Durk', 'Dooley Da Don', 'Jackboy', 'Lil Polo Da Don', 'NoCap', 'Rylo Rodriguez', 'Seddy Hendrinx', 
                         'OBN Jay', 'Bway Yungy', 'Lil Loaded', 'YFN Lucci', 'Yung Bleu', 'Derez DeShon', 'Project Youngin', 'TEC', 
                         'YNW Melly', 'JayO Sama', 'Hotboii', 'DaDa1k', 'Luh Soldier', 'YK Toon', 'Soldier Kidd', 'T9ine', 'Foolio', 
                         'Y&R Mookey', 'Jdot Breezy', 'Ksoo', 'BigKayBeezy', 'Maine Musik', 'Toosii', 'Kevin Gates', 'NWM Cee Murdaa']

melodic_rap_dict['acoustic_melodic_rappers'] = list(itertools.combinations(melodic_rappers_south, 2))


# Create different keyword banks depending on geographic region + instrumentation  
# Eg.) "south, piano" = [tntxd, drumdummie, rod wave, slatt zy, ... , etc] 
# Eventually substitute this hard coded association dictionary with an NLP algorithm 

keyword_score_list = [" ", 0]

producer = random.choice(melodic_rap_dict['acoustic_melodic_producers_tier1'])

max_score = 0

for elem in melodic_rap_dict['acoustic_melodic_rappers']:
    kstr_1 = elem[0] + " x " + elem[1] + " x " + producer + " Type Beat"
    kstr_2 = elem[0] + " x " + producer + " x " + elem[1] + " Type Beat"
    kstr_3 = elem[1] + " x " + elem[0] + " x " + producer + " Type Beat"
    kstr_4 = elem[1] + " x " + producer + " x " + elem[0] + " Type Beat"
    keyword_string = random.choice([kstr_1, kstr_2, kstr_3, kstr_4])
    keyword_search_bar.clear() 
    keyword_search_bar.send_keys(keyword_string) 
    keyword_search_bar.send_keys(Keys.RETURN)
    time.sleep(random.randint(1, 3))
    seo_score = int((driver.find_element_by_xpath("//span[@id='tb-tag-explorer-total-score']").text).split("/")[0])
    if seo_score > max_score: 
        max_score = seo_score
        keyword_score_list[0] = keyword_string
        keyword_score_list[1] = max_score
    



