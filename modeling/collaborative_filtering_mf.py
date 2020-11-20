# -*- coding: utf-8 -*-
"""collaborative_filtering_MF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G_laEQEuYym9i7KOv8GJdFpQVSKJaGgG

# Matrix Factorization을 활용한 Collaborative Filtering

참고: https://skettee.github.io/post/latent_factor_model

## 데이터 전처리

- 데이터 수집
"""

from tensorflow.keras.utils import get_file
import os

zip_fname = 'ml-latest-small.zip'
data_dir = 'ml-latest-small'
ratings_fname = 'ratings.csv'
movies_fname = 'movies.csv'
origin = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
path = get_file(zip_fname, origin, extract=True)

path = path.replace(zip_fname, data_dir)

ratings_path = os.path.join(path, ratings_fname)
movies_path = os.path.join(path, movies_fname)

"""- csv 데이터셋을 dataframe으로 변환"""

import pandas as pd
import numpy as np

ratings_df = pd.read_csv(ratings_path)
print(ratings_df.shape)
ratings_df.head()

movies_df = pd.read_csv(movies_path)
movies_df.head()

"""- 이용자 수와 영화 수 체크"""

unique_user_list = ratings_df.userId.unique()
n_users = unique_user_list.shape[0]
# print(unique_user_list)
print('n_users:',n_users)

unique_movie_list = movies_df.movieId.unique()
n_movies = unique_movie_list.shape[0]
# print(unique_user_list)
print('n_movies:', n_movies)

"""- n번 사용자가 5개 별점을 준 영화 리스트"""

userId = 37 
rating = 5
top_movie_ids = ratings_df[(ratings_df['userId'] == userId) 
                          & (ratings_df['rating'] == rating)].movieId
top_titles = movies_df[movies_df['movieId'].isin(top_movie_ids)].title

print(f'Top rated titles of userId {userId}: \n')
for item in top_titles:
  print(item)

"""- 데이터 클렌징(Data Cleansing)"""

# Check missing data
print('missing number of userId data is ', ratings_df['userId'].isnull().sum())
print('missing number of movieId data is ', ratings_df['movieId'].isnull().sum())
print('missing number of rating data is ', ratings_df['rating'].isnull().sum())

"""- 데이터 분석(Data Analysis)"""

print('{} Ratings, {} Users, {} Movies'.format(len(ratings_df), 
                                               len(ratings_df.userId.unique()), 
                                               len(ratings_df.movieId.unique())))

"""- userId를 컬럼(Column), movieId를 열(Row)로 만들어서 rating값 확인"""

# stack()/unstack() 참조 https://rfriend.tistory.com/276
df_table = ratings_df.set_index(["movieId", "userId"]).unstack()
print(df_table.shape)
df_table.head()

"""- 데이터셋을 체크해보니 데이터가 너무 듬성듬성있음. 희소행렬(sparse matrix)임."""

df_table.iloc[808:817, 212:222].fillna("")

"""## 미니 데이터를 이용한 연습
  - 데이터셋 크기가 크면 핸들링이 어려우므로 우선 미니 데이터로 MF를 이용해서 잠재 인수(latent factor)를 구해보자
  - 별점 매트릭스를 R이라 하고 R (5X4) 매트릭스를 Q (5X2)와 PT (2X4) 매트릭스로 분해
"""

from sklearn.decomposition import NMF

R = [
     [5,5,1,1],
     [5,4,1,1],
     [5,5,1,1],
     [1,1,5,5],
     [1,1,5,4],
    ]

k = 2  # number of factors

model = NMF(n_components=k)
print('model:', model)

Q = model.fit_transform(np.array(R))
print('Q:', Q)
P = model.components_
print('P:', P)

"""- MF(행렬 인수분해)를 이용한 R 예측"""

R_hat = np.dot(Q, P)
print('R:', R)
print(pd.DataFrame(R_hat))

"""## Latent Factor(잠재 인수) 찾기

위 예제는 Dense Matrix(밀집행렬)을 이용했다. Sparse Matrix(희소행렬)을 이용하려면 어떻게 해야 할까

선형회귀(Linear regression) 방식
y^=wx+b를 정의하고
손실함수(Loss function) J(w,b)를 정의하고
경사하강법(Gradient descent)으로 손실값이 최소가 되는 w,b를 찾음

이것을 잠재 인수 찾기에 활용

r^=q⋅pT를 정의하고
손실함수(Loss function) J(p,q)를 정의하고
경사하강법(Gradient descent)으로 손실값이 최소가 되는 p,q를 찾음

### keras를 이용한 미니 모델링
"""

import pandas as pd
import numpy as np

