#! -*-coding:utf-8 -*-
'''
Function:获取订阅文章内容
Author:蘭兹
'''

from urllib import request, parse
from bs4 import BeautifulSoup as Bs
from collections import Counter
import sqlite3
import lxml
import json
import datetime
import xlsxwriter
import re
import random
import time
import string
import os


starttime = datetime.datetime.now()

url = r'http://www.tuicool.com/ah/0?lang=1'

root_path = os.getcwd()

img_file_path = os.path.join(root_path, r'Blog/upload/blog')




# 获取推荐内容列表
def get_rss_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Host': 'www.tuicool.com',
        'Connection': 'keep-alive',
        'Referer': 'http://www.tuicool.com/a/?style=abs'
        }
    req = request.Request(url, headers=headers)
    page = request.urlopen(req).read()
    page = page.decode('utf-8')
    return page

# 获取推荐内容
def get_rss_info(page):
    soup = Bs(page,'lxml')
    # 标题list
    title_list = []
    for title in soup.select('a[class="article-list-title"]'):
        title_list.append(str(title.get_text()).replace('\n',''))
    # 链接list
    url_list = []
    for url in soup.select('a[class="article-list-title"]'):
        url_list.append('http://www.tuicool.com' + url['href'])
    # 摘要list
    summary_list = []
    for summary in soup.select('div[class="article_cut"]'):
        summary_list.append(str(summary.get_text()).replace('\n','').strip())
    rss_info_list = []
    for i in range(len(title_list)):
        rss_single = []
        rss_single.append(title_list[i])
        rss_single.append(url_list[i])
        rss_single.append(summary_list[i])
        rss_info_list.append(rss_single)
    return rss_info_list

def get_rss_content(rss_info_list,img_file_path):
    rss_content = []
    for rss in rss_info_list:
        url = rss[1]
        page = get_rss_page(url)
        soup = Bs(page,'lxml')
        try:
            source = re.search(r'>\w+',str(soup.select('span[class="from"] > a')[0])).group(0)
            source = re.search(r'\w+', source).group(0)
            content = str(soup.select('div[class="article_body"]')[0])
            content = re.sub(r'\\.', r'', content)
            content_soup = Bs(content,'lxml')
        except Exception as e:
            print('基本信息未获取')
        slug =''.join(random.sample('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789', 8))
        img_list = []
        img_url_list = content_soup.select('img')
        for img in img_url_list:
            img = img['src']
            try:
                img_name = re.search(r'\w+.(jpg|png)', img).group(0)
                img_list.append(img_name)
                img_download_path = img_file_path + '/' + '%s' %slug
                if os.path.exists(img_download_path):
                    request.urlretrieve(img,img_download_path + '/' + '%s' %img_name)
                else:
                    os.makedirs(img_download_path)
                    request.urlretrieve(img,img_download_path + '/' + '%s' %img_name)
                print('----------------- 下载 %s 完成 -----------------' %img_name)
                content = re.sub(r'http://img\d.tuicool.com/',r'/upload/blog/%s/' %slug ,content)
                content = re.sub(r'!web','',content)
            except Exception as e:
                print (u'图片下载错误')

        if len(img_list) == 0:
            rss.append('')
        else:
            rss.append(img_list[0])
        rss.append(slug)
        rss.append(content)
        rss.append(source)
        rss_content.append(rss)
    return rss_content


def post_db(rss_content, root_path):
    for rss in rss_content:
        title = rss[0]
        summary = rss[2]
        slug = rss[4]
        img = 'blog/%s/%s' %(slug,rss[3])
        content = rss[5]
        source = rss[6]
        status = 3
        blog_in_status = 3
        rss_time = time.strftime("%Y-%m-%d %H:%M:%S")
        read_zan_times = 0
        owner = 1
        category = 26
        top = 'True'
        try:
            db_path = root_path + r'/db.sqlite3'
            db = sqlite3.connect(db_path, timeout=10)
            db.execute("insert or ignore into Blog_blog(title,summary,img,slug,markdown_content,html_content,status,blog_in_status, created, modified, owner_id, category_id, top, read_times)"
                    "values('%s','%s','%s','%s','%s','%s',%d, %d, '%s', '%s', %d, %d, '%s', %d)"%(title,summary,img,slug,content,content,status,blog_in_status,rss_time,rss_time,owner,category,top,read_zan_times))
            print(u'添加--%s--到数据库' %title)
        except Exception as e:
            print(u'添加--%s--到数据库>>>****圆满失败*****' %title)
        db.commit()
        db.close()
    return 'db ok!'



if __name__ == '__main__':
    page = get_rss_page(url)
    rss_info_list = get_rss_info(page)
    rss_content = get_rss_content(rss_info_list,img_file_path)
    post_db(rss_content, root_path)


