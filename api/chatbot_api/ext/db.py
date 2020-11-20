from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

'''
어플리케이션이 SQLAlchemy ORM을 사용한다면, 
객체에 바인딩된 쿼리를 위해서 Session 객체를 사용해야 한다. 
이는 session.add(), session.rollback(), session.commit(), session.close()를 통해 
트랜잭션을 단일 작업 단위로 관리하기 좋고, 
이러한 특징을 통해 Python의 Context Manager 패턴을 사용하기에도 좋다.
'''

db = SQLAlchemy()

# aws rds 일때
# config = {
#     'user': 'mychatbot',
#     'password': 'mychatbot',
#     'host': 'mychatbot.chkq44slodcf.ap-northeast-2.rds.amazonaws.com',
#     'port': '3306',
#     'database': 'mychatbot'
# }

# local mariadb 일 때
# config = {
#     'user': 'root',
#     'password': 1004,
#     'host': '127.0.0.1',
#     'port': '3306',
#     'database': 'mariadb'
# }

charset = {'utf8': 'utf8'}
url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/" \
      f"{config['database']}?charset=utf8"

Base = declarative_base()  # SqlAlchemy에서 사용
engine = create_engine(url)

def openSession():
    return sessionmaker(bind=engine)

# 예시
# engine = create_engine('mysql+mysqlconnector://root:1004@127.0.0.1/mariadb?charset=utf8', encoding='utf8', echo=True)
# Base.metadata.create_all(engine)  # metadata: 스키마 구조 DDL create문 실행해 줌. 최초만 실행
# Base.metadata.drop_all(bind=engine, tables=[User.__table__])  # drop table


# Session = sessionmaker(bind=engine)
# session = Session()
# session.add(User(userid='tom', password='1', name='thomas'))
# query = session.query
# session.commit()