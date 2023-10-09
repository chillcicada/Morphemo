# -*- coding: utf-8 -*-
"""
MorphemoWordCut 类为词频统计类，用于统计词频。
MorphemoWordCut 运行依赖 bin 目录下的 .json 文件。
"""

import re
import json
import jieba
import jieba.posseg
import jieba.analyse

with open('bin/stopWords.json', encoding='UTF-8', mode='r') as removeWordsFile:
  wordsRemovedList = json.load(removeWordsFile)


class MorphemoWordCut:
  def __init__(self, content):
    self.content = content  # 原文本
    self.newContent = ''  # 去除停用文字后文本
    self.wordsDict = {}  # 词频字典，用于生成词云图
    self.wordsTuple = []  # 词频元组，用于生成词频图
    self.wordsPos = {}  # 词性字典
    self.wordsNode = {}  # 词性关系-点
    self.wordsLink = {}  # 词性关系-边
    self.highFrequentWordsKey = []  # 高频词词汇
    self.highFrequentWordsValue = []  # 高频词词频
    self.highFrequentWordsDict = {}  # 高频词字典
    self.intSliceLenMax = 10  # 高频词切片长度

  def getWordsDict(self, intSliceLenMax=10):
    """获取词频"""
    wordsList = jieba.lcut(self.content, cut_all=False)
    newContent = []
    for word in wordsList:
      word = word.strip()
      if word not in wordsRemovedList:
        newContent.append(word)
        if word in self.wordsDict:
          self.wordsDict[word] += 1
        else:
          self.wordsDict[word] = 1
      elif word in ('!', '?', '\n', ',', '.', '，', '。', '！', '？'):
        newContent.append(word)
    self.newContent = ' '.join(newContent)
    wordsDictLen = len(self.wordsDict)
    self.wordsDict = {key: value for key, value in (sorted(self.wordsDict.items(), key=lambda item: item[1], reverse=True))}  # 根据键值讲其转化为按照词频降序排序
    for i in range(wordsDictLen):
      self.wordsTuple.append((list(self.wordsDict.keys())[i], list(self.wordsDict.values())[i]))
    intSliceLen = wordsDictLen if wordsDictLen < intSliceLenMax else intSliceLenMax
    self.highFrequentWordsValue = list(self.wordsDict.values())[0:intSliceLen]
    self.highFrequentWordsKey = list(self.wordsDict.keys())[0:intSliceLen]
    self.highFrequentWordsDict = dict(zip(self.highFrequentWordsKey, self.highFrequentWordsValue))

  def getWordsPos(self):
    """获取词性"""
    pass

  def getWordsRelationship(self):
    """获取词性关系"""
    sentences = re.sub('[！？。，]', '\n', self.newContent).split('\n')
    for sentence in sentences:
      if sentence not in ('', ' ', '\t', '\r'):
        words = [word for word in sentence.split(' ') if word != '']
        wordsLen = len(words)
        for i in range(wordsLen - 1):
          if words[i] not in self.wordsNode:
            self.wordsNode[words[i]] = {'name': words[i], 'symbolSize': 10}
          else:
            self.wordsNode[words[i]]['symbolSize'] += 10
          if words[i] != words[i + 1]:
            if words[i] < words[i + 1]:
              if (words[i] + ' ' + words[i + 1]) not in self.wordsLink:
                self.wordsLink[words[i] + ' ' + words[i + 1]] = {'source': words[i], 'target': words[i + 1], 'value': 10}
              else:
                self.wordsLink[words[i] + ' ' + words[i + 1]]['value'] += 10
            else:
              if (words[i + 1] + ' ' + words[i]) not in self.wordsLink:
                self.wordsLink[words[i + 1] + ' ' + words[i]] = {'source': words[i + 1], 'target': words[i], 'value': 10}
              else:
                self.wordsLink[words[i + 1] + ' ' + words[i]]['value'] += 10

  def save(self):
    """保存数据"""
    with open('assets/data/newContent.txt', encoding='UTF-8', mode='w') as newContent:
      newContent.write(self.newContent)
    with open('assets/data/wordsTuple.json', encoding='UTF-8', mode='w') as wordsTuple:
      json.dump(self.wordsTuple, wordsTuple, ensure_ascii=False)
    with open('assets/data/wordsRelationship/wordsNode.json', encoding='UTF-8', mode='w') as wordsNode:
      json.dump(self.wordsNode, wordsNode, ensure_ascii=False)
    with open('assets/data/wordsRelationship/wordsLink.json', encoding='UTF-8', mode='w') as wordsLink:
      json.dump(self.wordsLink, wordsLink, ensure_ascii=False)
    with open('assets/data/wordsPos.json', encoding='UTF-8', mode='w') as wordsPos:
      json.dump(self.wordsPos, wordsPos, ensure_ascii=False)
    with open('assets/data/highFrequentWords/highFrequentWordsKey.json', encoding='UTF-8', mode='w') as highFrequentWordsKey:
      json.dump(self.highFrequentWordsKey, highFrequentWordsKey, ensure_ascii=False)
    with open('assets/data/highFrequentWords/highFrequentWordsValue.json', encoding='UTF-8', mode='w') as highFrequentWordsValue:
      json.dump(self.highFrequentWordsValue, highFrequentWordsValue, ensure_ascii=False)
    with open('assets/data/highFrequentWords/highFrequentWordsDict.json', encoding='UTF-8', mode='w') as highFrequentWordsDict:
      json.dump(self.highFrequentWordsDict, highFrequentWordsDict, ensure_ascii=False)

  def setup(self):
    self.getWordsDict(self.intSliceLenMax)
    self.getWordsRelationship()
    self.save()


def main():
  testContent = '本文介绍了 Python 字典切片的基本语法、选取键或值、按照键或值进行排序、按照键或值进行过滤以及列表转字典等常用的操作。需要注意的是，在字典切片时，由于字典是无序的，因此不能像列表和字符串一样进行精确的索引切割。在具体操作时，需要考虑到字典键值对的对应关系，使用各种方法进行过滤、选择、排序等操作。'
  obj = MorphemoWordCut(testContent)
  obj.setup()


if __name__ == '__main__':
  main()
