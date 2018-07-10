#encoding=utf-8
from appium import webdriver  
  
desired_caps = {}  
desired_caps['platformName'] = 'Android'  
desired_caps['platformVersion'] = '6.0'  
desired_caps['deviceName'] = 'DWH9X17718W01627'  
desired_caps['appPackage'] = 'com.android.calculator2'  
desired_caps['appActivity'] = '.Calculator'
desired_caps['noReset'] = 'true'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)  

el1 = driver.find_element_by_accessibility_id("4")
el1.click()

el3 = driver.find_element_by_accessibility_id("5")
el3.click()
driver.quit()
