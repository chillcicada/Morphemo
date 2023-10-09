# -*- coding: utf-8 -*-
"""
-*- Coded by LLK -*-\n
该模块包含一个类：MorphemoCrawler。
MorphemoCrawler 为通用爬虫类，用于爬取指定 URL 的文章内容。
本程序依赖 bug 运行，请勿随意修改。
如需添加新的网站爬虫，请在 bin/siteconfig.json 文件中添加相应的配置。
如需爬取新的网站，请在 bin/urls.json 文件中添加相应的 URL。
如需爬取多个网站，请先运行 assets 目录下的 InitializeCrawlerData.py 初始化 csv 数据，再运行本程序。
如需爬取单个网站，请在 py 脚本中调用 MorphemoCrawler 类的 setup 方法，传入 URL 即可，而不是直接运行本程序。
初始化 MorphemoCrawler 类时，需要传入 URL 参数，该参数为字符串类型。
- MorphemoCrawler 运行依赖于 bin 目录的 siteconfig.json 文件，该文件用于存储各个网站的爬虫配置。
siteconfig.json 文件的格式如下：
{
  "域名": {
    "name": "网站名称",
    "site": "网站 url 地址",
    "siteconfig": {
      "getTitle": "获取标题的方法",
      "getContent": "获取内容的方法",
      "getLeadAuthor": "获取主作者的方法",
      "getDate": "获取日期的方法",
      "getTags": "获取标签的方法",
      "getWordCount": "获取字数的方法",
      "getReadingTime": "获取阅读时间的方法",
      "getCommentCount": "获取评论数的方法",
      "getLikeCount": "获取点赞数的方法",
      "getViewCount": "获取阅读数的方法",
      "getChargeCount": "获取充电数的方法",
      "getRelatedArticles": "获取相关文章的方法",
      "getSource": "获取来源的方法"
    }
  }
}
- MorphemoCrawler 运行依赖于 bin 目录的 urls.json 文件用于存储需要爬取的 URL，格式如下：
[
  "url1",
  "url2",
  "url3",
  ...
]
爬取数据将以 csv 格式导入到 assets 目录下的 crawlerData.csv 文件中。
"""

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning  # 用于解析 HTML, XML 需要安装 lxml (pip(3) install lxml)
from urllib.request import urlopen  # 用于打开 URL
from urllib.error import HTTPError, URLError  # 用于处理 HTTP 异常 和 URL 异常
import tldextract  # 用于解析 URL
import json  # 用于解析 JSON 数据
import csv  # 用于存储 CSV 数据
import re  # 用于解析正则表达式

siteconfig = open('bin/siteconfig.json', encoding='utf-8')  # 加载配置文件
datafile = open('assets/crawlerData.csv', mode='a', encoding='utf-8-sig', newline='')  # 写入 CSV 文件
datawriter = csv.writer(datafile)  # 创建 CSV 写入器
jsonUrls = open('bin/urls.json', encoding='utf-8')  # 读取 urls.json 文件
urls = json.load(jsonUrls)  # 将 urls.json 文件中的数据转换为列表


