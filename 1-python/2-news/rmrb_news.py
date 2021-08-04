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
sys.path.append('~/Desktop/misc/mysys')
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
    bag.baseurl = 'http://paper.people.com.cn/rmrb/html/%s-%s/%s/'%(bag.yyyy,bag.mm,bag.dd)
    bag.news = []
    return bag

def request_rmrb(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parse_result(url,bag):
    mode = 'Headline'
    res = request_rmrb(url)
    soup = BeautifulSoup(res,features="lxml")
    # bag.homepage_soup = soup
    page_name= soup.find('p',attrs={'class':'left ban'}).contents[0]
    print(page_name)
    if mode == 'Headline':
        a_htmls = soup.find_all('a')
        news = []
        for i in a_htmls:
            try:
                if 'nw' in str(i):
                    title = ''.join(i.contents).strip()
                    id = hash_CH(title+page_name)
                    news.append({
                                 'title':title,
                                 'pageurl': bag.baseurl+i.attrs['href'],
                                 'date':bag.date_str,
                                 'page':page_name,
                                 'source':'rmrb',
                                 'id':id,
                                 })
            except:
                print('No headlines, skip...')

        bag.news.append(news)
        # bag.home_page = res
    return bag

def parse_result_homepage(bag):
    home_url = bag.baseurl+'nbs.D110000renmrb_01.htm'
    # parse_out home page headlines
    parse_result(home_url,bag)
    res = request_rmrb(home_url)
    soup = BeautifulSoup(res,features="lxml")
    bag.homepage_soup = soup

    # parse out other pages, uri
    other_pages = []
    pages = soup.find_all('a',attrs={'id':'pageLink'})
    for item in pages[1:]:
        other_pages.append({'page':item.contents[0],
                            'pageUri':item.attrs['href']})
    bag.other_pages = other_pages

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

def parse_all(bag):
    print(len(bag.other_pages),print('*'*10))
    for uri in bag.other_pages:
        page_url_to_parse = bag.baseurl+uri['pageUri']
        print(page_url_to_parse)
        parse_result(page_url_to_parse,bag)

def display(detail=False):
    df = pd.read_json('news.json',lines=True)
    mask = df.page == '第01版:要闻'
    if not detail:
        print(df[mask].title)
    else:
        print(df)


def main():
    bag = getbag()
    parse_result_homepage(bag)
    parse_all(bag)
    print('*'*100)
    fmt_str = '%s  年  %s  月  %s  日'%(bag.yyyy,bag.mm,bag.dd)
    print(fmt_str.center(100))
    for item in bag.news:
        for k in item:
            if len(k) != 0:
                write_item_to_file(k,silent_mode=True);
    display(False)
    print('*'*100)

if __name__ == "__main__":
    main()