data = [
    ['Alice', 'Beauty Inside', 5],
    ['Alice', 'La La Land', 5],
    ['Alice', 'Love Story', 5],
    ['Alice', 'Matrix', 1],
    ['Alice', 'Star Wars', 1], 
    ['Bob', 'La La Land', 4],
    ['Bob', 'Love Story', 5],
    ['Bob', 'Matrix', 1],
    ['Bob', 'Star Wars', 1],
    ['Carol', 'Beauty Inside', 1],
    ['Carol', 'La La Land', 1],
    ['Carol', 'Matrix', 5],
    ['Carol', 'Star Wars', 5], 
    ['Dave', 'Beauty Inside', 1], 
    ['Dave', 'La La Land', 1],
    ['Dave', 'Love Story', 1],
    ['Dave', 'Matrix', 5],
    ['Dave', 'Star Wars', 4],
]

mini_df = pd.DataFrame( data=data, columns=['user', 'item', 'rating'])
mini_df

"""- pd.pivot_table을 이용해서 item * user 테이블 생성해서 내용 확인"""

df_table = pd.pivot_table(mini_df, index='item', columns='user',  values='rating', fill_value='')
df_table

"""- 데이터 변환(Data Transformation)
  - 벡터화 연산을 위해 문자열을 숫자로 변환 필요

- 유저를 숫자로 변환
"""

mini_df.user = mini_df.user.astype('category').cat.codes.values
mini_df

"""- 영화 제목을 숫자로 변환"""

mini_df.item = mini_df.item.astype('category').cat.codes.values
print(mini_df.item)
print(mini_df.shape)
mini_df

"""### 임베딩(Embedding)

- 잠재 인수(Latent factor)의 모양(Shape)를 정의하고 모델에 삽입하는 것
- 임베딩(Embedding)된 값들은 모델이 훈련되면서 학습됨
- 손실함수(Loss function)가 최저값을 찾아가는 과정에서 최적의 값으로 자동으로 세팅
"""

from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, dot
from tensorflow.keras import regularizers

# input tensor
item_input = Input(shape=[1]) # mini_df.item: 숫자로 인코딩된 벡터 형태
user_input = Input(shape=[1]) # mini_df.user

n_items = len(mini_df.item.unique()) # 영화 5편
n_items_latent_factors = 2 # 영화의 잠재 인수 갯수

n_users = len(mini_df.user.unique()) # 사용자 4명 
n_users_latent_factors = 2 # 유저의 잠재 인수 갯수

"""- regularizer
  - 참고: https://wdprogrammer.tistory.com/33
  - 과대적합을 피하는 처리 과정
  - L2 regularization(=weight decay) : 가중치의 제곱에 비례하는 비용이 추가됨(가중치의 L2 norm)
"""

# Item latent factor
item_embedding = Embedding(n_items, n_items_latent_factors, # (5X2) Latent factor
                           embeddings_regularizer=regularizers.l2(0.001),
                           name='item_embedding')(item_input)
# User latent factor
user_embedding = Embedding(n_users, n_users_latent_factors, # (4X2) Latent factor
                           embeddings_regularizer=regularizers.l2(0.001),
                           name='user_embedding')(user_input)
print(item_embedding)

"""- 벡터화 (Flatten)
  - 2D로 되어 있는 임베딩(Embedding)을 1D로 변환한다. 이것을 잠재 벡터(Latent vector) 라고 함
"""

# Item latent vector
item_vec = Flatten()(item_embedding)
# User latent vector
user_vec = Flatten()(user_embedding)
print(item_vec)

"""### 미니 모델링 (Modeling)

- R^=Q⋅PT
손실 함수(Loss function)는 평균 제곱 오차(mean-squared error)를 사용
- 최적화(Optimizer)는 경사하강법(gradient descent)을 사용. 정확히는 sgd(stocastic  Gradient Descent,확률적 경사 하강법)
"""

r_hat = dot([item_vec, user_vec], axes=-1)
mini_model = Model([user_input, item_input], r_hat)
mini_model.compile(optimizer = 'sgd', loss = 'mean_squared_error')

"""### 미니 모델 훈련(Train Model)

- optimizer에 따른 loss (epochs=2000)
  - sgd: 0.07310202717781067
  - RMSprops: 0.07310551404953003
  - Adagrad: 0.07310205698013306
  - Adadelta: 0.07310205698013306
  - Adam: 0.07310204207897186
  - Adamax: 0.07310204207897186
  - Nadam: 0.07310382276773453
- 미세하게 adma이 가장 loss가 적다
- 다시 돌려보니 sgd가 더 나은 결과가 나옴
"""

hist = mini_model.fit([mini_df.user, mini_df.item], mini_df.rating, epochs=2000, verbose=0) 
print(hist.history['loss'][-1])  # 학습 후 가장 마지막 loss값 출력

# matplotlib inline
import matplotlib.pyplot as plt

plt.plot(hist.history['loss'])
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

"""### 미니 예측 (Predict)

- latent factor matrix 다시 결합하여 예측 메트릭스를 생성
"""

