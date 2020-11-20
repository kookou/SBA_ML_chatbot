import numpy as np
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise import Trainset
from surprise import dump
from surprise.model_selection import cross_validate
from surprise import NormalPredictor
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import KNNWithZScore
from surprise import KNNBaseline
from surprise import SVD
from surprise import BaselineOnly
from surprise import SVDpp
from surprise import NMF
from surprise import SlopeOne
from surprise import CoClustering
from surprise.accuracy import rmse
from surprise import accuracy
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import train_test_split

"""## 데이터 전처리

- 데이터 임포트
"""

df = pd.read_csv("../data/csv/important/db/order_review(remove_userid_nan).csv", sep=",", encoding='utf-8-sig', error_bad_lines=False, engine="python")

print(df.shape)
print(df.head())

"""- 필요한 컬럼만 추출"""

df = df[['userid', 'shop_id', 'taste_rate', 'quantity_rate', 'delivery_rate']]
print(df)

"""- 합계 평점 컬럼 생성"""

df['rating'] = (df['taste_rate'] + df['quantity_rate'] + df['delivery_rate'])/3
print(df.head())

"""- 세부 평점 컬럼 제거"""

df = df[['userid', 'shop_id', 'rating']]
print(df.head())

"""- 정렬"""

df_sort = df.sort_values(by=['userid', 'shop_id'], axis=0)


"""- 유저 리스트가 몇몇 부분 연속되어 있지 않은 것 확인"""

# unique_user_list = df.userid.unique()
# n_users = unique_user_list.shape[0]
# np.set_printoptions(threshold=np.inf)
# print(np.sort(unique_user_list))
# n_users

"""- 그룹화"""

# groupby_df = df_sort.groupby(["userid", 'shop_id'])  # groupby 객체 상태
df_group = df_sort.groupby(["userid", 'shop_id']).mean()  # groupby 객체 상태
df = df_group.reset_index()  # reset_index를 해주면 dataframe 객체가 됨
print(df.shape)
''' 예측값과 비교할 때 사용할 실제값 dataframe'''
df_backup = df
print(df)

# df = groupby_df.head()  # 이유는 모르겠지만 head를 붙였더니 dataframe화 되었음 -> 실수로 인한 잘못된 해결챇
# print(df)


"""- 평점이 0인 항목을 제거"""

df = df.loc[(df.rating != 0)]
print(df)

"""- 잘 변경 되었는지 확인"""

df1 = df[df['rating'] == 0]
print(df1)

"""- shop_id가 nan인 컬럼 제거 위해 확인"""

# Check missing data
print('missing number of userid data is ', df['userid'].isnull().sum())
print('missing number of food_id data is ', df['shop_id'].isnull().sum())
print('missing number of rating data is ', df['rating'].isnull().sum())

"""- 유저 리스트 및 유저 수
    - 주의: 일부 유저 연번은 데이터 처리 과정에서 업데이트되어 리뷰 데이터가 없어졌음.
"""

unique_user_list = df.userid.unique()
n_users = unique_user_list.shape[0]
print(unique_user_list)
print(n_users)

"""- 매장 리스트 및 매장 수 조회"""

unique_shop_list = df.shop_id.unique()
n_shops = unique_shop_list.shape[0]
print(unique_shop_list)
print(n_shops)

"""### 데이터 변환(Data Transformation)
- 벡터화 연산을 위해 문자열을 숫자로 변환 필요

- 유저를 숫자로 변환
"""

# df.userid = df.userid.astype('category').cat.codes.values  # 향후 확인을 위해 이 방식보다는 map을 사용해야 함
df['userid'] = df['userid'].map(lambda x: int(x.lstrip('user')))
print(df)

df.to_csv('model_df.csv', header=False, index=False)

# # ###############################
df_ = df[(df['userid'] == 777) & (df['shop_id'] == 472464)]
print(df_)
# import pdb
# pdb.set_trace()

"""
데이터 로딩
surprise data형식에 맞춰 dataframe 변환
"""
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df((df[['userid', 'shop_id', 'rating']]), reader=reader)
# train, test = train_test_split(data, test_size=0.25, random_state=42)
trainset = data.build_full_trainset()

"""
모델 설정 및 학습
"""

# model = SVD()
# cross_validate(model, data, measures=['rmse', 'mae'], cv=5, verbose=True)
# model.fit(trainset)

# 전체 데이터셋을 학습
model = SVD(n_factors=64, n_epochs=20, random_state=42)
model.fit(trainset)



"""
예측 및 평가
"""

testset = Trainset.build_testset(trainset)
prediction_list = model.test(testset)
print(prediction_list[:50])
print(len(prediction_list))
# for i in range(10):
#     pred = model.predict(112, 260443+i)
#     print(pred)
# pred = model.predict(112, 260443)
# print(pred)
pred = model.predict(11366, 279569)
print(pred)
pred = model.predict(str(200000), str(279569))
print(pred)
# pred = model.predict(112, 260445)
# print(pred)
# dump.dump('surprise_svd', predictions=prediction_list, algo=None, verbose=1)
#
# loaded_model = dump.load('surprise_svd')
#
# print(loaded_model[0])





