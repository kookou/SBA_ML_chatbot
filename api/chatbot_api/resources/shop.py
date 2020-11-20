# from sqlalchemy import Column, Integer, Float, String, ForeignKey, create_engine
# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
from typing import List
from flask import request, session
from flask_restful import Resource, reqparse
from flask import jsonify
import json
import os
import numpy as np
import pandas as pd
from sqlalchemy import or_


from sklearn.ensemble import RandomForestClassifier  # rforest
from sklearn.tree import DecisionTreeClassifier  # dtree
from sklearn.ensemble import RandomForestClassifier  # rforest
from sklearn.naive_bayes import GaussianNB  # nb
from sklearn.neighbors import KNeighborsClassifier  # knn
from sklearn.svm import SVC  # svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold  # k value is understood as count
from sklearn.model_selection import cross_val_score
from pathlib import Path

from chatbot_api.ext.db import db, openSession
from chatbot_api.util.file_handler import FileReader

from chatbot_api.resources.food import FoodDto, FoodDao
from chatbot_api.resources.user import UserDao, UserDto
from chatbot_api.resources.order_review import OrderReviewDto, OrderReviewDao
from chatbot_api.ext.model import df_shop, predict_shop, df_food, predict_food

from haversine import haversine
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.sql.expression import cast
from sqlalchemy.sql.sqltypes import Float

parser = reqparse.RequestParser()
parser.add_argument('shop_id', type=str, required=True)
parser.add_argument('cat_id', type=str, required=True)
parser.add_argument('key', type=str, required=True)

class ShopDto(db.Model):
    __tablename__ = "shop"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 한글 인코딩

    shop_id: int = db.Column(db.Integer, primary_key=True, index=True)
    shop_name: str = db.Column(db.String(30))
    shop_addr: str = db.Column(db.String(100))
    shop_img: str = db.Column(db.String(200), default='shop_default.png')
    cat: str = db.Column(db.String(100))
    shop_lat: float = db.Column(db.Float)
    shop_lng: float = db.Column(db.Float)
    shop_rev_avg: float = db.Column(db.Float)
    shop_rev_cnt: int = db.Column(db.Integer)
    open_time: str = db.Column(db.String(30))

    foods = db.relationship('FoodDto', backref='shop', lazy='dynamic', cascade="all, delete, delete-orphan")
    order_reviews = db.relationship('OrderReviewDto', backref='shop', lazy='dynamic', cascade="all, delete, delete-orphan")
    

    def __init__(self, shop_id, shop_name, shop_addr, shop_img, cat,
                 shop_lat, shop_lng, shop_rev_avg, shop_rev_cnt, open_time):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.shop_addr = shop_addr
        self.shop_img = shop_img
        self.cat = cat
        self.shop_lat = shop_lat
        self.shop_lng = shop_lng
        self.shop_rev_avg = shop_rev_avg
        self.shop_rev_cnt = shop_rev_cnt
        self.open_time =open_time

    def __repr__(self):
        return f'Shop(shop_id={self.shop_id}, shop_name={self.shop_name}, ' \
               f'shop_addr={self.shop_addr}, ,shop_img={self.shop_img}, cat={self.cat},' \
               f'shop_lat={self.shop_lat}, shop_lng="{self.shop_lng}"' \
               f'shopt_rev_avg={self.shop_rev_avg}, shop_rev_cnt={self.shop_rev_cnt}' \
               f'open_time={self.open_time}'

    @property
    def json(self):
        return {
            'shop_id': self.shop_id,
            'shop_name': self.shop_name,
            'shop_addr': self.shop_addr,
            'shop_img': self.shop_img,
            'cat': self.cat,
            'shop_lat': self.shop_lat,
            'shop_lng': self.shop_lng,
            'shop_rev_avg': self.shop_rev_avg,
            'shop_rev_cnt': self.shop_rev_cnt,
            'open_time': self.open_time
        }
    # 동적 컬럼 추가 실패
    # @hybrid_property
    # def dist(self):

    #     user_location = (session['user']['lat'], session['user']['lng'])

    #     return haversine((self.shop_lat, self.shop_lng), user_location)
    
    # @dist.expression
    # def dist(cls):
    #     user_location = (session['user']['lat'], session['user']['lng'])
    #     return haversine((cast(cls.shop_lat, sqlalchemy.Float), cast(cls.shop_lng, sqlalchemy.Float)), user_location)


class ShopVo:
    shop_id: int = 0
    shop_name: str = ''
    shop_addr: str = ''
    shop_img: str = ''
    cat: str = ''
    shop_lat: float = 0.0
    shop_lng: float = 0.0
    shop_rev_avg: float = 0.0 
    shop_rev_cnt: int = 0
    open_time: str = ''

