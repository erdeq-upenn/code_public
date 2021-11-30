import collections
import re
import logging
import argparse
import requests
import json
import os
import sys
import unicodedata
import time
import pandas as pd
import inspect
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import tqdm
from bs4 import BeautifulSoup
os.environ["PYTHONDONTWRITEBYTECODE"] ="1"
os.environ["PYTHONUNBUFFERED"] = "1"
sys.path.append('/Users/dequaner/Desktop/Mirror/git/erdeq-upenn/misc/mysys')
import mybag
from dateutil import tz
from myutil import *
from myutil_dt import *
from util_jupyter import *

pd.set_option('display.max_columns',20)
pd.set_option('display.width',50)

def getbag():
    bag = MyBunch()
    bag.mask_log_str = ""
    myinit(bag)
    print_start_time(bag)

    now_utc = dt.datetime.now()
    TZ_CHN  = tz.gettz('zh-cn')
    now_CHN = now_utc.astimezone(TZ_CHN)
    default_date_str_CHN = str(now_CHN.strftime('%Y%m%d')) # YYYYMMDD
    bag.date_str = default_date_str_CHN
    yyyy,mm,dd = bag.date_str[:4],bag.date_str[4:6],bag.date_str[6:]
    bag.yyyy = yyyy
    bag.mm = mm
    bag.dd = dd
    bag.baseurl = 'https://www.thepaper.cn/'
    bag.news = []
    return bag

def myrequest(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parse_result_homepage(bag):
    # home_url = bag.baseurl

    res = myrequest(bag.baseurl)
    soup = BeautifulSoup(res,features="lxml")
    page_name= soup.find_all('h2')
    news = []
    for i in page_name:
        page_news = i.text.strip()
        newsID = hash_CH(page_news)
        page_url = bag.baseurl+i.contents[1].attrs['href']
        news.append({
                     'title':page_news,
                     'pageurl':page_url,
                     'date':bag.date_str,
                     'source':'pp',
                     'id':newsID,
                     # '_id': {'$oid': ''}
                     })
    bag.news.append(news)

def write_item_to_file(item,silent_mode=True):
    if not silent_mode:
        print('开始写入数据 ====> ' + str(item))
    else:
        with open('news.json', 'a', encoding='UTF-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n');

def write_raw_file(input):
    print('开始写入数据 ====> ')
    with open('raw.txt', 'a', encoding='UTF-8') as f:
        f.write(input);

def display(source, detail=False):
    df = pd.read_json('news.json',lines=True)
    df.drop_duplicates(inplace=True)

    if source=='rmrb':
        mask = df.page == '第01版:要闻'
        if not detail:
            print(df[mask].title)
        else:
            print(df)
    if source=='pp':
        mask = df.source == 'pp'
        print(df[mask].head(20).title)

def main():
    bag = getbag()
    parse_result_homepage(bag)
    # parse_all(bag)
    print('*'*100)
    fmt_str = '%s  年  %s  月  %s  日'%(bag.yyyy,bag.mm,bag.dd)
    print(fmt_str.center(100))
    ff_str = '加入%s条新闻'%len(bag.news[0])
    print(ff_str.center(100))
    for item in bag.news:
        for k in item:
            if len(k) != 0:
                write_item_to_file(k,silent_mode=True);
    display('pp',False)
    print('*'*100)

if __name__ == "__main__":
    main()