class MorphemoCrawler:
  METADATA = {
    'url': '',
    'title': '',
    'content': '',
    'leadAuthor': '',
    'coAuthor': '',
    # 'date': {
    #   'year': 0,
    #   'month': 0,
    #   'day': 0,
    # },
    'date': '',
    'tags': '',
    'wordCount': 0,
    'readingTime': 0,
    'commentCount': 0,
    'chargeCount': 0,
    'likeCount': 0,
    'viewCount': 0,
    'shareCount': 0,
    'relatedArticles': [],
    'source': '',
  }

  def __init__(self, url):
    self.url = url
    self.html = None
    self.bs = None
    self.title = None
    self.content = None
    self.leadAuthor = None
    self.date = None
    self.tags = None
    self.coAuthor = None
    self.chargeCount = None
    self.readingTime = None
    self.wordCount = None
    self.commentCount = None
    self.likeCount = None
    self.viewCount = None
    self.shareCount = None
    self.relatedArticles = None
    self.source = None

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
      print('连接成功！')
      return True

  def getTitle(self):
    try:
      self.title = eval(getTitle)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('标题获取失败！')
    else:
      self.METADATA['title'] = self.title

  def getContent(self):
    try:
      self.content = eval(getContent)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('内容获取失败！')
    else:
      self.METADATA['content'] = self.content

  def getLeadAuthor(self):
    try:
      self.leadAuthor = eval(getLeadAuthor)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('主作者获取失败！')
    else:
      self.METADATA['leadAuthor'] = self.leadAuthor

  def getDate(self):
    try:
      self.date = eval(getDate)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('日期获取失败！')
    else:
      self.METADATA['date'] = self.date

  def getTags(self):
    try:
      self.tags = eval(getTags)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('标签获取失败！')
    else:
      self.METADATA['tags'] += self.tags

  def getWordCount(self):
    try:
      self.wordCount = eval(getWordCount)
    except (AttributeError, TypeError, SyntaxError, NameError):
      try:
        self.wordCount = len(self.METADATA['content'])
      except (AttributeError, TypeError, SyntaxError, NameError):
        print('字数获取失败！')
      else:
        self.METADATA['wordCount'] = self.wordCount
    else:
      self.METADATA['wordCount'] = self.wordCount

  def getReadingTime(self):
    try:
      self.readingTime = eval(getReadingTime)
    except (AttributeError, TypeError, SyntaxError, NameError):
      try:
        self.readingTime = self.METADATA['wordCount'] / 500
      except (AttributeError, TypeError, SyntaxError, NameError):
        print('阅读时间获取失败！')
      else:
        self.METADATA['readingTime'] = self.readingTime
    else:
      self.METADATA['readingTime'] = self.readingTime

  def getCommentCount(self):
    try:
      self.commentCount = eval(getCommentCount)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('评论获取失败！')
    else:
      self.METADATA['commentCount'] = self.commentCount

  def getLikeCount(self):
    try:
      self.likeCount = eval(getLikeCount)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('点赞人数获取失败！')
    else:
      self.METADATA['likeCount'] = self.likeCount

  def getViewCount(self):
    try:
      self.viewCount = eval(getViewCount)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('阅读人数获取失败！')
    else:
      self.METADATA['viewCount'] = self.viewCount

  def getChargeCount(self):
    try:
      self.chargeCount = eval(getChargeCount)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('充电人数获取失败！')
    else:
      self.METADATA['chargeCount'] = self.chargeCount

  def getRelatedArticles(self):
    try:
      self.relatedArticles = eval(getRelatedArticles)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('相关文章获取失败！')
    else:
      self.METADATA['relatedArticles'] += self.relatedArticles

  def getSource(self):
    try:
      self.source = eval(getSource)
    except (AttributeError, TypeError, SyntaxError, NameError):
      print('来源获取失败！')
    else:
      self.METADATA['source'] = self.source

  def writeData(self):
    """将爬取到的数据写入 CSV 文件"""
    datawriter.writerow(self.METADATA.values())

  def setup(self):
    """执行函数"""
    if self.isConnectable():
      self.bs = BeautifulSoup(self.html.read(), 'lxml')
      self.METADATA['url'] = self.url
      self.getTitle()
      self.getContent()
      self.getLeadAuthor()
      self.getDate()
      self.getTags()
      self.getWordCount()
      self.getReadingTime()
      self.getCommentCount()
      self.getLikeCount()
      self.getViewCount()
      self.getChargeCount()
      self.getRelatedArticles()
      self.getSource()
      # print(self.METADATA)  # 用于调试，输出爬取到的数据
      self.writeData()
      print('数据已写入 crawlerData.csv 文件中！')


def multiProcessCrawl(url):
  """多进程爬取"""
  domain = tldextract.extract(url).domain
  print(domain)  # 用于调试，获取域名
  try:
    # 上传配置文件中的所需配置
    globals().update(json.load(siteconfig)[domain]["siteconfig"])
  except KeyError:
    # 若配置文件中不存在该网站的配置，则退出程序
    print('该网站暂不支持或输入的 URL 有误！')
    exit(0)
  objCrawler = MorphemoCrawler(url)
  objCrawler.setup()


def main():
  """主函数"""
  from multiprocessing import cpu_count, Pool  # 用于获取 CPU 核心数和多进程爬取
  IntCpuUsed = int(cpu_count() / 2)  # 默认只使用一半的 CPU 核心数用于爬取
  poolCrawl = Pool(IntCpuUsed)  # 创建进程池
  poolCrawl.map(multiProcessCrawl, urls)  # 多进程爬取
  poolCrawl.close()  # 关闭进程池
  poolCrawl.join()  # 阻塞主进程，等待子进程的退出
  jsonUrls.close()  # 关闭 urls.json 文件
  datafile.close()  # 关闭 crawlerData.csv 文件
  siteconfig.close()  # 关闭 siteconfig.json 文件


if __name__ == '__main__':
  main()
