from flask import Blueprint
from flask_restful import Api

from microbiome_api.api.resources import (
    UserResource,
    UserList,
    PathoStat,
    Comets
)


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(PathoStat, '/pathostat')
api.add_resource(PathoStatStatus, '/pathostat/<str:task_id>')
