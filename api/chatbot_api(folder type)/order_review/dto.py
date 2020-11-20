# from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, create_engine
from chatbot_api.ext.db import Base, db
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT

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

    userid: str = db.Column(db.String(20), db.ForeignKey('user.userid'))
    shop_id: int = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    food_id: int = db.Column(db.Integer, db.ForeignKey('food.food_id')) 

    def __init__(self, or_id, order_time, review_cmnt, taste_rate, quantity_rate,
                 delivery_rate, review_time, review_img, owner_cmnt, userid, shop_id, food_id):
        self.or_id = or_id
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
        return f'Review(or_id={self.or_id}, ' \
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
               f'food_id={self.food_id} ' \


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
