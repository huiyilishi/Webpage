import urllib.request as ur
import re
from urllib.error import URLError,ContentTooShortError,HTTPError
from urllib.parse import urlparse,urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

rp = RobotFileParser()
user_agent="Python-urllib/5.0"

def download(url,num_retries=2):
    try:
        print("Downloading:",url)
        header = {"User-Agent": "Python-urllib/5.0"}
        request=ur.Request(url,headers=header)
        response = ur.urlopen(request)
# 类文件对象支持 文件对象的操作方法，如read()方法读取文件全部内容，返回字符串
        html = response.read()
    except (URLError,ContentTooShortError,HTTPError) as e:
        print('Download error:',e.reason)
        html=None
        if num_retries>0:
            if hasattr(e,'code') and (500 <= e.code <600):
                return download(url,num_retries=1)
    # print(html)
    return html
# 打印字符串
def crawl_sitemap(url):
    sitemap=download(url)
    links=re.findall('<loc>(.*?)</loc>',sitemap.decode('utf-8'))
    for link in links:
        html=download(link)
        print(html)

#链接爬虫
def link_crawler(seed_url,link_regex):
    rp.set_url(urljoin(seed_url,'/robots.txt'))
    rp.read()
    crawl_queue=[seed_url]
    seen=set(crawl_queue)
    while crawl_queue:
        url=crawl_queue.pop()
        html=download(url)
        soup=BeautifulSoup(html,'html.parser')
        tr=soup.find(attrs={'id':'app'})
        if tr is not None:
            td=tr.find(attrs={'class':'index_nav_center'})
            tl=td.find_all(attrs={'target':'_blank'})
            for data in tl:
                name=data.text
                print(name)
        for link in get_links(html) :
            if rp.can_fetch(user_agent,link):
                if link_regex in link:
                    # print(link+'?')
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
            else:
                print('Blocked by robots.txt:',link)
#获取网页中的所有链接
def get_links(html):
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    link_list=webpage_regex.findall(html.decode('utf-8'))
    # print(link_list)
    return link_list



# crawl_sitemap("http://csdn.net")
# crawl_sitemap("https://www.zillow.com/sitemap/catalog/cdp/index.xml")
# html=download('http://csdn.net')
html=download('https://www.zillow.com')
print(html)
# html1=download('https://www.zillow.com/')
# print(html1)