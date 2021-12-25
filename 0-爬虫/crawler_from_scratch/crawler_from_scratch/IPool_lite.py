# AUTOGENERATED! DO NOT EDIT! File to edit: 11b_ipool_lite.ipynb (unless otherwise specified).

__all__ = ['db', 'update_health', 'interval_task', 'get_progress_bar', 'show_current_progress', 'parallel_task',
           'count_good_ips', 'sites', 'https', 'match_ip', 'match_port', 'match_ip_with_port', 'parse_ips', 'save_ips',
           'crawl_ips', 'parse_protocal', 'proxy_request', 'validate_ips', 'last_modify', 'delete_ips', 'get_ip']

# Cell
import json,random,requests,re,time
from bs4 import BeautifulSoup
import concurrent.futures

from pathlib import Path

# Cell
db = {}

# Cell
def _get_ip() -> str:
    '健康值作为权重，随机抽取一个ip'
    global db
    ips = random.choices(list(db.keys()),weights=db.values(),k=1)
    return ips[0]

# Cell
def update_health(ip,is_good=False) -> int:
    '更新ip的health值，好用+1，无效/2'
    db[ip] = db[ip]*2 if is_good else db[ip]/2
#     db[ip] = db[ip]+1 if is_good else db[ip]/2
    return db[ip]

# Cell
def interval_task(fn,name,interval=300):
    '每5min自动执行fn'
    global last_modify
    if name not in last_modify or (time.time()-last_modify[name]) > interval:
        last_modify[name] = time.time()
        fn()

# Cell
def get_progress_bar(r,length=30) -> str:
    # 类似于这样的进度条'[#######                                          ]14.87%'
    current = int(length*r)
    rest = int(length*(1-r))
    return '['+'#'*current+' '*rest+'] '+str(r*100)[:5]+'%'

def show_current_progress(done_num,total_num,start_time):
    pct = done_num/total_num
    now = time.time()
    cost_time = int(now-start_time)
    left_time = int(cost_time/done_num*(total_num-done_num))
    print(f'progress:{get_progress_bar(pct)} | cost:{cost_time}s | left:{left_time}s')

# Cell
def parallel_task(fn,loop_args,max_workers=3) -> iter:
    with open('parallel_task.log','w') as f:
        f.write('')
    start_time = time.time()

    done_num = 0
    total_num = len(loop_args)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fn,arg):arg for arg in loop_args}
        for future in concurrent.futures.as_completed(futures):
            arg = futures[future]
            try:
                data = future.result()
            except Exception as exc:
                print('\n\nerror',arg,exc,'\n\n')
                with open('parallel_task.log','a') as f:
                    f.write(f'{arg}\n')
            else:
                done_num += 1
                interval_task(lambda:show_current_progress(done_num,total_num,start_time),'progress',1)
                results.append(data)

    cost_time = int(time.time()-start_time)
    print(f'{total_num} tasks, {cost_time}s')
    return results

# Cell
def count_good_ips():
    global db
    return len([k for k in db.keys() if db[k] > 100])

# Cell
sites = '''
https://www.kuaidaili.com/free/inha/
http://www.nimadaili.com/gaoni/
http://www.xiladaili.com/gaoni/
https://ip.jiangxianli.com/?anonymity=2
https://www.7yip.cn/free/
http://www.ip3366.net/free/
https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
http://proxyslist.com/
'''.strip().split('\n')

# Cell
def match_ip(tag): return re.match(r'^(\d{1,3}\.){3}\d{1,3}$',tag.text.strip())
def match_port(tag): return re.match(r'^\d{2,5}$',tag.text.strip())
def match_ip_with_port(tag): return re.match(r'^(\d{1,3}\.){3}\d{1,3}:\d{2,5}$',tag.text.strip())

def _parse_ip(soup) -> str:
    ip_with_port = soup.find(match_ip_with_port)
    ip = soup.find(match_ip)
    port = soup.find(match_port)
    if ip_with_port: return ip_with_port.text
    elif ip and port: return ip.text+':'+port.text
#     else: print('parse ip error:',soup)

def parse_ips(url) -> iter:
    res = requests.get(url,headers={'user-agent':'Mozilla/5.0'})
    soup = BeautifulSoup(res.text,features='lxml')
    tr_items = soup.body.find_all('tr')
    for tr in tr_items:
        ip = _parse_ip(tr)
        if ip: yield ip


# Cell
def save_ips(ips) -> int:
    'ips保存到db和txt中，并且返回新增ip个数'
    global db
    keys = db.keys()
    count_new = 0
    for ip in ips:
        if ip not in keys:
            db[ip] = 100
            count_new += 1
    with open('ipool.txt','w') as f:
        json.dump(db,f)
    return count_new


# Cell
def crawl_ips():
    '爬取并保存ip'
    global sites,db
    for url in sites:
        try:
            ips = list(parse_ips(url))
            count_new = save_ips(ips)
            print(url,' 新增：',count_new)
        except:
            print('error',url)
    print('总库存：',len(db.keys()))

# Cell
def parse_protocal(url): return 'https' if 'https' in url else 'http'

def _proxy_request(url,ip,method='get') -> object:
    '代理请求，并更新ip的health'
    protocal = parse_protocal(url)
    proxies = {protocal: protocal+'://'+ip}

    try:
        res = requests.request(method,url,
                               headers={'user-agent':'Mozilla/5.0'},
                               proxies=proxies,
                               allow_redirects=False,
                               timeout=5)
    except:
        update_health(ip)
#         print('except error:',ip,db[ip])
        return
    else:
        if res and res.status_code in [200,404]: update_health(ip,is_good=True)
        else: update_health(ip)
#         print(res,ip,db[ip])
        return res

# Cell
def proxy_request(url,method='get',repeat_times=10) -> object:
    '自动获取一个随机ip，不断重复请求，直到200'
    current_times = 1
    while current_times <= repeat_times:
        ip = get_ip()
        res = _proxy_request(url,ip,method)
        if res and res.status_code in [200,404]:
            print(url,'times:',current_times,res)
            return res
        else:
#             print(url,'times:',current_times,res)
            current_times += 1

# Cell
def validate_ips(url='http://www.baidu.com/',max_workers=100):
    global db
    ips = list(db.keys())
    r = parallel_task(lambda ip:_proxy_request(url, ip),ips,max_workers)
    print('good ips:',count_good_ips())

# Cell
last_modify = {}

# Cell
def delete_ips():
    '删除不健康的ip，节省内存，提高抽取效率'
    global db
    keys = list(db.keys())
    count_before = len(keys)
    for k in keys:
        if db[k] < 50: del db[k]
    count_current = len(db.keys())
    print('删除：',count_before-count_current,'剩余：',count_current)

def get_ip():
    '5min爬一次ip网站，1h删一次劣质ip'
    global db
    # 如果db为空，则尝试从txt文件读取
    if not db:
        if Path('ipool.txt').exists():
            with open('ipool.txt','r') as f:
                db = json.load(f)

    interval_task(delete_ips,'delete',interval=3600)
    interval_task(crawl_ips,'crawl')

    return _get_ip()