from flask import Blueprint
from flask_restful import Api
from resources import hello, category

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(hello.Hello, '/hello')
api.add_resource(category.CategoryResource, '/categories/<int:category_id>')
api.add_resource(category.CategoryListResource, '/categories')
