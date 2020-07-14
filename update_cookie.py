from selenium import webdriver
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
from tool_def import is_element_exist
#使用开发者模式
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(options=option)
browser.get('https://www.pixiv.net/')
#从文件读取cookie
with open('cookies.txt','r') as cookief:
    #使用json读取cookies 
    cookieslist = json.load(cookief)
#导入cookie
for c in cookieslist:
    browser.add_cookie(c)
#登入
browser.get('https://www.pixiv.net/')
#更新cookie
if is_element_exist('//*[@id="root"]/div[3]/div[3]/div/section/div[1]/div/h2',browser):
    #cookies = browser.get_cookies()
    print("get_good")
    with open('cookies.txt','w') as cookief:
        #将cookies保存为json格式
        cookief.write(json.dumps(browser.get_cookies()))
    print("cookie保存成功")
else:
	print("登陆失败")
    

