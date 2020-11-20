from chatbot_api.home.api import Home
from chatbot_api.user.api import User


def initialize_routes(api):
    print('========== routes ==========')
    api.add_resource(Home, '/api')
    # api.add_resource(Item, '/api/item/<string:id>')
    # api.add_resource(Items,'/api/items')
    api.add_resource(User, '/api/user/<string:id>')
    # api.add_resource(Users, '/api/users')
    # api.add_resource(Article, '/api/article/<string:id>')
    # api.add_resource(Articles, '/api/articles/')
