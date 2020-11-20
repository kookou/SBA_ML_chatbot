import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))

from haversine import haversine, Unit
import pandas as pd
import numpy as np
import folium
import pdb
pd.set_option('display.max_columns', 100)

from util.file_helper import FileReader


class Preprocessor:
    pass


# csv파일 불러옴
# 파이참 방식
# file_path = r'./../../data/csv/gangnam_seocho.csv'
# df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')

# file_path2 = r'./../../data/csv/store.csv'
# shop_df = pd.read_csv(file_path2, sep=',', encoding='utf-8-sig')

# file_path3 = r'./../../data/csv/menu/yogiyo_menu_gs.csv'
# food_df = pd.read_csv(file_path3, sep=',', encoding='utf-8-sig')

# file_path4 = r'./../../data/csv/owner_comment.csv'
# owner_cmnt_df = pd.read_csv(file_path4, sep=',', encoding='utf-8-sig')

# vscode 방식
file_path = r'.//data/csv/gangnam_seocho.csv'
df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')

file_path2 = r'./data/csv/store.csv'
shop_df = pd.read_csv(file_path2, sep=',', encoding='utf-8-sig')

file_path3 =  r'./data/csv/menu/yogiyo_menu_gs.csv'
food_df = pd.read_csv(file_path3, sep=',', encoding='utf-8-sig')

file_path4 = r'./data/csv/owner_comment.csv'
owner_cmnt_df = pd.read_csv(file_path4, sep=',', encoding='utf-8-sig')


# orderid_list = df['orderid'].tolist()
df = df.dropna(subset=['orderid'])
# df['orderid'].dropna()
df['orderid'] = df['orderid'].astype(int)


# for i, id in enumerate(orderid_list):

#     df.loc[df[df['orderid'] == id].index, 'owner_cmnt'] = \
#         owner_cmnt_df[owner_cmnt_df['orderid'] == id]['owner_comment']
#     print(f'{i}번 처리 완료')

merge_df = pd.merge(df, owner_cmnt_df, how='left',on='orderid')

merge_df.to_csv('review_df(add_owner_cmnt).csv', sep=',', encoding='utf-8-sig', index=False)




















