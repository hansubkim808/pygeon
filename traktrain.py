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

file = open('beatstore_credentials.txt', 'r').readlines()

def uploadTraktrain(audio, image, tag_list):

    times = [2, 5, 7, 4, 8, 3, 3, 2, 2, 3, 3, 11, 7, 6, 2, 5, 9, 2, 11, 9, 2, 9, 6, 8, 5, 8, 7, 7, 6, 3, 7, 9, 8, 5, 6, 4, 6, 5]

    wait_times = random.sample(times, 25)

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
        time.sleep(5) 
        username = driver.find_element_by_xpath("//input[@placeholder='Username or Email']").send_keys(file[0])
        time.sleep(wait_times[16])
        password = driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(file[1])
        time.sleep(wait_times[17])
        sign_in = driver.find_element_by_xpath("//div[@class='button--color sign-in-submit']").click() 
    except:
        print("Already logged in.")
        pass
    time.sleep(wait_times[0])
    profile_btn = driver.find_element_by_id("producer-profile-menu").click() 
    time.sleep(wait_times[1]) 
    upload_new_track = driver.find_element_by_xpath("//a[@class='dropdown-profile__link upload-track']").click() 
    time.sleep(wait_times[2]) 

    # ----------------------------------------- UPLOADING INFO --------------------------------------------------
    title = (str(audio)).split(",")[0]
    track_name = driver.find_element_by_id("trackname").send_keys(title)
    time.sleep(wait_times[3])
    genres = driver.find_element_by_id("genre_dropdown").click() 
    time.sleep(wait_times[4])

    trap = (driver.find_elements_by_xpath("//div[@class='dropdown__item js-filter-genres-item ng-star-inserted']"))[17].click() 
    print("Selected genres.")
    time.sleep(wait_times[5])

    exit_out_of_genres = driver.find_element_by_id("genre_dropdown").click() 
    print("Exiting out of genres...")
    time.sleep(wait_times[6])
    beats_per_minute = (str(audio)).split(",")[-1][:3]
    bpm = driver.find_element_by_xpath("//input[@placeholder='Enter BPM']").send_keys(beats_per_minute)
    print("Inputted BPM.")
    time.sleep(wait_times[7])

    # --------------------------------------------------------- TAGS -------------------------------------------------------------

    beat_tags = (str(tag_list)).split(",")
    tags = driver.find_element_by_xpath("/html/body/main/div/div/div/section/app-root/app-step1/div/form/div/div[2]/dl[3]/dd/tag-input/div/div/tag-input-form/form/input")
    tags.click() 
    time.sleep(wait_times[8])
    for tag in beat_tags:
        tags.send_keys(tag)
        time.sleep(wait_times[9])
        tags.send_keys(Keys.RETURN)
        time.sleep(wait_times[10])
    print("Inputted tags successfully.")

    # ----------------------------------------------------- IMAGE UPLOAD---------------------------------------------------------

    full_img_url = "C:\\Users\\hansu\\OneDrive\\Desktop\\" + str(image)
    time.sleep(wait_times[11])
    driver.find_element_by_id("upload-image").send_keys(full_img_url)
    time.sleep(wait_times[12])
    apply_changes = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='button--color']"))).click()
    print("Successfully uploaded image.") 

    # ------------------------------------------------------------------------------------------------------------------------

    time.sleep(wait_times[13])

    mp3_price = driver.find_element_by_id("rights-mp3-lease").send_keys("39.95")
    print("Inputted mp3 price.")
    time.sleep(wait_times[14])

    full_mp3_url = "C:\\Users\\hansu\\OneDrive\\Desktop\\beat_snip\\" + str(audio)
    upload_mp3 = driver.find_element_by_id("mp3Upload").send_keys(full_mp3_url)
    time.sleep(wait_times[15])
    print("Succesfully uploaded .mp3 file.")
    time.sleep(10)
    publish = driver.find_element_by_xpath("/html/body/main/div/div/div/section/app-root/div/button").click() 
    time.sleep(5)
    print("Successfully published beat!")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--audio_file")
    parser.add_argument("-i", "--image_file")
    parser.add_argument("-t", "--tags")
    args = parser.parse_args()
    uploadTraktrain(audio=args.audio_file, image=args.image_file, tag_list=args.tags)

'''
audio_file: just the raw .mp3 name (NOT the full path name). String parsing logic included to append full file base url onto file name.

audio_file format example: "DIRTY SPRITE - D minor,90 bpm.mp3"

image_file: just the raw .jpg or .png name (NOT the full path name).

tags: comma-delimited list of tags. 

'''

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass 