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
import pyautogui

creds_file = open("beatstore_credentials.txt", 'r').readlines() 

keyword_phrase = "King Von Type Beat"

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
options = Options()
options.add_argument("user-data-dir=C:\\Users\\hansu\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")
options.add_argument("profile-directory=Profile 3")
driver = Chrome(executable_path=PATH, options=options)
driver.get('https://www.traktrain.com/')
time.sleep(5)
try:
    print("Logging in...")
    login_btn = driver.find_element_by_id("profile-header-btn").click() 
    time.sleep(random.randint(3, 5)) 
    username = driver.find_element_by_xpath("//input[@placeholder='Username or Email']").send_keys(creds_file[0])
    time.sleep(wait_times[16])
    password = driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(creds_file[1])
    time.sleep(wait_times[17])
    sign_in = driver.find_element_by_xpath("//div[@class='button--color sign-in-submit']").click() 
except:
    print("Already logged in.")
    pass
time.sleep(wait_times[0])
search_bar = driver.find_element_by_xpath("//input[@placeholder='Search']")
search_bar.send_keys(keyword_phrase)
search_bar.send_keys(Keys.RETURN)


# ------------------------------------ Grab all popular tags from each search query -----------------------------------
tag_divs = driver.find_elements_by_xpath("//div[@class='tags']")
popular_tags = [tag.text for tag in tag_divs]

tag_dict = dict((x,popular_tags.count(x)) for x in set(popular_tags))

# ------------------------------------ Grab all popular titles from each search query ---------------------------------
beat_titles = driver.find_elements_by_xpath("//div[@class='title__name link--synt']")

beat_title_strings = [title.text for title in beat_titles]
total_str = " ".join(beat_title_strings)
title_word_bank = total_str.split(" ")

title_dict = dict((x,title_word_bank.count(x)) for x in set(title_word_bank))

# ------------------------------------ Grab all popular genres from each search query ---------------------------------
beat_genres = driver.find_elements_by_xpath("//div[@class='link--synt genre']") 
popular_genres = [genre.text for genre in beat_genres]

genre_dict = dict((x,popular_genres.count(x)) for x in set(popular_genres))

# -------------------------------------------------- Beat Producers: --------------------------------------------------
# For each popular producer (top results on 1st page) given a keyword phrase, keep a growing tally of the frequencies 
# of popular producers as a dict in another file. Periodically update this dict 

beat_producers = driver.find_elements_by_xpath("//div[@class='title__author link--synt']")

producer_usernames = [producer.text for producer in beat_producers]
 
from producer_logs import prod_freq_dict 

for prod in prod_usernames:
    if prod in prod_freq_dict.keys():
        prod_freq_dict[prod] += 1
    else:
        prod_freq_dict[prod] = 1

with open('producer_logs.py', 'w') as file:
    file.write("prod_freq_dict = { \n")
    for k in sorted(prod_freq_dict.keys()):
        file.write("%s:%s, \n" % (k, prod_freq_dict[k]))
    file.write("}")

# ----------------------------------------------------- Results -------------------------------------------------------

tags_sorted_popularity = sorted(tag_dict, key=tag_dict.get, reverse=True)
print("Top 3 tags: ")
print(tags_sorted_popularity[:3])

keywords_sorted_popularity = sorted(title_dict, key=title_dict.get, reverse=True)
print("Top title keywords for {}".format(keyword_phrase) + ":")
print(keywords_sorted_popularity)

genres_sorted_popularity = sorted(genre_dict, key=genre_dict.get, reverse=True)
print("Top 3 genres: ")
print(genres_sorted_popularity[:3])






