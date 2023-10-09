# -*- coding: utf-8 -*-
"""
-*- Coded by LLK -*-\n
该模块包含一个类：MorphemoUrlsIterator。
MorphemoUrlsIterator 类为 URL 迭代器类，通过搜索算法爬取 sitemap/feed/rss 用于生成 urls.json 文件。
"""

import json  # 用于解析 JSON 数据
import re  # 用于解析正则表达式
import warnings  # 用于处理警告
from urllib.error import HTTPError, URLError  # 用于处理 HTTP 异常 和 URL 异常
import requests  # 用于发送请求
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning  # 用于解析 HTML, XML 需要安装 lxml (pip(3) install lxml)


class MorphemoUrlsIterator:
  poolReq = Pool(IntCpuUsed)  # 创建进程池
  poolStatus = True  # 进程池状态

  # 用于存储 sitemap 的列表
  listSitemap = [
    'sitemap',
    'sitemap/',
    'sitemap.xml',
    'sitemap1',
    'sitemap_index',
    'sitemap_index/',
    'sitemap_index.xml',
    'post-sitemap',
    'page-sitemap',
    'feed',
    'feed/',
    'feed.xml',
  ]

  def __init__(self, url):
    self.url = url
    self.req = None
    self.urlTry = None

  def urlTruing(self):
    listProtocol = ['http', 'https']
    self.url = re.sub('https?//', '', self.url).split('/')[0] + '/'
    self.url = listProtocol[self.isConnectable('https' + '://' + self.url)] + '://' + self.url

  def isConnectable(self, urlTry):
    try:
      self.req = requests.get(urlTry, timeout=5, allow_redirects=False)
    except HTTPError as e:
      print(e)
      return False
    except (TimeoutError, URLError, ValueError):
      print('连接超时！请检查网络状态或 URL 地址是否存在拼写错误。')
      return False

  def reqSitemap(self, sitemapSuffix):
    urlTry = self.url + sitemapSuffix
    if self.isConnectable(urlTry):
      if self.req.status_code == 200:
        self.urlTry = urlTry
        self.poolReq.close()  # 关闭进程池
        self.poolStatus = False  # 更改进程池状态

  def multiProcessReq(self):
    self.poolReq.map(self.reqSitemap, self.listSitemap)  # 多进程爬取
    if self.poolStatus:
      self.poolReq.close()  # 关闭进程池
    self.poolReq.join()  # 阻塞主进程，等待子进程的退出

  def getUrls(self):
    if self.urlTry:
      self.req = requests.get(self.urlTry)
      bsReq = BeautifulSoup(self.req.text, 'lxml')
      if warnings.warn(bsReq.get_text(), category=XMLParsedAsHTMLWarning):
        bsReq = BeautifulSoup(self.req.text, 'lxml-xml')
      urlsFind = re.compile('<a href=".*>').findall(str(bsReq.get_text()))
      urlsFind = [re.sub('<a href="|".*?>', '', urlFind) for urlFind in urlsFind]
      return urlsFind

  def urlsUpload(self):
    urlsFind = self.getUrls()
    if urlsFind:
      for urlFind in urlsFind:
        urls.append(urlFind)
      jsonUrls.seek(-1, 2)  # 将文件指针移动到文件末尾
      json.dump(urls, jsonUrls, ensure_ascii=False, indent=2)  # 将 urls 列表写入 urls.json 文件
      jsonUrls.truncate()  # 截断文件
      print('urls.json 文件已更新！')
    else:
      print('未找到 sitemap！')

  def setup(self):
    """执行函数"""
    self.urlTruing()
    self.multiProcessReq()
    self.urlsUpload()
