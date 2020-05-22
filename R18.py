import os
import re
import urllib.request
import js2py
import requests
from lxml import etree
from clint.textui import progress
import fire
from loguru import logger
import time
from progressbar import *

from multiprocessing.dummy import Pool as ThreadPool


headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Cookie':
        '__cfduid=d13360120e854bc15674abedf40f2abcf1590034953; country=us; currencies=%7B%22JPY%22%3A%221%22%2C%22USD%22%3A%220.009289%22%2C%22EUR%22%3A%220.008465%22%2C%22GBP%22%3A%220.007597%22%2C%22AUD%22%3A%220.014099%22%2C%22CAD%22%3A%220.012924%22%2C%22SGD%22%3A%220.013136%22%2C%22TWD%22%3A%220.277803%22%2C%22CNY%22%3A%220.065827%22%2C%22HKD%22%3A%220.07187%22%2C%22NZD%22%3A%220.015121%22%2C%22CHF%22%3A%220.008968%22%7D; rtt=bCEzmdwqL9jrDJQu%2BGkidr7KzU3AndLlKDQLu5S81bupQVnoZFmXqjVFl9%2FG%2Bb8NcLlqfryk12K8i339b1X3rBJsZBPs7dfPJodlOgIKVE5%2Fopl%2BTMlWbydlg3soF%2Ffy7MQEl7Poz87rTVma%2FFgE%2FaXCf0W7de2k4hkeaFvw3l96jCgmtsU5laLakwHgvHCoiYVXvSCQDTGrXj5Np%2FQdyHOdXic%3D; lg=zh; ab=a; ex=USD; gid=1wVNf%2FBxcleNZUuGigOdZVwJGJ9tZD5D4q7NClJSVdGz0RBztZtHelWX%2BjWzYOpDwh7932KGx7l4PdajoFFdwU0N9bM%3D; _ga=GA1.2.1266138963.1590034960; _gid=GA1.2.1278650557.1590034960; i3_ab=6107; te=; mack=1'
}
proxies = {}

def run(offset):
    global keyworld
    keywd = urllib.request.quote(keyworld)
    url='https://www.r18.com/common/search/searchword=%s/page=%d/'%(keywd,offset)
    list_page(url)

def list_page(url):
    res = requests.get(url,headers=headers)
    if res.status_code==200:
        main_page = res.text
        pattern = re.compile('<div.*?data-id=\"(.*?)\".*?data-video-high=\"(.*?)\".*?</div>',re.S)
        items = re.findall(pattern,main_page)
        pool = ThreadPool(8) #双核电脑
        pool.map(download, items)#多线程工作
        pool.close()
        pool.join()
    else:
        print("请求网页失败，请检查网页URL是否正确------------")
        
def download(items):
    time.sleep(2)
    url = items[1]
    name = items[0]
    global keyworld
    filepath = '%s/%s.mp4' % (keyworld,name)
    print("正在下载: "+filepath)
    print("")
    if os.path.exists(filepath):
        print('已存在:%s '%(name))
        print('')
        return
    else:
        response = requests.get(url, headers=headers, stream=True)
        with open(filepath, "wb") as file:
            #total_length = int(response.headers.get('content-length'))
            file.write(response.content)
            # do something
            print("成功下载："+filepath)
            print("----------------------------------------------------------")
            print("")

keyworld = input("请输入搜索关键字:")
pages = input("请输入要爬取的页数:")
if __name__ == '__main__':
    pool = ThreadPool(8) #双核电脑
    tot_page = []
    path = '%s' % (keyworld)
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(1,int(pages)+1): #提取1到10页的内容
        tot_page.append(i)
    pool.map(run, tot_page)#多线程工作
    pool.close()
    pool.join()