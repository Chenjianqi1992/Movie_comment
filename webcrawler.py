#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-

import re, sys, requests
from bs4 import BeautifulSoup
import psycopg2 as py2
from selenium import webdriver
from datetime import datetime

def dbwrite(movie_id, movie_name):
    web_connect = py2.connect("dbname=movie_comment user=postgres password=postgres")
    cur = web_connect.cursor()
    cur.execute("SELECT * FROM public.movie_movie_info WHERE movie_id =%s",(movie_id,))
    answer = cur.fetchall()
    if not answer:
        cur.execute("INSERT INTO public.movie_movie_info (movie_title, movie_id) VALUES (%s, %s)",(movie_name,int(movie_id)))
        web_connect.commit()
    cur.close()
    web_connect.close()

PLAYING_LIST = 'https://movie.douban.com/cinema/nowplaying/beijing/'
try:
    r = requests.get(PLAYING_LIST)
except requests.exceptions.ConnectTimeout:
    print('Time out!')
    exit()

SOUP = BeautifulSoup(r.text, 'html.parser')
MOVIE_ID_SEARCH = SOUP.find_all('div',id='nowplaying')
MOVIE_LIST = MOVIE_ID_SEARCH[0].find_all('li',class_='list-item')
ID_LIST = []
for temp in MOVIE_LIST:
    try:
        id_temp = str(temp).replace('\n', '')
        id_str = re.match(r'(.*)(data-subject=")(\d*)(" data-title=")(.*)(" data-votecount=".*)', id_temp)
        ID_LIST.append(int(id_str.group(3)))
        dbwrite(id_str.group(3), id_str.group(5))
    except:
        print ("Unexpected error:%s", sys.exc_info())
        continue
print("映画リストＯＫ")

#映画ＩＤにより、コメントの抽出する関数
def GetComment(movie_url, movie_id):

    options = webdriver.firefox.options.Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    #web_url = movie_url
    driver.get(movie_url)
    next_button = driver.find_element_by_class_name("next")

    while next_button.is_enabled():
        COM_ARRAY=[]
    
        webpage_text = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(webpage_text, 'html.parser')#BeautifulSoupツールで取得したhtmlの分析
        comments = soup.find_all('div', class_='comment')#commentクラスリストの抽出
    
        for com in comments:
            try:
                com_object = re.match(r'(<span class="short">)(.*)(</span>)', str(com.find_all('span', class_='short')[0]).replace('\n', '')).group(2)#正規表現により、不要な文字を取り除く、コメントだけ残す
                COM_ARRAY.append(com_object)
                #print(com_object)
            except AttributeError:
                com_object = ''

        if COM_ARRAY:
            db_connect = py2.connect("dbname=movie_comment user=postgres password=postgres")
            cur = db_connect.cursor()
            cur.execute("SELECT id FROM public.movie_movie_info WHERE movie_id=%s", (movie_id,))
            list_id = cur.fetchone()[0]
            for com_items in COM_ARRAY:
                cur.execute("SELECT id FROM public.movie_movie_comments WHERE comment_text =%s", (str(com_items),))
                answer = cur.fetchall()
                if not answer:
                    cur.execute(
                        "INSERT INTO public.movie_movie_comments (comment_text,agree_vote,disagree_vote, movie_info_id) VALUES (%s,0,0, %s)",
                        (str(com_items), list_id)
                        )
                    db_connect.commit()
            cur.execute("UPDATE public.movie_movie_info SET movie_update=%s WHERE id=%s", (datetime.now(), list_id))
            cur.close()
            db_connect.close()
        
        next_button.click()
        driver.get(driver.current_url)
        try:
            next_button = driver.find_element_by_class_name("next")
        except:
            break
    
    driver.quit()
    
    return 0

for items in ID_LIST:
    print(items)
    DOUBAN_URL = 'https://movie.douban.com/subject/' + str(items) + '/comments?status=P'
    com_list = GetComment(DOUBAN_URL,items)
    

print("完了")
