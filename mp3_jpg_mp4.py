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


def mp3_jpg_mp4(audio_file, image_file):
    PATH = "C:\\Program Files (x86)\\chromedriver.exe"
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\hansu\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")
    options.add_argument("profile-directory=Profile 3")
    driver = Chrome(executable_path=PATH, options=options)
    driver.get("https://www.onlineconverter.com/audio-to-video")

    time.sleep(1)
    
    base_path = "C:\\Users\\hansu\\OneDrive\\Desktop\\"
    base_beat_path = "C:\\Users\\hansu\\OneDrive\\Desktop\\beat_snip\\"
    mp3_path = base_beat_path + str(audio_file)
    jpg_path = base_path + str(image_file)
    time.sleep(1)
    insert_audio = driver.find_element_by_id("file").send_keys(mp3_path)
    time.sleep(1)
    insert_image = driver.find_element_by_id("file_1").send_keys(jpg_path)  
    time.sleep(1)
    convert = driver.find_element_by_id("convert-button").click()
    
    time.sleep(15)

    submit_button = driver.find_element_by_xpath("//*[text() = 'Download Now']")
    submit_button.click() 
    time.sleep(60)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-mp3", "--audio_file", help="Name of audio file (with file extension)")
    parser.add_argument("-jpg", "--image_file", help="Name of image file (with file extension)")
    args = parser.parse_args()
    mp3_jpg_mp4(audio_file=args.audio_file, image_file=args.image_file)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass 