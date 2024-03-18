from flask import Blueprint
from flask_restful import Api

from api.resources.action import ActionList, ActionResource, ActionLogResource

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, errors=blueprint.errorhandler)

api.add_resource(ActionList, "/actions")
api.add_resource(ActionResource, "/actions/<int:action_id>")
api.add_resource(ActionLogResource, "/actions/<int:action_id>/log")
