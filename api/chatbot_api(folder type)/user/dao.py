from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chatbot_api.ext.db import db, openSession
from chatbot_api.user.service import UserService
from chatbot_api.user.dto import UserDto
import pandas as pd
import json
'''
어플리케이션이 SQLAlchemy ORM을 사용한다면, 
객체에 바인딩된 쿼리를 위해서 Session 객체를 사용해야 한다. 
이는 session.add(), session.rollback(), session.commit(), session.close()를 통해 
트랜잭션을 단일 작업 단위로 관리하기 좋고, 
이러한 특징을 통해 Python의 Context Manager 패턴을 사용하기에도 좋다.
'''


class UserDao(UserDto):
    

    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name).all()

    @classmethod
    def find_by_id(cls, userid):
        return cls.query.filter_by(userid == userid).first()

    @classmethod
    def login(cls, user):
        sql = cls.query\
            .filter(cls.userid.like(user.userid))\
            .filter(cls.password.like(user.password))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print('==================================')
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))


    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def insert_many():
        service = UserService()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def modify_user(user):
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete_user(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()




# user_dao.add_user(User(userid='tom', password='1', name='tom', addr="서울시 서초구", lat=37.1234, lng=128.1234))
# user_dao.delete_table()
# print(user_dao.fetch_user('tom'))

# for row in user_dao.fetch_all_users():
#     print(row)

'''    
u = UserDao()
u.insert_many()
'''

# 데이터 일괄 입력
# import numpy as np
# df = pd.read_csv('./data/csv/important/user_df.csv', sep=',', encoding='utf-8-sig')
# df = df.replace(np.nan, '', regex=True)
# Session = openSession()
# session = Session()
# session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
# session.commit()
# session.close()