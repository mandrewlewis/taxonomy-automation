import myPasswords as myPass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle

PATH = "C:\SeleniumDrivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('http://www.cru.org/wp-admin')
time.sleep(2)

driver.find_element_by_id('okta-signin-username').send_keys(myPass.email)
driver.find_element_by_id('okta-signin-password').send_keys(myPass.password)
driver.find_element_by_xpath('//*[@id="form19"]/div[1]/div[2]/div[3]/div/span/div').click()
driver.find_element_by_id('okta-signin-submit').click()

# Catch a two-step verification and allow time for manual input
time.sleep(30)


# driver.get('http://www.cru.org/communities/campus/ucdavis')
time.sleep(5)


# e = driver.find_element_by_link_text('Sign in')
# e.click()
# time.sleep(2)

# e = driver.find_element_by_id('identifierId')
# e.send_keys('andrew.lewis@cru.org')
# e.send_keys(Keys.ENTER)
# time.sleep(2)

# e = driver.find_element_by_link_text('Next')
# e.click()
# time.sleep(2)



# driver.quit()