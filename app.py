from flask import Blueprint
from flask_restful import Api
from resources import gift_assignment

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(gift_assignment.GiftAssignmentResource, '/employee/<int:employee_id>/assign_gift')
