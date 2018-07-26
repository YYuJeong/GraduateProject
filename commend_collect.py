# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:21:03 2018

@author: Bohyun
"""
##메소드 바로 사용하기 위해서 from~ import * 사용
import requests as rq
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs

from config.URL_config import TOP_URL, LOGIN_URL, BASE_URL
from config.ACCOUNT_config import EMAIL, PASSWORD

#from models.commends import Commends
#from database import db_session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import re
import time

# HTTP GET Request
#req = rq.get('https://play.google.com/store/apps/details?id=com.ludia.jurassicworld')
# HTML 소스 가져오기
#html = req.text
# BeautifulSoup 으로 html 소스를 python 객체로 변환하기
#soup = BeautifulSoup(html, 'html.parser')

##파이썬은 인터프리터 명령어로 패싱되어 실행되어서  자동으로 실행되는 메인함수가 없다
##__name__: 현재 모듈의 이름을 담고있는 내장 변수 -> testweb.py같이 이 모듈이 직접 실행되는 경우에만 __name__ 이 __main__으로 실행 

driver = webdriver.Chrome(r'chromedriver.exe')
driver.get("https://play.google.com/store/apps/details?id=com.ludia.jurassicworld&showAllReviews=true")

#Get Scroll height
last_height=driver.execute_script("return document.body.scrollHeight")
out = open('data.txt','w',encoding='UTF8')


if __name__ == "__main__":
    print('commend collecting crawler')

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    app_name = soup.select_one('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > c-wiz > c-wiz > div > div.D0ZKYe > div > div.sIskre > c-wiz > h1 > span')
   
    print("게임이름: ", app_name.string)
    out.write("게임이름: "+ app_name.string)

    
    count=0
    
    SCROLL_PAUSE_TIME = 0.5
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    soup = BeautifulSoup(driver.page_source, 'lxml')

    
    
     ##댓글 전체 block
    res = soup.select('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div > div:nth-of-type(2) > div > div > div > div.d15Mdf.bAhLNe') 
    for com in res:
        print("No.",count)
        ## 댓글 내용
        content = com.select_one('div.UD7Dzf > span:nth-of-type(1)')
        print("[내용]: ",content.string)
        ##댓글 작성자
        writer = com.select_one('div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > span')
        print("[작성자]: ", writer.string)
        sum=0
        ## 댓글 평점
        rating = com.select_one('div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > div > span.nt2C1d > div > div')
        rat = rating.find_all("div", class_='vQHuPe bUWb7c')
        length=len(rat)

        print("[평점]: ", length)
        
        ##댓글 날짜
        date = com.select_one("div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > div > span.p2TkOb")
        print("[날짜]: ", date.string)
        count+=1
        
        
        
        
    print("댓글 전체 수: ", count)



        