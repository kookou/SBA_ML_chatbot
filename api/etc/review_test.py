import pandas as pd

##################################
# 구별 점포 갯수 뽑기

# csv파일 불러옴
# file_path = r'./../../data/csv/store.csv'
# df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')


# print(df[['id', 'address']])
#
# gu_list = ["강남구", "강동구", "강서구", "강북구", "관악구", '광진구', '구로구',
#            '금천구', '노원구', '동대문구', '도봉구', '동작구', '마포구' ,'서대문구',
#            '성동구', '성북구', '서초구', '송파구', '영등포구', '용산구', '양천구',
#            '은평구', '종로구', '중구', '중랑구']
#
# print(gu_list)
# gu_len_list = []
# for item in gu_list:
#     gu_len_list.append({item: len(df[df['address'].str.contains(item)])})
#
# print(gu_len_list)
##################################

# 강남구 점포 아이디 추출
file_path = r'./../../data/csv/store.csv'
df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')

gangnam_store_list = df[df['address'].str.contains('강남구')]['id'].tolist()

print(gangnam_store_list)

file_path = r'./../../data/csv/review.csv'
df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')

gangnam_review_list = pd.DataFrame()

for item in gangnam_store_list:
    gangnam_review_list = gangnam_review_list.append(df[df['storeid'] == int(item)])

print(len(gangnam_review_list))
print(gangnam_review_list)