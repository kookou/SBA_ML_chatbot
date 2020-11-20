import logging
from flask import Blueprint
from flask_restful import Api
from chatbot_api.resources.user import User, Access
from chatbot_api.resources.home import Home
from chatbot_api.resources.shop import Shop, Shops, Shopscat, ShopSearch
from chatbot_api.resources.food import Food
from chatbot_api.resources.chatbot import Chatbot
from chatbot_api.resources.order_review import OrderReview, OrderReviewPage, OrderReviewUser, OrderReviewSelect,OrderReviewInsert



home = Blueprint('home', __name__, url_prefix='/')
user = Blueprint('user', __name__, url_prefix='/user')
# users = Blueprint('users', __name__, url_prefix='/api/users')
shop = Blueprint('shop', __name__, url_prefix='/shop')
shops = Blueprint('shops', __name__, url_prefix='/shops')
order = Blueprint('order', __name__, url_prefix='/order')
review = Blueprint('reviewwrite', __name__, url_prefix='/reviewwrite')
search = Blueprint('search', __name__, url_prefix='/search')
# auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/access')
# article = Blueprint('article', __name__, url_prefix='/api/article')
# articles = Blueprint('articles', __name__, url_prefix='/api/articles')

api = Api(home)
api = Api(user)
api = Api(shops)
api = Api(shop)
api = Api(order)
api = Api(review)
api = Api(search)
# api = Api(users)
# api = Api(auth)
api = Api(access)
# api = Api(article)
# api = Api(articles)


def initialize_routes(api):
    print('========== routes ==========')
    api.add_resource(Home,'/main')  # 초기화면 userid 노출을 피하기 위해 post형식 사용
    api.add_resource(User, '/user', '/user/<string:userid>')
    api.add_resource(Shop, '/shop/<string:shop_id>')
    api.add_resource(ShopSearch, '/search/<string:key>')
    api.add_resource(Shops, '/shops')
    api.add_resource(Shopscat,'/shops/<string:cat_id>')
    api.add_resource(OrderReview, '/order')
    api.add_resource(OrderReviewPage, '/order/<string:userid>')
    api.add_resource(OrderReviewUser, '/mypage/<string:userid>')
    api.add_resource(OrderReviewSelect, '/reviewwrite/<string:or_id>')
    api.add_resource(OrderReviewInsert, '/reviewwrite')
    api.add_resource(Chatbot, '/chatbot/<string:key>')
    # api.add_resource(Home, '/api')
    # api.add_resource(Item, '/api/item/<string:id>')
    # api.add_resource(Items,'/api/items')
    # api.add_resource(User, '/user/<string:id>')
    # api.add_resource(Users, '/api/users')
    # api.add_resource(Auth, '/api/auth')
    api.add_resource(Access, '/access', '/access/<string:userid>')



@user.errorhandler(500)
def user_api_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500

@home.errorhandler(500)
def home_api_error(e):
    logging.exception('An error occurred during home request. %s' % str(e))
    return 'An internal error occurred.', 500