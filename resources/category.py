import http

from flask_marshmallow import Marshmallow
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs

from models import db, Category
from utilities.exceptions import ResourceExists, ResourceDoesNotExist
from utilities.validations import handle_exceptions


ma = Marshmallow()


class CategorySchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()


class CategoryListResource(Resource):
    method_decorators = [handle_exceptions()]

    def get(self):
        categories = Category.query.all()
        categories = categories_schema.dump(categories)
        return {'data': categories}, http.HTTPStatus.OK

    @use_kwargs(category_schema)
    def post(self, *_, **category_data):
        category = Category.query.filter_by(name=category_data['name']).first()
        if category:
            raise ResourceExists('Category already exists')

        category = Category(
            name=category_data['name']
        )

        db.session.add(category)
        db.session.commit()

        result = category_schema.dump(category)

        return {"status": 'success', 'data': result}, http.HTTPStatus.CREATED


class CategoryResource(Resource):
    method_decorators = [handle_exceptions()]

    def get(self, category_id):
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            raise ResourceDoesNotExist('Category id does not exist')
        category = category_schema.dump(category)
        return {'data': category}, http.HTTPStatus.OK

    @use_kwargs(category_schema)
    def put(self, category_id, **category_data):
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            raise ResourceDoesNotExist('Category id does not exist')
        category.name = category_data['name']
        db.session.commit()

        result = category_schema.dump(category)

        return {"status": 'success', 'data': result}, http.HTTPStatus.OK

    def delete(self, category_id, **_):
        Category.query.filter_by(id=category_id).delete()
        db.session.commit()

        return {"status": 'success'}, http.HTTPStatus.NO_CONTENT
