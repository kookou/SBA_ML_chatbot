# from sqlalchemy import Column, Integer, Float, String, ForeignKey, create_engine
# from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, LONGTEXT
from pdb import main
from typing import List
from flask import request, session
from flask_cors import cross_origin

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

from chatbot_api.resources.order_review import OrderReviewDto


class UserDto(db.Model):
    __tablename__ = "user"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 한글 인코딩

    userid: str = db.Column(db.String(20), primary_key=True, index=True)
    password: str = db.Column(db.String(200))
    name: str = db.Column(db.String(30))
    age: int = db.Column(db.Integer)
    gender: int = db.Column(db.Integer)
    addr: str = db.Column(db.String(100))
    lat: float = db.Column(db.Float)
    lng: float = db.Column(db.Float)

    order_reviews = db.relationship('OrderReviewDto', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")

    def __init__(self, userid, password, name, age=0, gender=0, addr='', lat=0, lng=0):
        self.userid = userid
        self.password = password
        self.name = name
        self.age = age
        self.gender = gender
        self.addr = addr
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return f'User(userid={self.userid}, ' \
               f'password={self.password}, ' \
               f'name={self.name},' \
               f'age={self.age},' \
               f'gender={self.gender},' \
               f'addr={self.addr}, ' \
               f'lat={self.lat}, ' \
               f'lng={self.lng})'

    @property
    def json(self):
        return {
            'userid': self.userid,
            'password': self.password,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'addr': self.addr,
            'lat': self.lat,
            'lng': self.lng
        }

class UserVo:
    userid: str = ''
    password: str = ''
    name: str = ''
    age: int = 0
    gender: int = 0
    addr: str = ''
    lat: float = 0.0
    lng: float =  0.0



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

    # @cross_origin(supports_credentials=True)
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


# ==============================================================
# ==============================================================
# ====================     Service  ============================
# ==============================================================
# ==============================================================



"""
context: /Users/bitcamp/SbaProjects
fname: 
PassengerId
Survived: The answer that a machine learning model should match 
Pclass: Boarding Pass 1 = 1st-class seat, 2 = 2nd, 3 = 3rd,
Name,
Sex,
Age,
SibSp accompanying brothers, sisters, spouses
Parch accompanying parents, children,
Ticket : Ticket Number
Fare : Boarding Charges
Cabin : Room number
Embarked : a Port Name on Board C = Cherbourg, Q = Queenstown, S = Southhampton
"""


class UserService:
    def __init__(self):
        self.fileReader = FileReader()
        self.data = os.path.abspath("data")

        self.odf = None

    def hook(self):
        train = 'train.csv'
        test = 'test.csv'
        this = self.fileReader
        this.train = self.new_model(train)  # payload
        this.test = self.new_model(test)  # payload

        '''
        Original Model Generation
        '''
        self.odf = pd.DataFrame(

            {
                'userid': this.train.PassengerId,
                'password': '1',
                'name': this.train.Name
            }
        )

        this.id = this.test['PassengerId']  # This becomes a question.
        # print(f'Preprocessing Train Variable : {this.train.columns}')
        # print(f'Preprocessing Test Variable : {this.test.columns}')
        this = self.drop_feature(this, 'Cabin')
        this = self.drop_feature(this, 'Ticket')
        # print(f'Post-Drop Variable : {this.train.columns}')
        this = self.embarked_norminal(this)
        # print(f'Preprocessing Embarked Variable: {this.train.head()}')
        this = self.title_norminal(this)
        # print(f'Preprocessing Title Variable: {this.train.head()}')
        '''
        The name is unnecessary because we extracted the Title from the name variable.
        '''
        this = self.drop_feature(this, 'Name')
        this = self.drop_feature(this, 'PassengerId')
        this = self.age_ordinal(this)
        # print(f'Preprocessing Age Variable: {this.train.head()}')
        this = self.drop_feature(this, 'SibSp')
        this = self.sex_norminal(this)
        # print(f'Preprocessing Sex Variable: {this.train.head()}')
        this = self.fareBand_nominal(this)
        # print(f'Preprocessing Fare Variable: {this.train.head()}')
        this = self.drop_feature(this, 'Fare')
        # print(f'Preprocessing Train Result: {this.train.head()}')
        # print(f'Preprocessing Test Result: {this.test.head()}')
        # print(f'Train NA Check: {this.train.isnull().sum()}')
        # print(f'Test NA Check: {this.test.isnull().sum()}')
        this.label = self.create_label(this)  # payload
        this.train = self.create_train(this)  # payload
        # print(f'Train Variable : {this.train.columns}')
        # print(f'Test Variable : {this.train.columns}')
        clf = RandomForestClassifier()
        clf.fit(this.train, this.label)
        prediction = clf.predict(this.test)

        # print(this)
        df = pd.DataFrame(

            {
                'pclass': this.train.Pclass,
                'gender': this.train.Sex,
                'age_group': this.train.AgeGroup,
                'embarked': this.train.Embarked,
                'rank': this.train.Title
            }
        )

        # print(self.odf)
        # print(df)
        sumdf = pd.concat([self.odf, df], axis=1)

        '''
userid password                                               name  pclass  gender age_group  embarked  rank
0         1        1                            Braund, Mr. Owen Harris       3       0         4         1     1
1         2        1  Cumings, Mrs. John Bradley (Florence Briggs Th...       1       1         6         2     3
2         3        1                             Heikkinen, Miss. Laina       3       1         5         1     2
3         4        1       Futrelle, Mrs. Jacques Heath (Lily May Peel)       1       1         5         1     3
4         5        1                           Allen, Mr. William Henry       3       0         5         1     1
..      ...      ...                                                ...     ...     ...       ...       ...   ...
886     887        1                              Montvila, Rev. Juozas       2       0         5         1     6
887     888        1                       Graham, Miss. Margaret Edith       1       1         4         1     2
888     889        1           Johnston, Miss. Catherine Helen "Carrie"       3       1         2         1     2
889     890        1                              Behr, Mr. Karl Howell       1       0         5         2     1
890     891        1                                Dooley, Mr. Patrick       3       0         5         3     1
[891 rows x 8 columns]

        '''
        return sumdf

    def new_model(self, payload) -> object:
        this = self.fileReader
        this.data = self.data
        this.fname = payload
        print(f'{self.data}')
        print(f'{this.fname}')
        return pd.read_csv(Path(self.data, this.fname))

    @staticmethod
    def create_train(this) -> object:
        return this.train.drop('Survived', axis=1)  # Train is a dataset in which the answer is removed.

    @staticmethod
    def create_label(this) -> object:
        return this.train['Survived']  # Label is the answer.

    @staticmethod
    def drop_feature(this, feature) -> object:
        this.train = this.train.drop([feature], axis=1)
        this.test = this.test.drop([feature], axis=1)
        return this

    @staticmethod
    def pclass_ordinal(this) -> object:
        return this

    @staticmethod
    def sex_norminal(this) -> object:
        combine = [this.train, this.test]  # Train and test are bound.
        sex_mapping = {'male': 0, 'female': 1}
        for dataset in combine:
            dataset['Sex'] = dataset['Sex'].map(sex_mapping)
        this.train = this.train  # overriding
        this.test = this.test
        return this

    @staticmethod
    def age_ordinal(this) -> object:
        train = this.train
        test = this.test
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5)
        '''
        It's ambiguous to put an average, and it's too baseless to put a majority.
        the age is significant in determining survival rates and requires a detailed approach.
        If you don't know your age, 
        you have to deal with it without knowing it to reduce the distortion of the price
        -0.5 is the middle value.
        '''
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        '''
        This part represents a range.
        -1 and more than 0....60 and more...
        [] This must be a variable name here.If you think so, you've got it right.
        '''

        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
        # [] This must be a variable name here.
        train['AgeGroup'] = pd.cut(train['Age'], bins, labels=labels)
        test['AgeGroup'] = pd.cut(train['Age'], bins, labels=labels)
        age_title_mapping = {
            0: 'Unknown',
            1: 'Baby',
            2: 'Child',
            3: 'Teenager',
            4: 'Student',
            5: 'Young Adult',
            6: 'Adult',
            7: 'Senior'
        }  # If you treat it from [] to {} like this, you will treat Labs as a value.
        for x in range(len(train['AgeGroup'])):
            if train['AgeGroup'][x] == 'Unknown':
                train['AgeGroup'][x] = age_title_mapping[train['Title'][x]]
        for x in range(len(test['AgeGroup'])):
            if test['AgeGroup'][x] == 'Unknown':
                test['AgeGroup'][x] = age_title_mapping[test['Title'][x]]

        age_mapping = {
            'Unknown': 0,
            'Baby': 1,
            'Child': 2,
            'Teenager': 3,
            'Student': 4,
            'Young Adult': 5,
            'Adult': 6,
            'Senior': 7
        }
        train['AgeGroup'] = train['AgeGroup'].map(age_mapping)
        test['AgeGroup'] = test['AgeGroup'].map(age_mapping)
        this.train = train
        this.test = test
        return this

    @staticmethod
    def sibsp_numeric(this) -> object:
        return this

    @staticmethod
    def parch_numeric(this) -> object:
        return this

    @staticmethod
    def fare_ordinal(this) -> object:
        this.train['FareBand'] = pd.qcut(this['Fare'], 4, labels={1, 2, 3, 4})
        this.test['FareBand'] = pd.qcut(this['Fare'], 4, labels={1, 2, 3, 4})
        return this

    @staticmethod
    def fareBand_nominal(this) -> object:  # Rates vary, so prepare for clustering
        this.train = this.train.fillna({'FareBand': 1})  # FareBand is a non-existent variable added
        this.test = this.test.fillna({'FareBand': 1})
        return this

    @staticmethod
    def embarked_norminal(this) -> object:
        this.train = this.train.fillna({'Embarked': 'S'})  # S is the most common, filling in empty spaces.
        this.test = this.test.fillna({'Embarked': 'S'})
        '''
        Many machine learning libraries expect class labels to be encoded as * integer*
        mapping: blue = 0, green = 1, red = 2
        '''
        this.train['Embarked'] = this.train['Embarked'].map({'S': 1, 'C': 2, 'Q': 3})
        this.test['Embarked'] = this.test['Embarked'].map({'S': 1, 'C': 2, 'Q': 3})
        return this

    @staticmethod
    def title_norminal(this) -> object:
        combine = [this.train, this.test]
        for dataset in combine:
            dataset['Title'] = dataset.Name.str.extract('([A-Za-z]+)\.', expand=False)
        for dataset in combine:
            dataset['Title'] = dataset['Title'].replace(['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', \
                                                         'Jonkheer', 'Dona', 'Mme'], 'Rare')
            dataset['Title'] = dataset['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
            dataset['Title'] = dataset['Title'].replace('Mlle', 'Mr')
        title_mapping = {'Mr': 1, 'Miss': 2, 'Mrs': 3, 'Master': 4, 'Royal': 5, 'Rare': 6}
        for dataset in combine:
            dataset['Title'] = dataset['Title'].map(title_mapping)
            dataset['Title'] = dataset['Title'].fillna(0)  # Unknown
        this.train = this.train
        this.test = this.test
        return this

    # Dtree, rforest, nb, nnn, svm among Learning Algorithms use this as a representative

    @staticmethod
    def create_k_fold():
        return KFold(n_splits=10, shuffle=True, random_state=0)

    def accuracy_by_dtree(self, this):
        dtree = DecisionTreeClassifier()
        score = cross_val_score(dtree, this.train, this.label, cv=UserService.create_k_fold(), \
                                n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_by_rforest(self, this):
        rforest = RandomForestClassifier()
        score = cross_val_score(rforest, this.train, this.label, cv=UserService.create_k_fold(), \
                                n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_by_nb(self, this):
        nb = GaussianNB()
        score = cross_val_score(nb, this.train, this.label, cv=UserService.create_k_fold(), \
                                n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_by_knn(self, this):
        knn = KNeighborsClassifier()
        score = cross_val_score(knn, this.train, this.label, cv=UserService.create_k_fold(), \
                                n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_by_svm(self, this):
        svm = SVC()
        score = cross_val_score(svm, this.train, this.label, cv=UserService.create_k_fold(), \
                                n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def learning(self, train, test):
        service = self.service
        this = self.modeling(train, test)
        print(f'Dtree verification result: {service.accuracy_by_dtree(this)}')
        print(f'RForest verification result: {service.accuracy_by_rforest(this)}')
        print(f'Naive Bayes tree verification result: {service.accuracy_by_nb(this)}')
        print(f'KNN verification result: {service.accuracy_by_knn(this)}')
        print(f'SVM verification result: {service.accuracy_by_svm(this)}')

    def submit(self, train, test):
        this = self.modeling(train, test)
        clf = RandomForestClassifier()
        clf.fit(this.train, this.label)
        prediction = clf.predict(this.test)

        print(this)
        # Pclass  Sex   Age  Parch  Embarked  Title AgeGroup
        df = pd.DataFrame(

            {
                'pclass': this.train.Pclass,
                'gender': this.train.Sex,
                'age_group': this.train.AgeGroup,
                'embarked': this.train.Embarked,
                'rank': this.train.Title
            }
        )

        # print(self.odf)
        # print(df)
        sumdf = pd.concat([self.odf, df], axis=1)
        print(sumdf)
        return sumdf


'''
service = UserService()
service.hook()
'''

# ==============================================================
# ==============================================================
# =================     Controller  ============================
# ==============================================================
# ==============================================================

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed   # deprecated 예정이라고 함
parser.add_argument('userid', type=str, required=True,
                                        help='This field should be a userid')
parser.add_argument('password', type=str, required=True,
                                        help='This field should be a password')
parser.add_argument('name', type=str, required=False,
                                        help='This field should be a password')

class User(Resource):
    @staticmethod
    def post():
        print('================user post 요청받음 =================')
        
        # --------------
        # parameter 받는 방법
        # parser.parse_args(): <class 'flask_restful.reqparse.Namespace'>
        args = parser.parse_args()
        print('type(args): ', type(args))
        print('args: ', args)
        # print(f'User {args["userid"]} added ')

        # request.get_json(): <class 'dict'>
        params = request.get_json()
        # params = json.loads(request.get_data(), encoding='utf-8')
        print('type(params): ', type(params))
        print('params: ', params)
        if len(params) == 0:
            return 'No parameter'

        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value: {}<br>'.format(key, params[key])
        # ---------------

        # create 구현
        user = UserDto(**params)
        UserDao.save(user)
        userid = user.userid
        
        return {'code':0, 'message': 'SUCCESS', 'userid': userid }, 200
    
    @staticmethod
    def get(id):
        print(f'User {id} added ')
        try:
            user = UserDao.find_by_id(id)
            if user:
                return user.json()
        except Exception as e:
            return {'message': 'User not found'}, 404

    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'User {args["id"]} updated ')
        return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'USer {args["id"]} deleted')
        return {'code' : 0, 'message' : 'SUCCESS'}, 200

    
    
class Users(Resource):
    
    def post(self):
        ud = UserDao()
        ud.insert_many('users')

    def get(self):
        print('========== 10 ==========')
        data = UserDao.find_all()
        return data, 200

class Auth(Resource):

    def post(self):
        body = request.get_json()
        user = UserDto(**body)
        UserDao.save(user)
        id = user.userid
        
        return {'id': str(id)}, 200 


class Access(Resource):

    @staticmethod
    def post():
        print('========== access post 요청 받음 ==========')
        args = parser.parse_args()
        user = UserVo()
        user.userid = args.userid
        user.password = args.password
        data = UserDao.login(user)
        if data[0]:
            # session[f'{args.userid}'] = data[0]
            session['user'] = data[0]
        print(session)
        return data[0], 200

    @staticmethod
    def delete(userid):
        print('========== access delete 요청 받음 ==========')
        print(session)
        session.pop('user', None)
        # session.pop('user', None)
        # session.clear()   
        return {'code' : 0, 'message' : 'SUCCESS'}, 200



# ------------ 실행 영역 --------------

if __name__ == '__main__':
     
    # 데이터 일괄 입력
    # df = pd.read_csv('./data/db/user.csv', sep=',', encoding='utf-8-sig') # 혜정
    df = pd.read_csv('./data/csv/important/db/user.csv', sep=',', encoding='utf-8-sig') # 영돈
    df = df.replace(np.nan, 0, regex=True)


    Session = openSession()
    session = Session()
    session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
    session.commit()
    session.close()

