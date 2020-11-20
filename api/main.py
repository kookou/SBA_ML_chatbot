from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
from chatbot_api.ext.db import url, db, openSession
from chatbot_api.resources import user
from chatbot_api.resources.user import UserDto
from chatbot_api.resources.food import FoodDto
from chatbot_api.resources.order_review import OrderReviewDto
import numpy as np
import pandas as pd
print('========== url ==========')
print(url)
import secrets

app = Flask(__name__)

# 세션을 위한 키 설정
# app.config["SECRET_KEY"] = "secretkeyforsession"
# SECRET_KEY = "secretkeyforsession"
# SESSION_TYPE = 'filesystem'
app.secret_key = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
CORS(app, supports_credentials=True, resources={r'/*': {"origins": "*"}})
# CORS(app, resources={r"/api/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config [ 'CORS_HEADERS' ]  =  'Content-Type'
db.init_app(app)
api = Api(app)

'''
@app.before_first_request
def create_tables():
    db.create_all()
with app.app_context():
    db.create_all()
'''

# 테이블 일괄 생성
with app.app_context():
    from chatbot_api.ext.routes import initialize_routes  # db에서 sql를 첫 로딩시 실행하기 위한 임시 방편.. 모듈 로딩 관련
    db.create_all()


# with app.app_context():
#     count = UserDao.count()
#     print(f'Users Total Count is {count}')
#     if count == 0:
#         UserDao.insert_many()


initialize_routes(api)


# @app.route('/api/test')
# def test():
#     return {'test': 'Success'}

# context 생성
# app.app_context().push()

# 유저 추가 (create)
# user = UserDto(userid='tom', password='1', name='tom', addr="서울시 서초구", lat=37.1234, lng=128.1234)
# UserDao.add(user)

# 유저 조회
# 전체 조회
# user_list = UserDao.find_all()
# print(user_list)
# print(type(user_list))  # <class 'list'>
# print(user_list[0])
# print(type(user_list[0]))

# ###################################
# # 데이터 일괄 입력

# import pdb
# food/order_review 테이블 데이터 일괄 입력
def insert_at_all(fila_name, dto):
    chunksize = 10 ** 4
    # for cnt, chunk in enumerate(pd.read_csv(f'./data/db/{fila_name}.csv', sep=',', encoding='utf-8-sig', chunksize=chunksize)): # 혜정
    for cnt, chunk in enumerate(pd.read_csv(f'./data/csv/important/db/{fila_name}.csv', sep=',', encoding='utf-8-sig', chunksize=chunksize)): # 영돈
        df = chunk.replace(np.nan, 1, regex=True)
        # print(df.head())

        Session = openSession()
        session = Session()
        session.bulk_insert_mappings(dto, df.to_dict(orient="records"))
        session.commit()
        session.close()
        print(f'{cnt*chunksize}건 입력 완료')


# food 테이블 입력
# insert_at_all('food', FoodDto)        
# order_review 테이블 입력
# insert_at_all('order_review(remove_userid_nan)', OrderReviewDto)        


# shop_seoul = df.loc[df['shop_addr'].str.contains('서울', na=False)]
# print(shop_seoul['shop_addr'])

# shop_seoul.to_csv('./data/csv/important/shop(seoul).csv', sep=',', encoding='utf-8-sig', index=False)

# pdb.set_trace()
# ####################################

# 캐스케이딩 삭제 테스트
# with app.app_context():
#     # db.session.query(ShopDto).filter(ShopDto.shop_id==117).delete()
#     user = db.session.query(ShopDto).filter(ShopDto.shop_id==117).first()
#     db.session.delete(user)
#     db.session.commit()
#     db.session.close()


