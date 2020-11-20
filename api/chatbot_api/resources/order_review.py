# from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, create_engine
# from sqlalchemy import Column, Integer, Float, String, ForeignKey, create_engine
# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT

from flask import request
from flask_restful import Resource, reqparse
from flask import jsonify
import json
import os
import numpy as np
import pandas as pd

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


# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
parser = reqparse.RequestParser()
parser.add_argument('food_id', type=str, required=True)
parser.add_argument('or_id', type=str, required=True)

class OrderReviewDto(db.Model):
    __tablename__ = "order_review"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 한글 인코딩

    or_id: int = db.Column(db.Integer, primary_key=True, index=True)
    order_time: str = db.Column(db.Date)
    review_cmnt: str = db.Column(db.Text)
    taste_rate: float = db.Column(db.Float)
    quantity_rate: float = db.Column(db.Float)
    delivery_rate: float = db.Column(db.Float)
    review_time: str = db.Column(db.Date)
    review_img: str = db.Column(db.String(300))
    owner_cmnt: str = db.Column(db.Text)

    userid: str = db.Column(db.String(20), db.ForeignKey('user.userid', ondelete="CASCADE"))
    shop_id: int = db.Column(db.Integer, db.ForeignKey('shop.shop_id', ondelete="CASCADE"))
    food_id: int = db.Column(db.Integer, db.ForeignKey('food.food_id', ondelete="CASCADE")) 

    foods = db.relationship('FoodDto', back_populates='order_reviews')

    # self.or_id = or_id
    def __init__(self, order_time=-1, userid='', shop_id=-1, food_id=-1, review_cmnt='', taste_rate=0.0, quantity_rate=0.0,
                 delivery_rate=0.0, review_time=0.0, review_img='', owner_cmnt=1):
        
        self.order_time = order_time
        self.review_cmnt = review_cmnt
        self.taste_rate = taste_rate
        self.quantity_rate = quantity_rate
        self.delivery_rate = delivery_rate
        self.review_time = review_time
        self.review_img = review_img
        self.owner_cmnt = owner_cmnt
        self.userid = userid
        self.shop_id = shop_id
        self.food_id = food_id
        

    def __repr__(self):
        return f'OrderReview(or_id={self.or_id}, ' \
               f'order_time={self.order_time}, ' \
               f'review_cmnt={self.review_cmnt}, ' \
               f'taste_rate={self.taste_rate}, ' \
               f'quantity_rate={self.quantity_rate}, ' \
               f'delivery_rate={self.delivery_rate}, ' \
               f'review_time="{self.review_time}" ' \
               f'review_img={self.review_img}, ' \
               f'owner_cmnt={self.owner_cmnt}, ' \
               f'userid={self.userid}, ' \
               f'shop_id={self.shop_id} ' \
               f'food_id={self.food_id}) ' \


    @property
    def json(self):
        return {
            'or_id': self.or_id,
            'order_time': self.order_time,
            'review_cmnt': self.review_cmnt,
            'taste_rate': self.taste_rate,
            'quantity_rate': self.quantity_rate,
            'delivery_rate': self.delivery_rate,
            'review_time': self.review_time,
            'review_img': self.review_img,
            'owner_cmnt': self.owner_cmnt,
            'userid': self.userid,
            'shop_id': self.shop_id,
            'food_id': self.food_id,
        }

class OrderReviewVo:
    or_id: int = 0
    order_time: str = ''
    review_cmnt: str = ''
    taste_rate: float = 0.0
    quantity_rate: float = 0.0
    delivery_rate: float = 0.0
    review_time: str = ''
    review_img: str = ''
    owner_cmnt: str = ''

    userid: str = ''
    shop_id: int = 0
    food_id: int = 0