class ShopDao(ShopDto):
    
    @classmethod
    def find_all(cls):
        from chatbot_api.resources.food import FoodDto
        sql = db.session.query(ShopDto, FoodDto).\
                filter(ShopDto.shop_id == FoodDto.shop_id).\
                order_by(ShopDto.shop_rev_cnt.desc()).\
                group_by(ShopDto.shop_id)

        df = pd.read_sql(sql.statement, sql.session.bind)  

        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        df = df.head(200) # 로딩이 길어서 임시적으로 일부만 표시
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_shopid(cls, shop_id):
        sql = db.session.query(ShopDto, FoodDto).\
        filter(ShopDto.shop_id == FoodDto.shop_id).\
        filter(ShopDto.shop_id == shop_id).limit(1)        
        df = pd.read_sql(sql.statement, sql.session.bind)
        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        return json.loads(df.to_json(orient='records'))
        # return cls.query.filter_by(shop_id = shopid).all()


        # sql = cls.query.filter_by(shop_id = shop_id)
        # df = pd.read_sql(sql.statement, sql.session.bind)
        # return json.loads(df.to_json(orient='records'))
        # # return cls.query.filter_by(shop_id = shopid).all()


    @classmethod
    def find_limit(cls):
        # sql = cls.query.join(FoodDto).filter(FoodDto.shop_id == cls.shop_id).all()
        sql = cls.query
        # print(type(sql))
        # print('**************test******************')
        df = pd.read_sql(sql.statement, sql.session.bind)
        df = df.head(50)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_cat(cls,cat_id):
        from chatbot_api.resources.food import FoodDto
        print(cat_id)

        user_location = (session['user']['lat'], session['user']['lng'])

        sql = db.session.query(ShopDto, FoodDto).\
                filter(ShopDto.shop_id == FoodDto.shop_id).\
                filter(ShopDto.cat.like('%'+cat_id+'%')).\
                filter(func.mychatbot.dist(ShopDto.shop_lat, ShopDto.shop_lng,
                user_location[0], user_location[1]) <= 1).\
                order_by(ShopDto.shop_rev_cnt.desc()).\
                group_by(ShopDto.shop_id)
        df = pd.read_sql(sql.statement, sql.session.bind)
        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        print('*********')
        print(df)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def search(cls,key):
        from chatbot_api.resources.food import FoodDto
        # sql = cls.query.filter(ShopDto.shop_name.like('%'+key+'%'))
        # df = pd.read_sql(sql.statement,sql.session.bind)
        
        user_location = (session['user']['lat'], session['user']['lng'])

        sql = db.session.query(ShopDto, FoodDto).\
            filter(ShopDto.shop_id == FoodDto.shop_id).\
            filter(or_(ShopDto.shop_name.like('%'+key+'%'),
            FoodDto.food_name.like('%'+key+'%'))).\
            filter(func.mychatbot.dist(ShopDto.shop_lat, ShopDto.shop_lng,
            user_location[0], user_location[1]) <= 1).\
            order_by(ShopDto.shop_rev_cnt.desc()).\
            group_by(ShopDto.shop_id)       

        # sql = cls.query(ShopDto, FoodDto).from_statement(\
        #     "select * from shop s join food f on s.shop_id = f.shop_id where shop_name like :'%'key'%' or food_name like:'%'key'%' group by s.shop_id").\
        #         params(key=key)

        df = pd.read_sql(sql.statement,sql.session.bind)
        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        # print(df)

        return json.loads(df.to_json(orient='records'))

# ==============================================================
# ==============================================================
# =====================   Service   ============================
# ==============================================================
# ==============================================================

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import load_model

from surprise import dump

class ShopService:

    @staticmethod
    def load_model_from_file():
        fname = r'./modeling/recommender_mf.h5'
        model = load_model(fname)
        return model

    @staticmethod
    def shop_rev_predict_by_keras(model, userid, shop_id):
        
        userid = int(userid.lstrip('user'))
        predict = model.predict([np.array([userid]), np.array([shop_id])])
        return predict[0][0]

    @staticmethod
    def shop_rev_predict_by_surprise(shops_dict):
        shops_dict_ = shops_dict

        for i, row in enumerate(shops_dict_):
            # userid = int((session['user']['userid']).lstrip('user'))
            userid = session['user']['userid']
            shop_id = row['shop_id']

            predict = predict_shop(userid, shop_id) # 인자를 string으로 넣어야 한다고 함
            # 가게에 대한 유저의 평균평점을 불러와야 하는데, 복잡한 관계로 임시적으로 model 모듈에서 생성한 df를 활용
            df_ = df_shop[(df_shop['userid'] == userid) & (df_shop['shop_id'] == shop_id)]

            
            if df_['rating'].values.any():   # 유저가 입력한 평점이 있으면
                 shops_dict[i]['shop_user_avg'] = round(np.float(df_['rating'].values), 1)

            shops_dict[i]['shop_pred_avg'] = round(float(predict[3]), 1)
                          
        return shops_dict

    @staticmethod
    def food_rev_predict_by_surprise(food_dict):
        food_dict_ = food_dict

        for i, row in enumerate(food_dict_):
            # userid = int((session['user']['userid']).lstrip('user'))
            userid = session['user']['userid']
            food_id = row['food_id']

            predict = predict_food(userid, food_id) # 인자를 string으로 넣어야 한다고 함
            # 가게에 대한 유저의 평균평점을 불러와야 하는데, 복잡한 관계로 임시적으로 model 모듈에서 생성한 df를 활용
            df_ = df_food[(df_food['userid'] == userid) & (df_food['food_id'] == food_id)]
            
            if df_['rating'].values.any():   # 유저가 입력한 평점이 있으면
                 food_dict[i]['food_user_avg'] = round(np.float(df_['rating'].values), 1)

            food_dict[i]['food_pred_avg'] = round(float(predict[3]), 1)
                          
        return food_dict

