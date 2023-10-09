# -*- coding: utf-8 -*-
"""
-*- Coded by LLK -*-\n
此程序用于初始化同目录的 crawlerData.csv 文件。
"""

import csv

datafile = open('crawlerData.csv', 'w', encoding='utf-8-sig', newline='')  # 写入 CSV 文件
datawriter = csv.writer(datafile)  # 创建 CSV 写入器


def main():
  datawriter.writerow(['url', 'title', 'content', 'leadAuthor', 'coAuthor', 'date', 'tags', 'wordCount', 'readingTime', 'commentCount', 'chargeCount', 'likeCount', 'viewCount', 'shareCount', 'relatedArticles', 'source'])


if __name__ == '__main__':
  main()
