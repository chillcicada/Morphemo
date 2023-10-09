# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup  # 用于解析 HTML, XML 需要安装 lxml (pip(3) install lxml)
from urllib.request import urlopen  # 用于打开 URL
from urllib.error import HTTPError, URLError  # 用于处理 HTTP 异常 和 URL 异常
import tldextract  # 用于解析 URL
import json  # 用于解析 JSON 数据
import re  # 用于解析正则表达式
import os  # 用于处理文件路径


class MorphemoNewCrawler:
  def __init__(self, url):
    self.url = url
    self.html = None
    self.domain = None
    self.METADATA = {}
    self.FUNCTION = []

  def isConnectable(self):
    """抛出异常值检查，判断 URL 是否可连接"""
    try:
      self.html = urlopen(self.url)
    except HTTPError as e:
      print(e)
      return False
    except (TimeoutError, URLError, ValueError):
      print('连接超时！请检查网络状态或 URL 地址是否存在拼写错误。')
      return False
    else:
      try:
        self.domain = tldextract.extract(self.url).domain
      except KeyError:
        print('该网站暂不支持或输入的 URL 地址不合法！')
        return False
      else:
        print('连接成功！')
        return True

  def mainCrawler(self, **kwargs):
    for key in kwargs:
      if key not in ('tags', 'comments'):
        try:
          self.METADATA[key] = eval(kwargs[key])
          pass
        except (AttributeError, TypeError, SyntaxError, NameError):
          pass

  def getMetadata(self):
    siteconfig = json.load(open('src/siteconfig.json', 'r', encoding='utf-8'))
    domain = tldextract.extract(self.url).domain
    for key in siteconfig[domain]["siteconfig"]:
      self.METADATA[key] = None
      self.FUNCTION = siteconfig[domain]["siteconfig"][key]
    siteconfig.close()

  def saveData(self):
    pass

  def setup(self):
    if self.isConnectable():

      print('数据已写入')
    else:
      print('爬取失败，程序已退出，请重试！')
      exit(0)