# ==============================================================
# ==============================================================
# =====================   Controller   =========================
# ==============================================================
# ==============================================================

class Shops(Resource):

    @staticmethod
    def get():
        print('select all')
        shops = ShopDao.find_all()
        # print('shops: ', shops)
        # test = ShopDao.find_cat()
        # print("-------------shops-----------------")
        # print(type(shops))
        # print(shops)
        shops = ShopService.shop_rev_predict_by_surprise(shops)
        return shops, 200

class Shopscat(Resource):

    # keras로 만든 mf모델
    # @staticmethod
    # def get(cat_id : str):
    #     print('select catid : ' + cat_id)
    #     shopscat = ShopDao.find_by_cat(cat_id)
    #     model = UserService.load_model_from_file()
    #     shopscat_ = shopscat
    #     for i, row in enumerate(shopscat_):
    #         userid = session['userid']
    #         shop_id = row['shop_id']
    #         predict = ShopService.shop_rev_predict_by_keras(model, userid, shop_id)
    #         shopscat[i]['shop_pred_avg'] = round(float(predict), 1)

    #     return shopscat, 200

    # surprise로 만든 svd모델
    @staticmethod
    def get(cat_id : str):
        print('select catid : ' + cat_id)
        shopscat = ShopDao.find_by_cat(cat_id)

        shopscat = ShopService.shop_rev_predict_by_surprise(shopscat)

        return shopscat, 200


class Shop(Resource):
    
    @staticmethod
    def get(shop_id : str):
    
        shopAfoodAreview = []
        shop_dict = {'Shop' : ShopDao.find_by_shopid(shop_id)}

        food = FoodDao.food_find_by_shopid(shop_id)
        # 음식 예상 평점 키/값 입력
        food = ShopService.food_rev_predict_by_surprise(food)
        food_dict = {'Food' : food}

        review_dict = {'Review' : OrderReviewDao.review_find_by_shopid(shop_id)}
        shopAfoodAreview.append(shop_dict)
        shopAfoodAreview.append(food_dict)
        shopAfoodAreview.append(review_dict)
        print('*'*40)
        # print(shop)
        # shop = shop.json()
        # print(shop)
        # print(type(shopAfood))    
        # print(shopAfoodAreview[2])
        return shopAfoodAreview, 200



class ShopSearch(Resource):
    # keras 모델 적용
    # @staticmethod
    # def get(key : str):
    #     print("search",key)
    #     search = ShopDao.search(key)
    #     model = UserService.load_model_from_file()
    #     shopscat_ = search
    #     for i, row in enumerate(shopscat_):
    #         userid = session['userid']
    #         shop_id = row['shop_id']
    #         predict = ShopService.shop_rev_predict(model, userid, shop_id)
    #         search[i]['shop_pred_avg'] = round(float(predict), 1)

    #     return search, 200

    # surprise 모델 적용
    @staticmethod
    def get(key : str):
        print("search",key)
        search = ShopDao.search(key)
        search = ShopService.shop_rev_predict_by_surprise(search)

        return search, 200        


# ------------ 실행 영역 --------------
if __name__ == '__main__':

    # import pdb
    # 데이터 일괄 입력
    # df = pd.read_csv('./data/db/shop.csv', sep=',', encoding='utf-8-sig') # 혜정
    df = pd.read_csv('./data/csv/important/db/shop.csv', sep=',', encoding='utf-8-sig') # 영돈
    df = df.replace(np.nan, '', regex=True)

    # ------------------
    # 서울만 임시로 넣었을 때 사용
    # shop_seoul = df.loc[df['shop_addr'].str.contains('서울', na=False)]
    # print(shop_seoul['shop_addr'])

    # shop_seoul.to_csv('./data/csv/important/shop(seoul).csv', sep=',', encoding='utf-8-sig', index=False)

    # pdb.set_trace()
    # -------------------


    Session = openSession()
    session = Session()
    session.bulk_insert_mappings(ShopDto, df.to_dict(orient="records"))
    session.commit()
    session.close()