from math import e
from flask_restful import Resource, reqparse
from flask import session

import random

from chatbot_api.ext.db import config
from chatbot_api.ext.model import user_based_recommend, item_based_recommend
from chatbot_api.resources.shop import ShopDto, ShopDao, ShopService

    
# ==============================================================
# ==============================================================
# =====================   Service   ============================
# ==============================================================
# ==============================================================

class HomeService:
    @staticmethod
    def user_based_recommendation_by_surprise(userid):
        
        recommend_shop_id_set , df_shop = user_based_recommend(userid)

        shop_dict_list = []
        for shop_id in recommend_shop_id_set:
            shop = ShopDao.find_by_shopid(str(shop_id))
            try:
                shop_dict_list.append(shop[0])
            except :
                # print('out of index')
                pass
                
        # print(shop_dict_list)
        recommend = ShopService.shop_rev_predict_by_surprise(shop_dict_list)
        print(recommend)
        user_based_list = random.sample(recommend, 4)  # 랜덤하게 4개 추출

        return user_based_list, df_shop

    @staticmethod
    def item_based_recommendation_by_surprise(userid, df_shop):
        df_shop_by_userid = df_shop[(df_shop['userid'] == userid)].sort_values(by=['rating'], ascending=False)  # user가 이용한 매장을 평점 내림차순 정렬
        recommend_shop_list = df_shop_by_userid['shop_id'].head(5).values  # 가장 상위 매장 아이디만 5개 추출
        random_recommend_shop_id = random.choice(recommend_shop_list)  # 그 중 하나를 랜덤 추출

        recommend_shop_id_list, df_shop = item_based_recommend(random_recommend_shop_id)
        
        # 위 메서드와 중복되므로 나중에 리팩토링 필요
        shop_dict_list = []
        for shop_id in recommend_shop_id_list:
            shop = ShopDao.find_by_shopid(str(shop_id))
            try:
                shop_dict_list.append(shop[0])
            except :
                # print('out of index')
                pass
        
        recommend = ShopService.shop_rev_predict_by_surprise(shop_dict_list)
        item_based_list = random.sample(recommend, 4)  # 랜덤하게 4개 추출

        # 추천 기준이 되는 shop의 shop_name 추출
        random_recommend_shop = ShopDao.find_by_shopid(str(random_recommend_shop_id))
        random_recommend_shop_name = random_recommend_shop[0]['shop_name']

        return item_based_list, random_recommend_shop_name, df_shop
        



# ==============================================================
# ==============================================================
# =====================   Controller   =========================
# ==============================================================
# ==============================================================


class Home(Resource):

    @staticmethod
    def get():
        userid = session['user']['userid']
        # userid = int(userid.lstrip('user'))
        print('userid: ', userid)
        
        # user_based_recommendation
        user_based_list, df_shop = HomeService.user_based_recommendation_by_surprise(userid)

        # item_based_recommendation
        item_based_list, recommend_shop_name, df_shop = HomeService.item_based_recommendation_by_surprise(userid, df_shop)

        recommedation_list = [user_based_list, item_based_list, recommend_shop_name]
       
        return recommedation_list, 200        
 
 
        # return {'message': 'Server Start'}


    