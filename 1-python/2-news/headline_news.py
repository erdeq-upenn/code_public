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
    TZ_EST  = tz.gettz('America/New_York')
    TZ_CHN  = tz.gettz('zh-cn')
    now_CHN = now_utc.astimezone(TZ_CHN)
    now_EST = now_utc.astimezone(TZ_EST)
    default_date_str_CHN = str(now_CHN.strftime('%Y%m%d')) # YYYYMMDD
    default_date_str_EST = str(now_EST.strftime('%Y%m%d')) # YYYYMMDD
    bag.date_str = default_date_str_CHN
    yyyy,mm,dd = bag.date_str[:4],bag.date_str[4:6],bag.date_str[6:]
    bag.yyyy = yyyy
    bag.mm = mm
    bag.dd = dd
    bag.baseurl = 'http://paper.people.com.cn/rmrb/html/%s-%s/%s/'%(bag.yyyy,bag.mm,bag.dd)
    return bag


def request_rmrb(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_result(html):
    # pattern = re.compile(
    #     '<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">¥(.*?)</span>.*?</li>',
    #     re.S)
    pattern = re.compile(
        '<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'range': item[0],
            'image': item[1],
            'title': item[2],
            'recommend': item[3],
            'author': item[4],
            # 'times': item[5],
            # 'price': item[6]
        }


def write_item_to_file(item):
    print('开始写入数据 ====> ' + str(item))
    with open('book.json', 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

def write_raw_file(input):
    print('开始写入数据 ====> ')
    with open('raw.txt', 'a', encoding='UTF-8') as f:
        f.write(input);


def main():

    bag = getbag()
    url = bag.baseurl+'nbs.D110000renmrb_01.htm'
    res = request_rmrb(url)
    soup = BeautifulSoup(res,features="lxml");

    a_htmls = soup.find_all('a')
    # counts = soup.find_all('swiper-slide')
    # print(len(counts))
    news = []
    for i in a_htmls:
        if 'nw' in str(i):
            news.append({'title':''.join(i.contents).strip(),
                      'pageurl': bag.baseurl+i.attrs['href']}
                    )
    print(news)

    # a_htmls = soup.find_all('div')
    #
    # j = []
    # for i in a_htmls:
    #     if 'swiper-slide' in str(i):
    #         j.append(i)
    # print(len(j.content))


    # #url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    # if page == 1:
    #     url = 'http://bang.dangdang.com/books/fivestars'
    # else:
    #     url = 'http://bang.dangdang.com/books/fivestars/1-' + str(page)
    # html = request_dangdang(url);
    # # print(html)
    # items = parse_result(html)  # 解析过滤我们想要的信息
    #
    # for item in items:
    #     write_item_to_file(item)
    # write_raw_file(html)

if __name__ == "__main__":
    main()
