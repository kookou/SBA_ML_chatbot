import json
import csv
import pandas as pd
from pandas import DataFrame

review = './csv/review.csv'
food = './csv/menu.csv'
shop = './csv/store.csv'
total = 'total.csv'

myreview = pd.read_csv(review, sep=',', encoding='utf-8')
myfood = pd.read_csv(food, sep=',', encoding='utf-8')
mystore = pd.read_csv(shop, sep=',', encoding='utf-8')
data = pd.read_csv(total, sep=',', encoding='utf-8')

myframe = pd.read_csv(filename, sep=',', encoding='utf-8')
columns = ['id', 'name', 'lat', 'lng', '동', '지번', 'nickname', 'orderid', 'menu_summary', 'comment']

# print(myframe['구'].value_counts(ascending=True))

# row에서 필요한 셀만 추가
result = []
for index, row in myframe.iterrows():
    if row['동'] == '대림동':
        imsi = [row['id'], row['name'], row['lat'], row['lng'], row['동'], row['지번'], row['nickname'], row['orderid'],
                row['menu_summary'], row['comment']]
        result.append(imsi)

result = pd.DataFrame(result, columns=columns)

outcome = []
for index, row in result.iterrows():
    if row['nickname'] == 'do**':
        imsi = [row['id'], row['name'], row['lat'], row['lng'], row['동'], row['지번'], row['nickname'], row['orderid'],
                row['menu_summary'], row['comment']]
        outcome.append(imsi)

outcome = pd.DataFrame(outcome, columns=columns)

# 두개의 데이터 프레임을 옆으로 붙이기
data = pd.concat([myframe, result], axis=1)
print(data.head(20))

# index 'id'로 데이터 합치기
mergedata = pd.merge(data, outcome, on='id', how='left')
print(mergedata.head())

# outcome.to_csv('yeongdeungpo_do.csv', mode='w', encoding='utf-8', index=False)
