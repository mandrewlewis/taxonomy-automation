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
log = open(f'logs/{timestr}.txt','w')
log.write('This is a test')
finished_rows = []

# Set up driver and PATH
PATH = "C:\SeleniumDrivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Initiate driver and start log-in process
driver.get('http://www.cru.org/wp-admin')
driver.maximize_window()

# Send log-in credentials
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'okta-signin-username'))).send_keys(myPass.email)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'okta-signin-password'))).send_keys(myPass.password)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form19"]/div[1]/div[2]/div[3]/div/span/div'))).click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'okta-signin-submit'))).click()

# Catch a two-step verification and allow time for manual input
time.sleep(10)

########################################### Start loop
for i in range(len(data.clean_df)):
    # start from...
    gsuite_row = int(data.clean_df.iloc[i].name)+2
    if gsuite_row < 0: continue

    # get row data from csv
    url = data.clean_df.iloc[i].URL.strip()
    if url[0] == 'w':
        url = f'http://{url}'

    log.write(f'\n\n\nStarting GSuite row: {gsuite_row}\n')
    log.write(f'URL = {url}\n')

    tag_sets = []
    for set in data.clean_df.iloc[i].Tags.split(','):
        tag_sets.append(set.strip())

    log.write(f'Tags = {tag_sets}\n')


    # Get webpage
    driver.get(url)
    log.write('...requested url\n')

    # Hit edit on wp-toolbar
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'wp-admin-bar-edit'))).click()
    log.write('...click edit\n')

    ########Apperance editing#########
    # Hover apperance and click customize
    hover_e = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-appearance"]/a/div[3]')))
    time.sleep(1)
    action = ActionChains(driver)
    action.move_to_element(hover_e).perform()
    sub_e = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-appearance"]/ul/li[3]/a')))
    sub_e.click()
    log.write('...hover/click apperance/customize\n')

    # Click site identity
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="accordion-section-title_tagline"]/h3'))).click()
    log.write('...click site identity\n')

    # Click diable giving checkbox
    # Need to check if giving link box is empty first
    giving_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, '_customize-input-cru_giving_link')))
    if giving_link.get_attribute('value') == '':
        check_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, '_customize-input-cru_giving_link_disable')))
        if check_box.is_selected():
            log.write('...disable give link already selected\n')
        else:
            check_box.click()
            log.write('...click disable give link\n')
    else:
        log.write('    ***page is using giving link\n')


    # Check tagline
    tagline = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, '_customize-input-blogdescription')))
    if tagline.get_attribute('value') == '' or tagline.get_attribute('value') == 'Just another WordPress site':
        tagline.clear()
        tagline.send_keys('Helping you take your next step toward Jesus')
        log.write('   ***missing/bad tagline updated\n')

    # Click publish
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'save'))).click()
    log.write('...click publish\n')
    time.sleep(5) #let publish button finish

    # Click [x]
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="customize-header-actions"]/a'))).click()
    log.write('...click exit button\n')

    #######Back to main edit page#######
    # Check excerpt
    excerpt = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'excerpt')))
    if excerpt.get_attribute('value') == '':
        excerpt.send_keys('Find Christian community at your school.')
        log.write('   ***missing excerpt added\n')

    # Click Taxonomy [Add] (n-1 times)
    add_tag_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wtgm_aem-tagdiv"]/div[1]/h2/a')))
    for i in range(len(tag_sets)-1):
        add_tag_btn.click()
        log.write('...click add & create extra tag group\n')

    # tag_sets = ['ministry/us','target/students/undergrad','location/americas/us/california']

    for set_index, set in enumerate(tag_sets):
        for tag_index, tag in enumerate(set.split('/')):
            tag_text = tag
            if tag_text == 'Geographies Custom': tag_text = 'Geographies, Custom'
            dropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="wtgm_aem-tagdiv"]/div[2]/div/table/tbody/tr[{set_index+1}]/td[{tag_index+1}]/select')))
            Select(dropdown).select_by_visible_text(tag_text)
            log.write(f'...add tag [{set_index}][{tag_index}]{tag}\n')

    log.write(f'...DONE tagging\n')

    # Click save
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'publish'))).click()
    # log.write('...SAVED\n')
    time.sleep(10)

    log.write(f'FINISHED PAGE - no errors\n')
    finished_rows.append(int(data.clean_df.iloc[1].name)+2)

##################################################### End loop

# Close log
log.write('\n\n\n\nFinished Rows:\n')
for x in finished_rows:
    log.write(f'{x}\n')
log.close()

driver.quit()