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

creds_file = open("ig_creds.txt", "r").readlines()

# -------------------------------------------------- OPEN SELENIUM -------------------------------------------------------
PATH = "C:\\Program Files (x86)\\chromedriver.exe"
#options = Options()
#options.add_argument("user-data-dir=C:\\Users\\xxxxxxxxxxxxxxxxx")
#options.add_argument("profile-directory=Profile 3")
#driver = Chrome(executable_path=PATH, options=options)

driver = Chrome(executable_path=PATH)

driver.get("https://www.instagram.com/xxxxxxxxx/?hl=en")
time.sleep(random.randint(5, 8))
driver.find_element_by_xpath("//a[@class='sqdOP  L3NKy   y3zKF    ZIAjV ']").click()
time.sleep(2)
usr = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        )
usr.send_keys(creds_file[0])
time.sleep(random.randint(5, 8))
pwd = driver.find_element_by_xpath("//input[@name='password']")
pwd.send_keys(creds_file[1])
time.sleep(random.randint(5, 8))
pwd.send_keys(Keys.RETURN)
time.sleep(random.randint(5, 8))

# 1TAP STEPS
'''
if driver.current_url[:42] == "https://www.instagram.com/accounts/onetap/":
    not_now = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))
        ).click()
'''
not_now = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))
        ).click()
'''
else:
    # 2FA STEPS 
    time.sleep(random.randint(5, 8))
    fb_usr = driver.find_element_by_xpath("//input[@name='email']")
    fb_usr.send_keys(creds_file[0])
    time.sleep(random.randint(5, 8))
    fb_pwd = driver.find_element_by_xpath("//input[@name='pass']")
    fb_pwd.send_keys(creds_file[1])
    fb_pwd.send_keys(Keys.RETURN)
'''
time.sleep(random.randint(5, 8))

not_now_notifs = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='aOOlW   HoLwm ']"))
).click()
time.sleep(random.randint(5, 8))


# -------------------------------------------------- FIND ALL FOLLOWERS --------------------------------------------------
user = '{user}'
driver.get(f'https://www.instagram.com/{user}')
user_following_href = f'/{user}/following/'


people_they_follow = driver.find_element_by_xpath("//a[@href='{}']".format(user_following_href))
people_they_follow.click() 
num_following = int(people_they_follow.text[:3])//12
time.sleep(random.randint(2, 4))


fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
scrolling_times=(num_following//4)
scroll = 0
counter = 0
list_of_following = []
scroll_count = scrolling_times+5 
while scroll < scroll_count:
    if counter % 2 == 0:
        followers_list = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate  _0imsa ']")[(6*counter):]
        for i in range(len(followers_list)):
            list_of_following.append(followers_list[i].text)
    driver.execute_script(
        'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
        fBody)
    time.sleep(random.randint(3, 6))
    scroll += 1
    counter += 1
time.sleep(random.randint(2, 5))
driver.get(f'https://www.instagram.com/{user}')

# --------------------------------------------------- PANDAS SKELETON ---------------------------------------------------
df = pd.DataFrame(columns=['Artist IG', 'Followers', 'Following', 'Bio'])
title = f'{user} Artist Network Analysis'
df.style.set_caption(title)

# -------------------------------------------------- PARSE BIO & LINKS --------------------------------------------------

rapper_keywords = ['music.empi.re', 'youtube.com', 'linktr.ee', 'soundcloud', 'mymixtapez', 'audiomack', 'spinrilla', 
                   'music.apple.com', 'apple music', 'spotify', 'tidal', 'spnr.la', 'unitedmasters.com', 'li.sten.to', 
                   'manylink.co', 'smarturl.it', 'youtube', 'bookings', 'features', 'features/bookings', 'rapper', 
                   'artist', 'musician', 'musician/band', 'out now', 'youtu.be']

print("Making dataframe now...")
time.sleep(random.randint(2, 5))
for ig_username in list(set(list_of_following))[:10]:
    search_bar = driver.find_element_by_xpath("//input[@placeholder='Search']")
    search_bar.clear()
    search_bar.send_keys(ig_username)
    time.sleep(random.randint(3, 7))
    search_bar.send_keys(Keys.RETURN)
    time.sleep(random.randint(2, 5))
    try:
        click_on_name_search = driver.find_element_by_xpath("//a[@class='yCE8d  JvDyy']")
        href = f'/{ig_username}/'
        click_on_name_search.click()
    except:
        pass
    time.sleep(random.randint(3, 7))
    try:
        # Number of followers/following 
        followers_href = f'/{ig_username}/followers/'
        #followers = int(driver.find_element_by_xpath("//a[@href='{}']".format(followers_href)).text)
        followers = driver.find_element_by_xpath("//a[@href='{}']".format(followers_href)) 
        print("Found followers")
        '''
        if followers > 7500:
            continue 
        else: 
            following_href = f'/{ig_username}/following/'
            following = int(driver.find_element_by_xpath("//a[@href='{}']".format(following_href)).text)
        '''
        following_href = f'/{ig_username}/following/'
        #following = int(driver.find_element_by_xpath("//a[@href='{}']".format(following_href)).text)
        following = driver.find_element_by_xpath("//a[@href='{}']".format(following_href))
        print("Found following")
        # Parse bio as text 
        '''
            bio = driver.find_element_by_xpath("//div[@class='-vDIg']").text
            if any(keyword in bio for keyword in rapper_keywords):
                df = df.append(pd.DataFrame([[ig_username, followers, following, bio]], 
                                    columns=['Artist IG', 'Followers', 'Following', 'Bio']), ignore_index=True)
            else:
                continue 
        '''
        bio = driver.find_element_by_xpath("//div[@class='-vDIg']").text
        print("Found Bio")
        if any(keyword in bio for keyword in rapper_keywords):
            df = df.append(pd.DataFrame([[ig_username, followers.text, following.text, bio]], 
                                columns=['Artist IG', 'Followers', 'Following', 'Bio']), ignore_index=True)
            print("Made df row.")
        else:
            print("Could not make df row from this user. Continuing...")
            pass 

    except:
        continue 

print(df)









