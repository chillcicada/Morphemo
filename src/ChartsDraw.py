# -*- coding: utf-8 -*-
"""
MorphemoWordcloud 类为词云生成类，用于生成词云。
单独运行此类时，生成的文件会导出到 assets/charts/ 中。
"""

import json
from pyecharts import options as opts
from pyecharts.charts import Bar, Graph, WordCloud
from pyecharts.globals import ThemeType, CurrentConfig
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

CurrentConfig.ONLINE_HOST = 'js/'

with open('assets/data/highFrequentWords/highFrequentWordsKey.json', encoding='UTF-8', mode='r') as keyFile:
  highFrequentWordsKey = json.load(keyFile)
with open('assets/data/highFrequentWords/highFrequentWordsValue.json', encoding='UTF-8', mode='r') as valueFile:
  highFrequentWordsValue = json.load(valueFile)
with open('assets/data/wordsTuple.json', encoding='UTF-8', mode='r') as wordsTuple:
  wordsTuple = json.load(wordsTuple)
with open('assets/data/wordsRelationship/wordsNode.json', encoding='UTF-8', mode='r') as wordsNode:
  wordNodes = list(json.load(wordsNode).values())
with open('assets/data/wordsRelationship/wordsLink.json', encoding='UTF-8', mode='r') as wordsLink:
  wordLinks = list(json.load(wordsLink).values())


class MorphemoChartsDraw:
  def __init__(self):
    self.barTheme = ThemeType.LIGHT
    self.graphTheme = ThemeType.LIGHT
    self.wordcloudTheme = ThemeType.LIGHT

  def drawBar(self) -> Bar:
    bar = (
      Bar(init_opts=opts.InitOpts(theme=self.barTheme))
      .add_xaxis(highFrequentWordsKey)
      .add_yaxis('词频', highFrequentWordsValue)
      .set_series_opts(label_opts=opts.LabelOpts(position='top'))
      .set_global_opts(title_opts=opts.TitleOpts(title='词频柱状图'))
    )
    return bar

  def drawGraph(self) -> Graph:
    graph = (
      Graph(init_opts=opts.InitOpts(theme=self.graphTheme))
      .add('关系云图', wordNodes, wordLinks, repulsion=8000, layout='force')
      .set_global_opts(title_opts=opts.TitleOpts(title='关系云图'))
    )
    return graph

  def drawWordcloud(self) -> WordCloud:
    wordcloud = (
      WordCloud(init_opts=opts.InitOpts(theme=self.wordcloudTheme))
      .add('词云', wordsTuple, word_size_range=[6, 66], shape='diamond')
      .set_global_opts(
        title_opts=opts.TitleOpts(
          title='词云',
          title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True)
      )
    )
    return wordcloud

  def save(self):
    self.drawBar().render('assets/charts/bar.html')
    make_snapshot(snapshot, self.drawBar().render(), 'assets/charts/bar.png', is_remove_html=True)
    self.drawGraph().render('assets/charts/graph.html')
    make_snapshot(snapshot, self.drawGraph().render(), 'assets/charts/graph.png', is_remove_html=True)
    self.drawWordcloud().render('assets/charts/wordcloud.html')
    make_snapshot(snapshot, self.drawWordcloud().render(), 'assets/charts/wordcloud.png', is_remove_html=True)
    print('图片已保存到 assets/charts/ 中。')


def main():
  obj = MorphemoChartsDraw()
  obj.save()


if __name__ == '__main__':
  main()
