import random
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sys
import time
import requests

audioToTextDelay = 10
delayTime = 2
url1 = "https://cdn.discordapp.com/attachments/811871558138200075/911082266812370944/1.txt"
url2 = 'https://cdn.discordapp.com/attachments/811871558138200075/911084580214284298/2.txt'
audioFile = "\\payload.mp3"
URL = "https://minecraft-mp.com/server/295107/vote?alternate_captcha=2"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"
name1 = requests.get(url1).text
name2 = requests.get(url2).text
names1 = random.choice(name1.split())
names2 = random.choice(name2.split())

nickname = names1+names2

def delay():
    time.sleep(random.randint(7,9))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result


try:
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    delay()
    # go to website which have recaptcha protection
    driver.get(URL)
    delay()
    driver.save_screenshot("sss.png")
except Exception as e:
   print("[INFO!] Minecraft NickName = "+nickname)

g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
outerIframe.click()

xapt = driver.find_element_by_name("accept")
xapt.click()
nicknames = driver.find_element_by_name("nickname")
nicknames.send_keys(nickname)
nicknames.send_keys(Keys.ENTER)
delay()
iframes = driver.find_elements_by_tag_name('iframe')
driver.save_screenshot("70.png")
print("[INFO!] Minecraft NickName = "+nickname)
audioBtnFound = False
audioBtnIndex = -1

for index in range(len(iframes)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_tag_name('iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element_by_id("recaptcha-audio-button")
        audioBtn.click()
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass

if audioBtnFound:
    while True:
            # get the mp3 audio fil
            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print("[INFO] Audio src: %s" % src)

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech To Text Conversion
            key = audioToText(os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key: %s" % key)

            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)

            # key in results and submit
            inputField = driver.find_element_by_id("audio-response")
            inputField.send_keys(key)
            time.sleep(1)
            inputField.send_keys(Keys.ENTER)
            time.sleep(1)
            driver.save_screenshot("ss.png")
            time.sleep(3)

            err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
            if err.text == "" or err.value_of_css_property('display') == 'none':
                print("[INFO] Success!")
                break
else:
    sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
