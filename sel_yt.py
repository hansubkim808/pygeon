from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located
import time 

PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"

creds = open('zebra.txt', 'r').readlines()
#options = Options()
#options.add_argument("user-data-dir=C:\\Users\\hansu\\AppData\\Local\\Google\\Chrome\\User Data")
#options.add_argument("profile-directory=Profile 1")

# --------------------------------------- LOGGING INTO INSTAGRAM --------------------------------------- #
driver = Chrome(executable_path=PATH)
driver.get("https://www.instagram.com/1djayo/?hl=en")
time.sleep(3)
driver.find_element_by_xpath("//a[@class='sqdOP  L3NKy   y3zKF    ZIAjV ']").click()
time.sleep(1)
usr = driver.find_element_by_xpath("//input[@name='username']")
usr.send_keys(creds[0])
time.sleep(1)
pwd = driver.find_element_by_xpath("//input[@name='password']")
pwd.send_keys(creds[1])
time.sleep(1)
pwd.send_keys(Keys.RETURN)
time.sleep(3)

# 1TAP STEPS
if driver.current_url[:42] == "https://www.instagram.com/accounts/onetap/":
    not_now = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='sqdOP yWX7d    y3zKF     ']"))
        ).click()

else:
    # 2FA STEPS 
    time.sleep(3)
    fb_usr = driver.find_element_by_xpath("//input[@name='email']")
    fb_usr.send_keys(creds[2])
    fb_pwd = driver.find_element_by_xpath("//input[@name='pass']")
    fb_pwd.send_keys(creds[3])
    fb_pwd.send_keys(Keys.RETURN)

time.sleep(3)

not_now_notifs = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='aOOlW   HoLwm ']"))
).click()
