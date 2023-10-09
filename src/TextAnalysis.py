# -*- coding: utf-8 -*-
"""
TextAnalysis 为文本总结类，用于分析总结已经经过精细化处理的内容
将已经经过精细化处理的内容放入 text 中，读取其中内容进行最后的分析总结，并输出各分析数据和图表
总结流程：
    1.运用 jieba 库先对 text 中的内容进行中文分词
    2.分析文本的用词特点如词频、唯一词数量等
    3.用 snownlp 库分析文本的情感倾向
    4.运用 matplotlib 库绘制词频柱状图
    5.生成文本分析报告
输入：将文本内容放入 text 中
输出：文本总结报告和词频柱状图，报告将写入 assets/output.md 中
"""

import jieba
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from snownlp import SnowNLP

# 读取文本内容
articleFile = open('assets/paragraphs.txt', 'r', encoding='utf-8')
article = articleFile.read()


class MorphemoTextAnalysis:
  # 初始化文本分析对象，输入为待分析的文本和字体路径,并且使用 jieba 进行中文分词，以及创建一个 SnowNLP 对象用于情感分析
  def __init__(self, text, font_path):
    self.text = text
    self.font_path = font_path
    self.words = list(jieba.cut(text))
    self.blob = SnowNLP(text)

  # 绘制词频柱状图
  def plot_word_frequency(self):
    font = FontProperties(fname=self.font_path)
    # word_freq = self.analyze_word_frequency()
    word_freq = Counter(self.words)
    plt.figure(figsize=(10, 6))
    words, frequencies = zip(*word_freq.most_common())
    plt.bar(words, frequencies)
    plt.xlabel('词语', fontproperties=font)
    plt.ylabel('频率', fontproperties=font)
    plt.title('词语频率统计', fontproperties=font)
    plt.xticks(rotation=45, fontproperties=font)
    plt.tight_layout()
    plt.show()

  # 生成文本分析报告
  def generate_report(self):
    unique_words = set(self.words)
    num_unique_words = len(unique_words)
    avg_word_length = sum(len(word) for word in self.words) / len(self.words)
    sentiment_polarity = self.blob.sentiments  # 使用SnowNLP分析情感极性和主观性
    word_freq = Counter(self.words)
    markdownFile = open('assets/output.md', 'w', encoding='utf-8')
    markdownFile.write('# 文本分析报告\n\n## 词特点分析\n\n唯一词语数量: ' + str(num_unique_words) + '\n\n## 感情色彩分析\n\n情感极性: ' + str(sentiment_polarity) + '\n\n## 词语频率统计\n\n')
    markdownFile.close()
    markdownFile = open('assets/output.md', 'a', encoding='utf-8')
    for word, freq in word_freq.most_common():
      markdownFile.write(word + ': ' + str(freq) + '\n&emsp;')
    markdownFile.close()

  def setup(self):
    # 调用类
    self.generate_report()
    self.plot_word_frequency()


obj = MorphemoTextAnalysis(article, "assets/fonts/SmileySans-Oblique.ttf")
obj.setup()
