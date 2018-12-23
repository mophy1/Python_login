#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import time
import cv2
import numpy as np
import urllib.request as request
driver = webdriver.Firefox()
# http://gate.jd.com/InitCart.aspx?pid=4993737&pcount=1&ptype=1

# 获取图形验证的图片，并滑动滑块实现滑块验证处理
def get_image_position(flag):
    # 获取滑块图片的下载地址
    try:
        image1 = driver.find_element_by_class_name('JDJRV-smallimg').find_element_by_xpath('img').get_attribute('src')
    except BaseException:
        flag= True
        return flag
    # 获取背景大图图片的下载地址
    image2 = driver.find_element_by_class_name('JDJRV-bigimg').find_element_by_xpath('img').get_attribute('src')
    # print("image1:", image1)
    # print("image2:", image2)
    if image1 is None or image2 is None:
        return

    if driver.find_element_by_class_name('JDJRV-smallimg').is_displayed() is False:
        return

    image1_name = 'slide_block.png'  # 滑块图片名
    image2_name = 'slide_bkg.png'  # 背景大图名

    # 下载滑块图片并存储到本地
    request.urlretrieve(image1, image1_name)
    # 下载背景大图并存储到本地
    request.urlretrieve(image2, image2_name)

    # 获取图片，并灰化
    block = cv2.imread(image1_name, 0)
    template = cv2.imread(image2_name, 0)

    # 二值化之后的图片名称
    block_name = 'block.jpg'
    template_name = 'template.jpg'
    # 将二值化后的图片进行保存
    cv2.imwrite(template_name, template)
    cv2.imwrite(block_name, block)
    block = cv2.imread(block_name)
    block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
    block = abs(255 - block)
    cv2.imwrite(block_name, block)

    block = cv2.imread(block_name)
    template = cv2.imread(template_name)

    # 获取偏移量
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)  # 查找block图片在template中的匹配位置，result是一个矩阵，返回每个点的匹配结果


    x, y = np.unravel_index(result.argmax(), result.shape)

    # 获取滑块
    element = driver.find_element_by_class_name('JDJRV-slide-inner.JDJRV-slide-btn')
    # 滑动滑块
    ActionChains(driver).click_and_hold(on_element=element).perform()
    # print("x方向的偏移", int(y * 0.4 + 18), 'x:', x, 'y:', y)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=y, yoffset=0).perform()
    # sleep(1)
    ActionChains(driver).release(on_element=element).perform()
    time.sleep(3)

def login(username, password):
    driver.get("https://passport.jd.com/new/login.aspx")
    time.sleep(3)
    driver.find_element_by_link_text("账户登录").click()
    driver.find_element_by_name("loginname").send_keys(username)
    driver.find_element_by_name("nloginpwd").send_keys(password)
    driver.find_element_by_id("loginsubmit").click()
    while True:
        time.sleep(3)
        a = get_image_position(True)
        if a:
           break
    time.sleep(3)
    driver.get("https://cart.jd.com/cart.action")
    time.sleep(3)
    driver.find_element_by_id("toggle-checkboxes_down").click()
    driver.find_element_by_link_text("去结算").click()
    time.sleep(2)
    driver.find_element_by_id("order-submit").click()
    now = datetime.datetime.now()
    #now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
    print('login success, you can ou up!')

def buy_on_time(buytime):
    while True:
        now = datetime.datetime.now()
        if now.strftime('%Y-%m-%d %H:%M:%S') == buytime:
            driver.find_element_by_id('order-submit').click()
            time.sleep(3)
            print(now.strftime('%Y-%m-%d %H:%M:%S'))
            print('purchase success')
        time.sleep(0.5)

login('YourName', 'Yourpassword')
buy_on_time('2018-12-21 23:33:00')
