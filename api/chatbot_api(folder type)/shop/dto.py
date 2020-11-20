# from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, create_engine
from chatbot_api.ext.db import Base, db
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
from chatbot_api.food.dto import FoodDto
from chatbot_api.order_review.dto import OrderReviewDto

class ShopDto(db.Model):
    __tablename__ = "shop"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 한글 인코딩

    shop_id: int = db.Column(db.Integer, primary_key=True, index=True)
    shop_name: str = db.Column(db.String(30))
    shop_addr: str = db.Column(db.String(100))
    shop_img: str = db.Column(db.String(200), default='shop_default.png')
    cat: str = db.Column(db.String(20))
    shop_lat: float = db.Column(db.Float)
    shop_lng: float = db.Column(db.Float)
    shop_rev_avg: float = db.Column(db.Float)
    shop_rev_cnt: int = db.Column(db.Integer)
    opentime: str = db.Column(db.Date)

    foods = db.relationship('FoodDto', backref='shop', lazy=True)
    order_reviews = db.relationship('OrderReviewDto', backref='shop', lazy=True)
    

    def __init__(self, shop_id, shop_name, shop_addr, shop_img, cat,
                 shop_lat, shop_lng, shop_rev_avg, shop_rev_cnt, opentime):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.shop_addr = shop_addr
        self.shop_img = shop_img
        self.cat = cat
        self.shop_lat = shop_lat
        self.shop_lng = shop_lng
        self.shop_rev_avg = shop_rev_avg
        self.shop_rev_cnt = shop_rev_cnt
        self.opentime =opentime

    def __repr__(self):
        return f'Shop(shop_id={self.shop_id}, shop_name={self.shop_name}, ' \
               f'shop_addr={self.shop_addr}, ,shop_img={self.shop_img}, cat={self.cat},' \
               f'shop_lat={self.shop_lat}, shop_lng="{self.shop_lng}"' \
               f'shopt_rev_avg={self.shop_rev_avg}, shop_rev_cnt={self.shop_rev_cnt}' \
               f'opentime={self.opentime}'

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
            'opentime': self.opentime
        }


class UserVo:
    shop_id: int = 0
    shop_name: str = ''
    shop_addr: str = ''
    shop_img: str = ''
    cat: str = ''
    shop_lat: float = 0.0
    shop_lng: float = 0.0
    shop_rev_avg: float = 0.0 
    shop_rev_cnt: int = 0
    opentime: str = ''