# 학습한 모델에서 가중치 행렬을 얻고 array로 리턴되므로 0번째 인덱스를 호출
Q = mini_model.get_layer(name='item_embedding').get_weights()[0]
P = mini_model.get_layer(name='user_embedding').get_weights()[0]
P_t = np.transpose(P)

R_hat = np.dot(Q, P_t)
pd.DataFrame(R_hat)

"""## 잠재 인수 모델링(Latent Factor Modeling) 정리 및 예제

### 정리
1. Item, User 값을 인덱스 값으로 변환한다.
2. 잠재 인수(Latent factor)의 개수를 정한다.
3. 잠재 인수(Latent factor)를 임베딩(Embedding) 한다.
4. 벡터화(Flatten) 해서 잠재 벡터(Latent vector)로 변환한다.
5. R^를 Item과 User의 잠재 벡터의 내적(dot) 으로 설정한다.
6. 손실 함수 (Loss function)를 정의한다. 여기서는 평균 제곱 오차(mean squared error) 를 사용한다.
7. 옵티마이저(Optimizer)를 정의한다. 여기서는 Adam 을 사용한다.
8. 반복할 회수(epoch)를 결정한다.
9. 주어진 조건으로 모델을 최적화(fit) 시킨다.

### 케라스(Keras)로 모델링(Modeling)

- 데이터 변환
  - userId와 movieId를 숫자로 변환(인코딩)함
"""

# Indexing userId and movieId
users = ratings_df.userId.unique()
print(len(users))
movies = ratings_df.movieId.unique()
print(len(movies))
print(ratings_df.head())

userid2idx = {o:i for i,o in enumerate(users)}
movieid2idx = {o:i for i,o in enumerate(movies)}

ratings_df['userId'] = ratings_df['userId'].apply(lambda x: userid2idx[x])
ratings_df['movieId'] = ratings_df['movieId'].apply(lambda x: movieid2idx[x])

"""- 훈련, 테스트 데이터 분할"""

# Split train and test data
split = np.random.rand(len(ratings_df)) < 0.8
print(split)

train_df = ratings_df[split]
test_df = ratings_df[~split]

print('shape of train data is ',train_df.shape)
print('shape of test data is ',test_df.shape)

"""- 임베딩(Embedding)
  - 잠재 인수 개수를 64개로 설정
"""

n_movies = len(ratings_df.movieId.unique())
n_users = len(ratings_df.userId.unique())
n_latent_factors = 64

movie_input = Input(shape=[1])
# Item latent factor
movie_embedding = Embedding(n_movies, n_latent_factors,
                            embeddings_regularizer=regularizers.l2(0.00001), 
                            name='movie_embedding')(movie_input)

user_input = Input(shape=[1])
# User latent factor
user_embedding = Embedding(n_users, n_latent_factors,
                           embeddings_regularizer=regularizers.l2(0.00001),
                           name='user_embedding')(user_input)

"""- 벡터화(Flatten)"""

# Item latent vector
movie_vec = Flatten()(movie_embedding)
# User latent vector
user_vec = Flatten()(user_embedding)

"""- 모델링(Modeling)"""

r_hat = dot([movie_vec, user_vec], axes=-1)
model = Model([user_input, movie_input], r_hat)
model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])

"""- 모델 훈련(Train Model)"""

# Commented out IPython magic to ensure Python compatibility.
hist = model.fit([train_df.userId, train_df.movieId], train_df.rating, validation_split=0.1,
                 batch_size=128, epochs=50, verbose=1) 
print(hist.history.keys())
print('train loss: ', hist.history['loss'][-1])
print('train acc: ', hist.history['accuracy'][-1])
print('val acc: ', hist.history['val_loss'][-1])
print('val acc: ', hist.history['val_accuracy'][-1])


# %matplotlib inline
import matplotlib.pyplot as plt

plt.plot(hist.history['val_loss'])
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

"""- 모델 평가(Test Model)"""

test_loss = model.evaluate([test_df.userId, test_df.movieId], test_df.rating)

print('test loss: ', test_loss)

"""- ## 학습된 머신을 활용한 예측"""

pd.options.display.float_format = '{:.2f}'.format  # 출력 포매팅 설정
ratings_df[(ratings_df['userId'] == 249) & (ratings_df['movieId'] == 70)]
movies_df['movieId'].head(575)
ratings_df.loc[7000]

userId = 31       # 1 ~ 610
movieId = 165  # 1 ~ 193609  # sparse하고 ratings_df와 모두 대응되지도 않음
movie_title = list(movies_df[movies_df['movieId']== movieId].title)[0]

user_v = np.expand_dims(userid2idx[userId], 0)
movie_v = np.expand_dims(movieid2idx[movieId], 0)
predict = model.predict([user_v, movie_v])

print('영화 {} 에 대한 사용자 ID {}님의 예상 별점은 {:.1f} 입니다.'.format(movie_title, userId, predict[0][0]))