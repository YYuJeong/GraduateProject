# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 06:29:31 2018

@author: Bohyun
"""

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

import re
import time

driver = webdriver.Chrome(r'chromedriver.exe')
driver.get("https://play.google.com/store/apps/collection/topselling_free") ##인기 앱

reviewURL=[]

def getTopGame():  
    global reviewURL
    i=0
    gcount=0    
    driver.implicitly_wait(10)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        
        SCROLL_PAUSE_TIME = 0.5
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

        # Wait to load page
        time.sleep(5)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
                soup = BeautifulSoup(driver.page_source, 'lxml')
                break
        
        last_height = new_height
    
    links=[]
    URL=[]
    topGame=soup.select("#body-content > div > div > div.main-content > div > div > div > div.id-card-list.card-list.two-cards > div > div")
    for game in topGame:
        selectGame = game.find("a", href=True)
        links.append(selectGame.get('href'))
        newURL='https://play.google.com'+str(links[i])
        URL.append(newURL)
        i+=1
        gcount+=1
        

    
    i=0

    for i in range(gcount):  
       revURL=str(URL[i])+'&showAllReviews=true'
       reviewURL.append(revURL)
       print('count: ',i,'reviewURL: ',reviewURL[i])
    print('gcount: ',gcount)
    print('lengnth: ', len(reviewURL))
    return gcount

#getTopGame()  
    
    

