from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
import time
import json
import requests
from PIL import Image
from io import BytesIO
from tool_def import is_element_exist


DATA_SET=''
PAGE_MIN=1
PAGE_MAX=2

'''
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') #增加无界面选项
chrome_options.add_argument('--disable-gpu') #如果不加这个选项，有时定位会出现问题
'''
#作品页面查看原图需要登陆，所以使用cookie
#从文件读取cookie
with open('cookies.txt','r') as cookief:
#使用json读取cookies 
    cookieslist = json.load(cookief)
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])#开发者模式
option.add_argument('--headless')
option.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=option)
browser.get('https://www.pixivision.net/zh/c/illustration/')
page=PAGE_MIN
while page<=PAGE_MAX:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "main-column-container")))
    #time.sleep(4)
    #page_path='//a[@class="next"]'
    article_card_No=1
    while article_card_No:#循环进入插画特辑详情页面
        if article_card_No>20:#一页显示20期，此时一页循环完毕
            #结束这一页的循环
            break
        path_article_card='//ul[@class="main-column-container"]/li['
        child_path_date=']/article/div[3]/div/time'
        child_path_title=']/article/div[2]/h2/a'
        date_path=path_article_card+str(article_card_No)+child_path_date
        #匹配日期设置
        date=browser.find_element_by_xpath(date_path).text
        #当前插画特辑日期与设置的日期不匹配（前提是有设置日期）
        if date!=DATA_SET and DATA_SET!="":
            #指向下一期
            article_card_No+=1
            #直接进入下一次循环
            continue
        #显示当前插画特辑日期
        print(date,end=" ")
        title_path=path_article_card+str(article_card_No)+child_path_title
        title=browser.find_element_by_xpath(title_path).text.encode('GBK','ignore').decode('GBk')
        #显示当前插画特辑标题
        print(title,end=" ")
        child_path_tag_left=']/article/div[3]/ul/li['
        child_path_tag_right=']/a/div'
        Tag_No=1
        while Tag_No:#循环Tag种类
            tag_path=path_article_card+str(article_card_No)+child_path_tag_left+str(Tag_No)+child_path_tag_right
            if is_element_exist(tag_path,browser):#判断当前tag是否存在
                tag=browser.find_element_by_xpath(tag_path).text
                #输出tag
                print("#"+tag,end=" ")
                #指向下一个tag
                Tag_No+=1
            else:#当前tag不存在
                #结束tag循环
                break
        #进入插画特辑详情页面
        browser.get(browser.find_element_by_xpath(title_path).get_attribute("href"))
        time.sleep(3)
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "am__body")))
        work=1
        path_work_left='//div[@class="am__work gtm__illust-collection-illusts-'
        path_work_right='"]/div[2]/a'
        while work:#循环进入当前插画特辑的作品详情页面
            work_path=path_work_left+str(work)+path_work_right
            #导入cookie
            for c in cookieslist:
                browser.add_cookie(c)
            if is_element_exist(work_path,browser):
                #如果作品存在（用于判断当前插画特辑的所有作品是否都进入过）
                #跳转到作品详情页面
                browser.get(browser.find_element_by_xpath(work_path).get_attribute("href"))
                time.sleep(5)
                print("");
                #得到作品ID
                work_id=browser.current_url.split("/")[-1]
                print(work_id,end=" ")
                #分类处理不同作品页面
                if is_element_exist('//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/div[4]/div/div[2]/button',browser):#尝试寻找多图作品页的展开按钮
                    browser.find_element_by_xpath('//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/div[4]/div/div[2]/button').click()
                    time.sleep(2)
                    print("多图",end=" ")
                    pic_url=browser.find_element_by_xpath('//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[2]/div[2]/a').get_attribute("href")
                    print(pic_url)
                    
                elif is_element_exist('//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div/button',browser):
                    print("动图跳过")
                else:
                    print("单图",end=" ")
                    pic_url=browser.find_element_by_xpath('//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div/div/a').get_attribute("href")
                    print(pic_url)
                '''
                #下载图片
                r=requests.get(pic_url, headers={'referer':browser.current_url})#修改referer绕过防盗链
                image = Image.open(BytesIO(r.content))
                file_name=work_id+'.'+pic_url.split(".")[-1]
                image.save(file_name)
                print(file_name+"保存成功")
                '''
                #处理完成退出作品详情页面，回到插画特辑详情页面
                browser.back()
                #指向下一个作品详情页面
                work+=1
            else:#准备进入的作品不存在 即当前作品阅览页面已全部处理完毕
                #退出当前作品阅览页面，回到初始页面
                browser.back()
                #跳出进入作品详情的循环
                break
        #指向下一个作品阅览页面
        article_card_No+=1
        print("")
    #browser.find_element_by_xpath(page_path).click()
    #指向下一页
    page+=1
    #跳转到下一页
    browser.get('https://www.pixivision.net/zh/c/illustration/'+'?p='+str(page))

