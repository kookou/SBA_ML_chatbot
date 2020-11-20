from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chatbot_api.ext.db import db, openSession
from com_sba_api.user.service import UserService
from chatbot_api.user.dto import UserDto
'''
어플리케이션이 SQLAlchemy ORM을 사용한다면, 
객체에 바인딩된 쿼리를 위해서 Session 객체를 사용해야 한다. 
이는 session.add(), session.rollback(), session.commit(), session.close()를 통해 
트랜잭션을 단일 작업 단위로 관리하기 좋고, 
이러한 특징을 통해 Python의 Context Manager 패턴을 사용하기에도 좋다.
'''


class UserDao:
    # def __init__(self):
    #     self.engine = create_engine('mysql+mysqlconnector://root:1004@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
    #     Session = sessionmaker(bind=self.engine)
    #     self.session = Session()

    # def create_table(self):
    #     if not self.engine.dialect.has_table(self.engine, "user"):
    #         self.Base.metadata.create_all(self.engine)  # metadata: 스키마 구조 DDL create문 실행해 줌. 최초만 실행
    #         print('테이블 생성')
    #     else:
    #         print('이미 테이블이 존재')

    # def delete_table(self):
    #     Base.metadata.drop_all(bind=self.engine, tables=[UserDto.__table__])  # drop table

    # ---------------------------------------------------
    # SqlAlchemy 방식
    # def add_user(self, user):
    #     # User(userid='tom', password='1', name='thomas')
    #     self.session.add(user)
    #     self.session.commit()
    #
    # def fetch_user(self, userid):
    #     query = self.session.query(User).filter((User.userid == userid))
    #     return query[0]
    #
    # def fetch_all_users(self):
    #     return self.session.query(User).all()
    #
    # def update_user(self):
    #     ...
    #
    # def delete_user(self):
    #     ...
    # --------------------------------------------------

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name).all()

    @classmethod
    def find_by_id(cls, userid):
        return cls.query.filter_by(userid == userid).first()

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
