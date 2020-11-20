from haversine import haversine, Unit
import pandas as pd
import numpy as np
import folium
import pdb
pd.set_option('display.max_columns', 100)

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))

class Preprocessor:
    pass


# csv파일 불러옴
# file_path = r'./../../data/csv/gangnam_seocho.csv'
# df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')

# file_path2 = r'./../../data/csv/store.csv'
# shop_df = pd.read_csv(file_path2, sep=',', encoding='utf-8-sig')

# file_path3 = r'./../../data/csv/menu.csv'
# food_df = pd.read_csv(file_path3, sep=',', encoding='utf-8-sig')

# vscode 방식
file_path = r'./data/csv/gangnam_seocho.csv'
df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')

file_path2 = r'./data/csv/store.csv'
shop_df = pd.read_csv(file_path2, sep=',', encoding='utf-8-sig')

file_path3 = r'./data/csv/menu.csv'
food_df = pd.read_csv(file_path3, sep=',', encoding='utf-8-sig')


# print(df)
# print(df.columns)
# print(df['nickname'])

###############################
# 샘플 데이터 테스트 코드

### 닉네임에 따라 데이터 필터링 ###
# 해당 조건을 만족하면 true, 아니면 false인 dataframe 리턴
# nickname = 'kh**'
# user = df['nickname'] == nickname
# 조건이 true인 행들만 담아 dataframe으로 리턴
# user = df[user]

# print(user)

# print(user['id'].drop_duplicates().tolist())

# 조건을 만족하는 리뷰 리스트의 id(shop)를 중복을 제거하고 리스트로 리턴
# user_shop_list = user['id'].drop_duplicates().tolist()

# 기준점 위경도
# target = df.head(1)
# target_geo = df[['lat', 'lng']].iloc[1].to_frame() //df 방식
# print(target_geo)
# target_lat, target_lng = target_geo_list = (37.520775, 127.022767)


# 이중 리스트로 되어있는 것을 flatten
# target_lat, target_lng = target_geo_list = sum(target_geo.values.tolist(), [])  # df방식
# print(sum(target_geo.values.tolist(), []))



# folium map 생성
# map = folium.Map(location=[target_lat, target_lng], zoom_start=14)
# filtered_df = pd.DataFrame()
# # print(type(filtered_df))
# for item in user_shop_list:
#     is_item = df['id'] == item
#     row = df[is_item]
#     one_row = row.head(1)
#     # print(one_row[['id', 'name', 'lat', 'lng']])
#     if haversine(target_geo_list, [one_row['lat'], one_row['lng']]) <= 1:
#
#         filtered_df = filtered_df.append(df[(df['nickname'] == nickname) & (df['id'] == item)])
#         # folium.Marker([one_row['lat'], one_row['lng']],
#         #               tooltip=one_row['name']
#         #               ).add_to(map)


# print(filtered_df)
# filtered_df.to_csv('filtered_df.csv', sep=',', encoding='utf-8-sig')
# map.save('map.html')
###############################


# 기준점 위경도
target_lat, target_lng = target_geo_list = (37.520775, 127.022767)

# user DataFrame
user_columns = ['userid', 'pwd', 'name', 'age', "gender", 'addr', 'lat', 'lng']
user_df = pd.DataFrame(columns=user_columns)

# # order_review DataFrame
# order_review_columns = ['order_id', 'order_time', 'order_cmnt', 'userid', 'shop_id', 'food_id']
order_review_df = pd.DataFrame(columns=order_review_columns)

# 리뷰 리스트에서 id(shop)를 중복을 제거하고 리스트로 리턴
shop_list = df['id'].drop_duplicates().tolist()



# 기준점으로 부터 반경 1km 이내의 매장만 필터링
def filter_shop(i):
    one_row = df[df['id'] == i].head(1)
    if haversine(target_geo_list,
                 [one_row['lat'].head(1), one_row['lng'].head(1)]) <= 1:
        return i


filtered_shop_list = list(filter(filter_shop, shop_list))
# print(filtered_shop_list)


