import datetime

from flask import request, session
from flask_restful import Resource, reqparse

from chatbot_api.resources.food import FoodDao
from chatbot_api.resources.shop import ShopDao, ShopService
from chatbot_api.resources.order_review import OrderReviewDao, OrderReviewDto
from chatbot_api.resources.home import HomeService
from chatbot_api.ext.searchChatbot import process_nb
from chatbot_api.ext.kobert_chatbot import process_kobert

class ChatbotService:
    
    @staticmethod
    def load_model_from_file():
        print("어디까지 오니 ================")
        fname = r'./modeling/chatbot_model.h5'
        model = joblib.load(fname)
        print("모델 리턴전 ")
        return model

    @staticmethod
    def response_message(text):
        print("chatbot 2 text : ", text)
        kobert = process_kobert(text)
        _, keyword = process_nb(text)
        intent = kobert[0]
        cat = kobert[1].replace('/','')  # 피자/양식 -> 피자양식
        print('intent', intent)
        print('cat', cat)
        userid = session['user']['userid']
        chatsearch = ''
        if intent == '인사':
            pass
        # chatsearch = FoodDao.chat_food_find(cat)
        elif intent == '추천':
            if cat == '오늘' or cat == '베스트':
                user_based_list, df_shop = HomeService.user_based_recommendation_by_surprise(userid)
    
                return user_based_list, intent, cat, 200
            else:
                chatsearch = ShopDao.find_by_cat(cat)
                for item in ShopDao.search(keyword):
                    chatsearch.append(item)

                chatsearch = ShopService.shop_rev_predict_by_surprise(chatsearch)
                top_1 = {}
                tmp = 0
                for dict in chatsearch:
                    if (dict['shop_pred_avg'] > tmp) and (keyword in dict['food_name'] or keyword in dict['shop_name']):
                        top_1 = dict
                        tmp = dict['shop_pred_avg']
                chatsearch = [top_1]
                session['order_info'] = top_1
        elif intent == '주문':
            order_review = OrderReviewDto(userid=userid,
            order_time=datetime.datetime.now(), shop_id=session['order_info']['shop_id'],
            food_id=session['order_info']['food_id'])
            OrderReviewDao.save(order_review)
            return OrderReviewDao.order_review_join_food_for_order(userid), intent, cat, 200
            
        return chatsearch, intent, cat, 200


class Chatbot(Resource):
    
    @staticmethod
    def get(key : str):
        print("chatbot 1 key : ", key)
        words = ChatbotService.response_message(key)
        return words, 200