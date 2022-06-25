import data
import myPasswords as myPass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import pandas as pd

# Create log file
timestr = time.strftime("%Y%m%d-%H%M%S")
log = open(f'logs/CTA_{timestr}.txt','w')
log.write('GSuite Row,cta href\n')

# Set up driver and PATH
PATH = "C:\SeleniumDrivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)




########################################### Start loop
for i in range(len(data.clean_df)):
    # start from...
    gsuite_row = int(data.clean_df.iloc[i].name)+2
    if gsuite_row <= 263 or gsuite_row == 176: continue
    if data.clean_df.iloc[i].Staff != 'Andrew*': continue
    completed_indexs = []

    # get row data from csv
    url = data.clean_df.iloc[i].URL.strip()
    if url[0] == 'w':
        url = f'http://{url}'

    # Get webpage
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)

    # Hit CTA button
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'elementor-button-link')))
    cta_btns = driver.find_elements_by_class_name('elementor-button-link')
    if cta_btns is None: continue
    for btn in cta_btns:
        if gsuite_row in completed_indexs: continue
        completed_indexs.append(gsuite_row)

        link = btn.get_attribute('href')
        log.write(f'{gsuite_row},{link}\n')
    

##################################################### End loop

# Close log
log.close()

driver.quit()