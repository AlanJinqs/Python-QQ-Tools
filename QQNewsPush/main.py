#! python3
# coding: utf-8
from qqbot import QQBot

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import chardet
groupnum = "这里写群号"
# 使用selenium
driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
#driver = webdriver.PhantomJS(executable_path="/root/qqbot/phantomjs")
driver.maximize_window()
myqqbot = QQBot()

@myqqbot.On('qqmessage')
# 登录QQ空间
def get_shuoshuo(qq):
    global num1
    global time1
    driver.refresh()
    time.sleep(5)
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False

    driver.implicitly_wait(3)
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        content = driver.find_elements_by_css_selector('.content')
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for con, sti in zip(content, stime):
            if num1 == 0:
                if time1 == sti.text:
                    pass
                    num1 = 1
                else:
                    time1 = sti.text
                    myqqbot.Send('group', groupnum, con.text)
                    print(con.text)
                    pages = driver.page_source
                    soup = BeautifulSoup(pages, 'lxml')
                    num1 = 1




myqqbot.Login()
time1 = "1999-99-99"
qq = '2159195672'
driver.set_page_load_timeout(300)
driver.get('http://user.qzone.qq.com/' + qq + '/311')
time.sleep(10)
driver.set_window_size(1280,800)
savepath = r'qzone.jpg'

driver.save_screenshot(savepath)
print("[INFO]请打开程序目录下“qzone.jpg”并扫描二维码")
while 1 == 1:
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        print("[INFO]检测到登录！读取网页中")
        time.sleep(10)
        break
    except:
        print("[INFO]未检测到登录")
        time.sleep(1)
@myqqbot.On('qqmessage')
def handler(bot, message):
    if message.content == '-stop':
        bot.SendTo(message.contact, 'biu~')
        print(message.contact)
        bot.Stop()
while 1 == 1:
    num1 = 0
    get_shuoshuo(qq)
    time.sleep(300)
        #driver.close()
        #driver.quit()

