#!/usr/bin/python
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
import csv
#from models.commends import Commends
#from database import db_session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from search import getTopGame
import search

 
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


    
#엑셀 파일 만들기
def scroll():
    while True:
       
        global last_height
        global soup
        global flag
        SCROLL_PAUSE_TIME = 0.5
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        # Wait to load page
        time.sleep(5)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            find_button()
            if (flag==1):
                soup = BeautifulSoup(driver.page_source, 'lxml')
                break
        
        last_height = new_height
            
        
        

        
def find_button():
        ##더보기 버튼  
        global flag
        global soup
        try:
           driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div').send_keys(Keys.ENTER) 
        except:
            flag=1
            pass
        else:
            flag=0
            scroll()

            


def crawl():
    global file
    global wr
    global pFlag
    global count
    global flag
    global page
    global soup
    global last_height
    global section ##더보기 버튼
    pFlag=1

    app_name = soup.select_one('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > c-wiz > c-wiz > div > div.D0ZKYe > div > div.sIskre > c-wiz > h1 > span')
     ##댓글 전체 block
    res = soup.select('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div > div > div > div > div > div.d15Mdf.bAhLNe') 
    for com in res:

        print("No.",count)  
        ##게임 이름
        app_name = soup.select_one('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > c-wiz > c-wiz > div > div.D0ZKYe > div > div.sIskre > c-wiz > h1 > span')
        print("[게임이름]: ", app_name.string)
        ##게임 카테고리
        app_categ = soup.select_one('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > c-wiz > c-wiz > div > div.D0ZKYe > div > div.sIskre > div.jdjqLd > div.ZVWMWc > div > span:nth-of-type(2)')
        genre = app_categ.find("a", itemprop="genre")
        print("[카테고리]: ", genre.string)   
        ##유용함
        useful = com.select_one('div.xKpxId.zc7KVe > div.YCMBp.GVFJbb > div > span > div > content > span > div')
        print("[유용함]: ", useful.string)
        ## 댓글 내용
        content = com.select_one('div.UD7Dzf > span:nth-of-type(1)')
        print("[내용]: ",content.string)
        ##댓글 작성자
        writer = com.select_one('div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > span')
        print("[작성자]: ", writer.string)
        ## 댓글 평점
        rating = com.select_one('div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > div > span.nt2C1d > div > div')
        rat = rating.find_all("div", class_='vQHuPe bUWb7c')
        length=len(rat)
        print("[평점]: ", length)   
        ##댓글 날짜
        date = com.select_one("div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > div > span.p2TkOb")
        print("[날짜]: ", date.string)
        
        ##댓글 반응
        if length > 2.5:
            response = 1 #긍정
            print("[반응]: ", response)
        else:
            response = 0 #부정
            print("[반응]: ", response)
        wr.writerow([str(count),app_name.string,genre.string,useful.string,content.string,writer.string,str(length),date.string,response])
        count+=1
    
    
    
if __name__ == "__main__":
    global count
   # gcount=gcount
    count=1
    gcount=0
    flag=0
    section=0
    last_height=0
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    pFlag=0
    index=0
    print('commend collecting crawler')
    ##써야할 URL 배열 받아오기
    gcount=getTopGame()

    for url in range(gcount):    
        url=search.reviewURL[index]
        driver.get(str(url)) ##인기 앱
        print("url: ",search.reviewURL[index])
        
        driver.implicitly_wait(3)
        file = open('ouput1.csv','w+',encoding='utf-8', newline='')
        wr=csv.writer(file)
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        scroll()
        crawl()
        index+=1
        print("댓글 전체 수: ", count)
        print(gcount)
        print(len(search.reviewURL))
    

file.close()
        
    
        
      