from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle

PATH = "C:\SeleniumDrivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('http://www.google.com')
time.sleep(60)
driver.get('http://www.cru.org/wp-admin')
time.sleep(60)

# Manually log-in here at this step and DON'T close window

# 2 minute timer, then store cookies 

cookies = driver.get_cookies()
pickle.dump(cookies, open('cookies.pkl', 'wb'))

driver.quit()