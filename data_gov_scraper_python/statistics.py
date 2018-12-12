import csv
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')

articles_per_topic = data['topic'].value_counts()
topics = articles_per_topic.index.tolist()
number_articles_topic = articles_per_topic.values


articles_per_publisher = data['published_by'].value_counts()
publishers = articles_per_publisher.index.tolist()[:10]
number_articles_publisher = articles_per_publisher.values[:10]

articles_per_topic_ch = go.Pie(labels=topics, values=number_articles_topic)
py.plot([articles_per_topic_ch], filename='articles_per_topic_pie_chart')

top_publishers = go.Pie(labels=publishers, values=number_articles_publisher)
py.plot([top_publishers], filename='top_publishers_pie_chart')

