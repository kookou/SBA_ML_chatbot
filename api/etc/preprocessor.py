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
file_path = r'./../../data/csv/important/review_df.csv'
# df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig', dtype={'userid': str, 'food_id': float, 'order_time': str})
df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')
print('오더리뷰 로딩완료')

# file_path2 = r'./../../data/csv/store.csv'
# shop_df = pd.read_csv(file_path2, sep=',', encoding='utf-8-sig')
# print('매장 로딩완료')
file_path3 = r'./../../data/csv/important/food.csv'
food_df = pd.read_csv(file_path3, sep=',', encoding='utf-8-sig')
print('메뉴 로딩완료')

file_path4 = r'./../../data/csv/important/위경도(강남_서초).csv'
point_df = pd.read_csv(file_path4, sep=',', encoding='utf-8-sig')

# vscode 방식
# file_path = r'./data/csv/gangnam_seocho(add_owner_cmnt).csv'
# df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')
#
# file_path2 = r'./data/csv/store.csv'
# shop_df = pd.read_csv(file_path2, sep=',', encoding='utf-8-sig')
#
# file_path3 =  r'./data/csv/menu/yogiyo_menu_gs.csv'
# food_df = pd.read_csv(file_path3, sep=',', encoding='utf-8-sig')



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

count = 3978
for idx in range(5, 6):
# for idx in range(5, len(point_df)):

    # 기준점 위경도
    target_lat, target_lng = target_geo_list = (point_df.loc[idx]['lat'], point_df.loc[idx]['lng'])
    print(f'위도: {target_lat}, 경도: {target_lng}')

    # user DataFrame
    user_columns = ['userid', 'pwd', 'name', 'age', "gender", 'addr', 'lat', 'lng']
    user_df = pd.DataFrame(columns=user_columns)

    # # order_review DataFrame
    # order_review_columns = ['order_id', 'order_time', 'order_cmnt', 'userid', 'shop_id', 'food_id']
    # order_review_df = pd.DataFrame(columns=order_review_columns)

    # 리뷰 리스트에서 id(shop)를 중복을 제거하고 리스트로 리턴
    shop_list = df['shop_id'].drop_duplicates().tolist()



    # 기준점으로 부터 반경 1km 이내의 매장만 필터링
    def filter_shop(i):
        one_row = df[df['shop_id'] == i].head(1)
        if haversine(target_geo_list,
                     [one_row['lat'].head(1), one_row['lng'].head(1)]) <= 1:
            return i


    filtered_shop_list = list(filter(filter_shop, shop_list))
    # print(filtered_shop_list)


    # ================================
    # 기준점 내의 매장에 리뷰를 쓴 아이디 리스트 필터링

    user_list = []

    for shop in filtered_shop_list:
        nickname = df[df['shop_id'] == shop]['nickname'].tolist()
        user_list.append(nickname)

    # print(user_list)
    # flatten(1차원 리스트화)
    user_list = sum(user_list, [])
    # print(user_list)
    # print('--------------------------')
    # 중복 제거
    user_list = list(set(user_list))
    print('user count', len(user_list))
    # pdb.set_trace()
    try:
        user_list.remove(np.nan)
        user_list.remove('손님')
    except:
        '해당값이 없음'
    # print('===================')
    # print(user_list)
    # user_series = pd.Series(user_list)
    # user_series.to_csv('user_df(37.520775, 127.022767).csv', sep=',', encoding='utf-8-sig', index=False)

    # ================================
    # 파이참일 때
    # user_list = pd.read_csv('./../../user_df(37.520775, 127.022767).csv')

    # vscode일 때
    # user_list = pd.read_csv('./user_df(37.520775, 127.022767).csv')

    # print(user_list.head())
    # user_list = user_list['0'].tolist()
    # print(user_list)


    # userid pk생성을 위한 index count
    # count = 1439

    for user in user_list:
        # user DateFrame 생성
        # 유저 아이디 생성
        userid = f'user{str(count).zfill(6)}'
        lat = target_lat
        lng = target_lng
        addr = point_df.loc[idx]['addr']
        # 잘못한거지만 형식 남겨둠
        # lat = shop_df[shop_df['id'] == shop]['lat'].head(1).to_string(index=False)
        # lng = shop_df[shop_df['id'] == shop]['lng'].head(1).to_string(index=False)
        # addr = shop_df[shop_df['id'] == shop]['address'].head(1).to_string(index=False)
        _user_df = pd.DataFrame([[userid, "", userid, "", "", addr, lat, lng]], columns=user_columns)
        user_df = user_df.append(_user_df, ignore_index=True)
        for shop in filtered_shop_list:
            is_shop_user = (df['shop_id'] == shop) & (df['nickname'] == user)
            user_review_list = df[is_shop_user]
            if not user_review_list.empty:


                # index를 기준으로 review에 userid 추가/order_df data 생성
                for i in user_review_list.index:


                    food_name = df.loc[i, 'menu_summary']
                    # 메뉴명 누락(nan)인 경우 제외
                    try:
                        food_name = food_name.split('/')[0]
                    except:
                        print('메뉴명 누락(nan)')
                        food_name = ""


                    is_food_name = (food_df['shop_id'] == shop) & (food_df['food_name'] == food_name)
                    food_id = food_df[is_food_name]['food_id']
                    # food_id가 여러 개 검색되었을 경우 예외 처리
                    if len(food_id) > 1:
                        food_id = food_id.iloc[0]
                    else:
                        food_id = food_id.to_string(index=False)

                    # 해당 메뉴가 없을 경우 공백으로 처리
                    if food_id == 'Series([], )':
                        food_id = ""
                    # ===============================
                    # review DataFrame에 컬럼 추가
                    # print(i)
                    # print('food_id:', food_id)
                    df.loc[i, 'userid'] = userid
                    # print(df.loc[i])
                    df.loc[i, 'food_id'] = food_id

                    order_time = df.loc[i, 'time']
                    df.loc[i, 'order_time'] = order_time
                    # print(df.loc[i])
                    # pdb.set_trace()
                    # ===============================

        print(f'{idx}번째 지점, {count}번 완료')
        count += 1



    # print(user_df)
    # print(df)
    user_df.to_csv(f'user_df({target_lat}, {target_lng}).csv', sep=',', encoding='utf-8-sig', index=False)
    df.to_csv(r'./../../data/csv/important/review_df.csv', sep=',', encoding='utf-8-sig', index=False)



















