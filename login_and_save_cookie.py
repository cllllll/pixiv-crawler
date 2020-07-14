from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
import json
import time
from tool_def import is_element_exist

your_email=''
your_name=''
your_password=''



option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(options=option)
browser.get('https://www.pixiv.net/')
print('load finish')
login=WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "signup-form__submit--login")))
login.click()
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "input-field")))
log_email = browser.find_element_by_xpath('//input[@autocomplete="username"]')
log_email.send_keys(your_email)
password = browser.find_element_by_xpath('//input[@autocomplete="current-password"]')
password.send_keys(your_password)
browser.find_element_by_xpath('//div[@id="LoginComponent"]/form/button').click()
time.sleep(6)
if is_element_exist('//*[@id="root"]/div[3]/div[3]/div/section/div[1]/div/h2',browser):
    #cookies = browser.get_cookies()
    print("get_good")
    with open('cookies.txt','w') as cookief:
        #将cookies保存为json格式
        cookief.write(json.dumps(browser.get_cookies()))
    print("cookie保存成功")
else:
	print("登陆失败")
    
browser.quit()
'''
bu=WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "signup-form__submit")))
browser.execute_script("arguments[0].click();",bu)
print(bu)
bu.click()
'''
