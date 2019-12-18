import http

from flask_marshmallow import Marshmallow
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs

from functionalities.employees import Employee
from utilities.validations import handle_exceptions


ma = Marshmallow()


class CategorySchema(ma.Schema):
    id = fields.Integer()


categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()


class GiftAssignmentResource(Resource):
    method_decorators = [handle_exceptions()]

    @use_kwargs(category_schema)
    def post(self, employee_id):
        employee = Employee(employee_id)
        gift = employee.assign_gift()
        return {"status": 'success', 'data': {'gift': gift.name}}, http.HTTPStatus.OK
