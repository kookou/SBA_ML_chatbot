# from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, create_engine
from chatbot_api.ext.db import Base, db
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
from chatbot_api.order_review.dto import OrderReviewDto

class FoodDto(db.Model):
    __tablename__ = "food"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 한글 인코딩

    food_id: int = db.Column(db.Integer, primary_key=True, index=True)
    food_name: str = db.Column(db.String(30))
    price: int = db.Column(db.Integer)
    food_img: str = db.Column(db.String(1000))  # 최대 길이가 634정도였음
    food_rev_avg: float = db.Column(db.Float)
    food_rev_cnt: float = db.Column(db.Integer)

    shop_id: int = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))

    order_reviews = db.relationship('OrderReviewDto', backref='food', lazy=True)

    def __init__(self, food_id, food_name, price, food_img, food_rev_avg,
                 food_rev_cnt, shop_id):
        self.food_id = food_id
        self.food_name = food_name
        self.price = price
        self.food_img = food_img
        self.food_rev_avg = food_rev_avg
        self.food_rev_cnt = food_rev_cnt
        self.shop_id = shop_id

    def __repr__(self):
        return f'Food(food_id={self.food_id}, ' \
               f'food_name={self.food_name}, ' \
               f'price={self.price}, ' \
               f'food_img={self.food_img}, ' \
               f'food_rev_avg={self.food_rev_avg}, ' \
               f'food_rev_cnt={self.food_rev_cnt}, ' \
               f'shop_id="{self.shop_id}"'

    @property
    def json(self):
        return {
            'food_id': self.food_id,
            'food_name': self.food_name,
            'price': self.price,
            'food_img': self.food_img,
            'food_rev_avg': self.food_rev_avg,
            'food_rev_cnt': self.food_rev_cnt,
            'shop_id': self.shop_id
        }

class FoodVo:
    food_id: int = 0
    food_name: str = ''
    price: int = 0
    food_img: str = ''
    food_rev_avg: float = 0.0
    food_rev_cnt: float = 0.0

    shop_id: int = 0