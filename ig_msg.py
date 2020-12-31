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

file = open('ig_creds.txt', 'r').readlines()

#from zw import users, msg_dict

login_sleep_times = [2.77, 3.57, 5.85, 7.6127, 2.055, 3.703, 4.11, 5.67, 2.3]

msg_sleep_times = [3.701, 4.107, 5.12, 6.21, 7.354, 5.901]

try_except_sleep_times = [9.67, 7.223, 11.5003]

# --------------------------------------- LOGGING INTO INSTAGRAM --------------------------------------- #

''' Randomize sleep times to confuse bot radar 
'''
sleep = random.sample(login_sleep_times, len(login_sleep_times))

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
options = Options()
options.add_argument("user-data-dir=C:\\Users\\hansu\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")
options.add_argument("profile-directory=Profile 3")
driver = Chrome(executable_path=PATH, options=options)
driver.get('https://www.instagram.com/')

time.sleep(sleep[0])
try:
    not_now_notifs = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='aOOlW   HoLwm ']"))
    ).click()
except:
    pass

time.sleep(sleep[1])

'''
driver.get("https://www.instagram.com/floodonthetrack/?hl=en")
time.sleep(sleep[0])
driver.find_element_by_xpath("//a[@class='sqdOP  L3NKy   y3zKF    ZIAjV ']").click()
time.sleep(sleep[1])
usr = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        )
usr.send_keys(file[0])
time.sleep(sleep[2])
pwd = driver.find_element_by_xpath("//input[@name='password']")
pwd.send_keys(file[1])
time.sleep(sleep[3])
pwd.send_keys(Keys.RETURN)
time.sleep(sleep[4])

# 1TAP STEPS

if driver.current_url[:42] == "https://www.instagram.com/accounts/onetap/":
    not_now = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))
        ).click()

not_now = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))
        ).click()

else:
    # 2FA STEPS 
    time.sleep(sleep[5])
    fb_usr = driver.find_element_by_xpath("//input[@name='email']")
    fb_usr.send_keys(file[0])
    time.sleep(sleep[6])
    fb_pwd = driver.find_element_by_xpath("//input[@name='pass']")
    fb_pwd.send_keys(file[1])
    fb_pwd.send_keys(Keys.RETURN)

time.sleep(sleep[7])

not_now_notifs = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='aOOlW   HoLwm ']"))
).click()
time.sleep(sleep[8])
'''

# ----------------------------------------------- MESSAGING ----------------------------------------------- #

users = []
albums = []

assert(len(users) == len(albums))

msg_sleep = random.sample(msg_sleep_times, len(msg_sleep_times))

loop_sleep = random.sample(try_except_sleep_times, len(try_except_sleep_times))

msg_dict = dict(zip(users, albums))
counter = 0
while counter < len(users):
    for user in users:
        # Search for relevant user (main search bar)
        search_bar = driver.find_element_by_xpath("//input[@placeholder='Search']")
        search_bar.send_keys(user)
        time.sleep(msg_sleep[0])
        search_bar.send_keys(Keys.RETURN)

        try:
            # Click "message" next to username
            correct_username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='uyeeR']"))
                ).click()
            time.sleep(msg_sleep[1])
            
            follow_click = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='_5f5mN       jIbKX  _6VtSN     yZn4P   ']"))
            ).click()
            time.sleep(msg_sleep[2])

            message_click = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='sqdOP  L3NKy _4pI4F   _8A5w5    ']"))
                ).click()
            time.sleep(msg_sleep[3]) 

            # Find message bar
            message_bar = driver.find_element_by_xpath("//textarea[@class='focus-visible']")
            time.sleep(msg_sleep[4])

            # Send message 
            if msg_dict[user] != 'NaN':
                msg_string = f"I've been listening to {msg_dict[user]}, really liking your music!"
            else:
                msg_string = "Really liking your music!"
            time.sleep(msg_sleep[5])
            message_bar.clear()
            message_bar.send_keys(msg_string)
            time.sleep(loop_sleep[0])
            message_bar.send_keys(Keys.RETURN)
            print("Successfully sent message to {}!".format(user))
            time.sleep(loop_sleep[1])
            counter += 1
        except:
            print("Could not send message to {}. Skipping...".format(user))
            time.sleep(loop_sleep[2])
            counter += 1
            continue 

# -------------------------------------- FORMATTING --------------------------------------- #

print(f"\nSent DMs to {counter} users.")
print("\nInstagram Daily Follow Maximum: 200")
print("\nInstagram Hourly Follow Maximum: 10")
one_hour_from_now = datetime.datetime.now() + datetime.timedelta(hours=1)
print(f"\nYou can follow {10-counter} more users until {one_hour_from_now}.")
time.sleep(2)
print("\nAdding most recent execution to followers list...")
followers_list = open("followers.txt", 'a')
followers_delineated = '\n'.join(users)
followers_list.write(followers_delineated)
followers_list.write("\n")
time.sleep(2)
print("\nSuccessfully added all followers. You can now close this window.")