# ================================
# 기준점 내의 매장에 리뷰를 쓴 아이디 리스트 필터링
user_list = []
for shop in filtered_shop_list:
    nickname = df[df['id'] == shop]['nickname'].tolist()
    user_list.append(nickname)

# print(user_list)
# flatten(1차원 리스트화)
user_list = sum(user_list, [])
# print(user_list)
# print('--------------------------')
# 중복 제거
user_list = list(set(user_list))
print(len(user_list))
# pdb.set_trace()
try:
    user_list.remove(np.nan)
    user_list.remove('손님')
except:
    '해당값이 없음'
# print('===================')
# print(user_list)
# ================================

# userid pk생성을 위한 index count
count = 0

for user in user_list:
    # user DateFrame 생성
    # 유저 아이디 생성
    userid = f'user{str(count).zfill(6)}'
    lat = target_lat
    lng = target_lng
    addr = '서울특별시 강남구 신사동 534-20'  # 하드 코딩 주의!! 기준점 위/경도로 검색해서 주소 입력해야함
    # 잘못한거지만 형식 남겨둠
    # lat = shop_df[shop_df['id'] == shop]['lat'].head(1).to_string(index=False)
    # lng = shop_df[shop_df['id'] == shop]['lng'].head(1).to_string(index=False)
    # addr = shop_df[shop_df['id'] == shop]['address'].head(1).to_string(index=False)
    _user_df = pd.DataFrame([[userid, "", userid, "", "", addr, lat, lng]], columns=user_columns)
    user_df = user_df.append(_user_df, ignore_index=True)
    for shop in filtered_shop_list:
        is_shop_user = (df['id'] == shop) & (df['nickname'] == user)
        user_review_list = df[is_shop_user]
        if not user_review_list.empty:


            # index를 기준으로 review에 userid 추가/order_df data 생성
            for i in user_review_list.index:

                # ===============================
                # order DateFrame 생성
                order_id = df.loc[i, 'orderid']
                # order_id = df[df['id'] == shop]['orderid'].head(1).to_string(index=False)
                # order_id가 float 형태의 문자열이라 포맷 변환(나중에 문자열 포매팅으로 변환할 것)
                order_id = int(float(order_id))
                # print('order_id:', order_id)

                order_time = df.loc[i, 'time']
                shop_id = df.loc[i, 'id']
                shop_id = int(float(shop_id))
                # print('shop_id:', shop_id)

                food_name = df.loc[i, 'menu_summary']
                # 메뉴명 누락(nan)인 경우 제외
                try:
                    food_name = food_name.split('/')[0]
                except:
                    print('메뉴명 누락(nan)')
                    food_name = ""
                # print(food_name)

                is_food_name = (food_df['id'] == shop) & (food_df['name'] == food_name)
                food_id = food_df[is_food_name]['id.1'].to_string(index=False)
                # 해당 메뉴가 없을 경우 공백으로 처리
                if food_id == 'Series([], )':
                    food_id = ""
                # print(type(food_id))
                # print(food_id)
                _order_df = pd.DataFrame([[order_id, order_time, "", userid, shop_id, food_id]], columns=order_columns)
                order_df = order_df.append(_order_df, ignore_index=True)

                # print(order_df)
                # pdb.set_trace()  # debug point
                # ===============================

                # ===============================
                # review DataFrame에 컬럼 추가
                # print(i)
                df.loc[i, 'userid'] = userid
                # print(df.loc[i])
                df.loc[i, 'food_id'] = food_id
                df.loc[i, 'order_id'] = order_id

                # ===============================
    count += 1

    if count >= 100:
        break
    # break

# print(user_df)
# print(df)
user_df.to_csv('user_df.csv', sep=',', encoding='utf-8-sig', index=False)
order_df.to_csv('order_df.csv', sep=',', encoding='utf-8-sig', index=False)
df.to_csv('review_df.csv', sep=',', encoding='utf-8-sig', index=False)




















