# -*- coding: utf-8 -*-
"""
MorphemoStandardization 为规范化处理类，用于将爬虫获取的文章内容变为统一格式，并消除 emoji 等坏类型
识别 assets 目录下记录爬虫爬取数据的 crawlerData.csv 文件，读取其中的内容，转化为 列表 [字典1{……}，字典2{……}，……] 格式，
再对文本进行规范化处理，将处理后的内容存入同目录下的 paragraphs.txt 文件。
处理标准：
    1.如果文章标题或内容为 nan ，则将其转换为字符串类型的 '无标题'或’无内容‘。
    2.标题后隔两行
    3.如有换行，进行分段，段落间隔一行
    4.将段落中相连的多个空格合并为一个
    5.如出现，,。.；;？！!:：…?中的任意一种，进行分句，句子间不隔行
    6.去除句子中的 emoji，去除句首句尾的空格。
    7.文章内容结束后隔两行
需要：assets 目录下的 crawlerData.csv 文件
输出：同目录下的 paragraphs.txt 文件
函数：MorphemoStandardization.save_articles_to_file
"""

import re  # 分段、分句
import emoji  # 去除emoji
import pandas as pd  # 读取、写入文件；判断 nan


class MorphemoStandardization:  # 规范化处理
  # 读取初始文件
  def read_csv(self, a: list, b: list):
    df = pd.read_csv("assets/crawlerData.csv", header=0)
    for line in df.values:
      dic = {}
      for item, data in zip(df, line.tolist()):
        dic[item] = data
      a.append(dic)
    for item, data in zip(df, df.values[0].tolist()):  # 读取表头
      b.append(item)
    return a, b

  # 根据标点分句
  def seg_tail_split(self, str1, sep=r"[，,。\.；;？！!:：…\?]"):  # 分隔符可为多样的正则表达式
    # 保留标点符号，置于句尾
    w = re.split(sep, str1)
    seg_word = re.findall(sep, str1)
    seg_word.extend(" ")  # 末尾插入一个空字符串，以保持长度和切割成分相同
    w = [x + y for x, y in zip(w, seg_word)]  # 顺序可根据需求调换
    return w

  # 将文本划分为句段并存储为文件
  def save_articles_to_file(self):
    articles = []  # 文章
    head_row = []  # 表头
    n = 1  # 标题
    m = 2  # 内容
    articles, head_row = self.read_csv(articles, head_row)  # 读取
    with open('assets/paragraphs.txt', 'w', encoding='utf-8') as file:
      for article in articles:  # 遍历列表内的文章
        # file.write(article['url'] + '\n')
        if pd.isna(article[head_row[n]]):  # 防止标题为空
          article[head_row[n]] = '无标题'
        file.write(article[head_row[n]] + '\n\n\n')  # 文章标题，之后空两行
        if pd.isna(article[head_row[m]]):  # 防止内容为空
          article[head_row[m]] = '无内容'
        content = article[head_row[m]]
        paragraphs = content.split('\n')  # 换行表示段落分隔
        for paragraph in paragraphs:
          paragraph = re.sub(r'\s+', ' ', paragraph)  # 将段落中相连的多个空格合并为一个
          if paragraph != ' ' and paragraph:  # 跳过空段落
            # sentences = re.split(r'[，,。.；;？?！!:：…]\s*', paragraph)  # 另一种断句方法，但是会消除标点
            sentences = self.seg_tail_split(paragraph)  # 根据标点符号断句
            for sentence in sentences:
              sentence = " ".join(emoji.replace_emoji(sentence).split())  # 去除emoji
              cleaned_sentence = sentence.strip()  # 去除句子首尾的空格
              if cleaned_sentence:  # 跳过空句子
                file.write(cleaned_sentence + '\n')  # 输出句子，句子间换行
            file.write('\n')  # 段落间空行
        file.write('\n')  # 文章间空两行


obj = MorphemoStandardization()
obj.save_articles_to_file()
