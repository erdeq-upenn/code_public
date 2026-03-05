# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:24:47 2019

@author: Dequan Er
"""

import requests
import json 
from lxml import etree
from bs4 import BeautifulSoup


headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
data = {
	'cate':'realtimehot'
}
 
try:
	r = requests.get('http://s.weibo.com/top/summary?',params=data,headers=headers)
	print(r.url)
	if r.status_code == 200:
		html = r.text
except:
    html = ''

print(html)
    
def parseMethod(id,html):
    if id == 'bs':
        soup = BeautifulSoup(html,'lxml')
        sc = soup.find_all('script')[14].string
        start = sc.find("(")
        substr = sc[start+1:-1]
        text = json.loads(substr)#str转dict
        rxml = text["html"]#打印dict的key值,包含pid,js,css,html
        soupnew = BeautifulSoup(rxml,'lxml')
        tr = soupnew.find_all('tr',attrs={'action-type':'hover'})
    elif id == 'lxml':
        selector = etree.HTML(html)
        tt = selector.xpath('//script/text()')
#        htm = tt[8]
        htm = tt[0]
        start = htm.find("(")
        substr = htm[start+1:-1]
        text = json.loads(substr)#str转dict
        rxml = text["html"]#打印dict的key值,包含pid,js,css,html
        et = etree.HTML(rxml)
        tr = et.xpath(u'//tr[@action-type="hover"]')
    else:
        pass

    return tr

def lxmldata(tr):
	for t in tr:
		id = eval(t.find(u".//td[@class='td_01']").find(u".//em").text)
		title = t.find(u".//p[@class='star_name']").find(u".//a").text
		num = eval(t.find(u".//p[@class='star_num']").find(u".//span").text)
		yield {
		'index' : id,
		'title' : title,
		'num' : num
		}
 
def bsdata(tr):
	for t in tr:
		id = eval(t.find('em').string)
		title = t.find(class_='star_name').find('a').string
		num = eval(t.find(class_='star_num').string)
		yield {
		'index' : id,
		'title' : title,
		'num' : num
		}
 
def output(id,tr):
    with open("weibohotnews.txt","w",encoding='utf-8') as f:
        if id == 'bs':
            for i in bsdata(tr):
                f.write(str(dict(i))+'\n')
        elif id == 'lxml':
            for i in lxmldata(tr):
                f.write(str(dict(i))+'\n')
        else:
            pass
   
def main():
    url = 'http://s.weibo.com/top/summary?'
    method = 'lxml'
    html = input(url)
    tr = parseMethod(method,html)
    output(method,tr)
     
main()