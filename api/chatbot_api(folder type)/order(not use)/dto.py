# from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, create_engine
from chatbot_api.ext.db import Base, db
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT


class OrderDto(db.Model):
    __tablename__ = "order"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 한글 인코딩

    order_id: int = db.Column(db.Integer, primary_key=True, index=True)
    order_time: str = db.Column(db.Date)
    order_cmnt: str = db.Column(db.String(200))

    userid: str = db.Column(db.String(20), db.ForeignKey('user.userid'))
    shop_id: int = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    food_id: int = db.Column(db.Integer, db.ForeignKey('food.food_id'))

    reviews = db.relationship('ReviewDto', backref='order', lazy=True)

    def __init__(self, order_id, order_time, order_cmnt, userid, shop_id, food_id):
        self.order_id = order_id
        self.order_time = order_time
        self.order_cmnt = order_cmnt
        self.userid = userid
        self.shop_id = shop_id
        self.food_id = food_id

    def __repr__(self):
        return f'Order(order_id={self.order_id}, ' \
               f'order_time={self.order_time}, ' \
               f'order_cmnt={self.order_cmnt}, ' \
               f'userid={self.userid}, ' \
               f'shop_id={self.shop_id}' \
               f'food_id={self.food_id}'

    @property
    def json(self):
        return {
            'order_id': self.order_id,
            'order_time': self.order_time,
            'order_cmnt': self.order_cmnt,
            'userid': self.userid,
            'shop_id': self.shop_id,
            'food_id': self.food_id
        }