class OrderReviewDao(OrderReviewDto):

    @classmethod
    def review_find_by_shopid(cls,shop_id):
        from chatbot_api.resources.food import FoodDto # 주의! 여기서 임포트 해야함! 
        print("================review=================")

        # sql = cls.query.filter_by(shop_id = shop_id)
        # sql = db.session.query(cls).join(cls.foods).filter_by(shop_id = shop_id)
        # sql = cls.query.join(OrderReviewDto.foods).filter_by(shop_id = shop_id)
        # join 하는 법
        sql = db.session.query(OrderReviewDto, FoodDto).\
            filter(OrderReviewDto.food_id == FoodDto.food_id).\
            filter_by(shop_id = shop_id).\
            order_by(OrderReviewDto.review_time.desc())
        df = pd.read_sql(sql.statement, sql.session.bind) 
        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        # print(df)
        return json.loads(df.to_json(orient='records'))

    #새로운 주문
    @staticmethod
    def save(order_review):
        db.session.add(order_review)
        db.session.commit()

    #주문 완료후 주문 정보 select 
    @classmethod
    def order_review_join_food_for_order(cls,userid):
        from chatbot_api.resources.user import UserDto
        from chatbot_api.resources.food import FoodDto
        print("-------------주문목록--------------")

        sql = db.session.query(OrderReviewDto, FoodDto, UserDto).\
            filter(UserDto.userid == OrderReviewDto.userid).\
            filter(OrderReviewDto.food_id ==  FoodDto.food_id).\
            filter_by(userid = userid).\
            order_by(OrderReviewDto.or_id.desc())

        df = pd.read_sql(sql.statement, sql.session.bind) 
        print(df)
        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        return json.loads(df.loc[[0]].to_json(orient='records'))


    # 마이페이지 유저 주문 목록 select    
    @classmethod
    def order_review_join_food(cls,userid):
        from chatbot_api.resources.food import FoodDto
        from chatbot_api.resources.shop import ShopDto
        sql = db.session.query(OrderReviewDto, FoodDto, ShopDto).\
            filter(OrderReviewDto.food_id == FoodDto.food_id,).\
            filter(OrderReviewDto.shop_id == ShopDto.shop_id,).\
            filter_by(userid = userid,).\
            order_by(OrderReviewDto.or_id.desc())

        df = pd.read_sql(sql.statement, sql.session.bind) 
        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        # print(df)
        return json.loads(df.to_json(orient='records'))

    # 마이페이지 > 리뷰쓰기 페이지 매장&메뉴 select
    @classmethod
    def order_review_join_shop_for_review(cls,or_id):
        from chatbot_api.resources.food import FoodDto
        from chatbot_api.resources.shop import ShopDto
        sql = db.session.query(OrderReviewDto, FoodDto, ShopDto).\
            filter(OrderReviewDto.food_id == FoodDto.food_id).\
            filter(OrderReviewDto.shop_id == ShopDto.shop_id).\
            filter_by(or_id = or_id).\
            order_by(OrderReviewDto.order_time.desc())

        df = pd.read_sql(sql.statement, sql.session.bind) 
        df = df.loc[:,~df.columns.duplicated()] # 중복 컬럼 제거
        # print(df)
        return json.loads(df.to_json(orient='records'))
    
    # 리뷰 작성 save
    @classmethod
    def order_review_writer(cls, params):
        or_id = params.pop("or_id")
        db.session.query(OrderReviewDto).\
            filter(cls.or_id == or_id).\
            update(params,synchronize_session=False);
        db.session.commit()




# ==============================================================
# ==============================================================
# =====================   Service   ============================
# ==============================================================
# ==============================================================

# from keras.models import Sequential
# from keras.layers import Dense, Activation
# from keras.models import load_model

# class UserService:
#     @staticmethod
#     def load_model_from_file():
#         fname = r'./modeling/recommender_mf.h5'
#         model = load_model(fname)
#         return model

#     @staticmethod
#     def shop_rev_predict(model, userid, shop_id):

#         userid = int(userid.lstrip('user'))
#         predict = model.predict([np.array([userid]), np.array([shop_id])])
#         print(predict[0])
#         return predict[0]



# ==============================================================
# ==============================================================
# =====================   Controller   =========================
# ==============================================================
# ==============================================================


class OrderReview(Resource):
    @staticmethod
    def post():
        params = request.get_json()
        order_review = OrderReviewDto(**params)
        print("주문정보",order_review)
        OrderReviewDao.save(order_review)
        return 200

class OrderReviewPage(Resource):

    @staticmethod
    def get(userid : str):
        print("주문정보")
        order = OrderReviewDao.order_review_join_food_for_order(userid)
        # print(order)
        # print(type(order))
        return order[0], 200

class OrderReviewUser(Resource):
    @staticmethod
    def get(userid : str):
        orderlist = OrderReviewDao.order_review_join_food(userid)
        return orderlist, 200

class OrderReviewSelect(Resource):
    @staticmethod
    def get(or_id : str):
        orderselect = OrderReviewDao.order_review_join_shop_for_review(or_id)
        # print(orderselect)
        return orderselect,200

class OrderReviewInsert(Resource):

    @staticmethod
    def post():  # update로 변경할 것
        params = request.get_json()
        # or_id = params.pop("or_id")
        # print(or_id)
        # print("리뷰쓰자아ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ" , params)
        # order_revew = OrderReviewDto(**params)
        # print(order_revew)
        OrderReviewDao.order_review_writer(params)
        print("리뷰썻다")

        return 200


# if __name__ == "__main__":
    # s = UserService()
    # model = s.load_model_from_file()