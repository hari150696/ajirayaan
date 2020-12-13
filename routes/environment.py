from flask import Blueprint, request
from utils.response import send_response

Environment = Blueprint('environment', __name__, url_prefix="/api/environment")
env_attr = {}


@Environment.route('/configure', methods=['POST'])
def add_environment():
    if not request.headers['Content-Type'] == 'application/json':
        return send_response("Only json request is supported", 400)

    if env_attr:
        return send_response("The environment is already configured. "
                             "Kindly use the /api/environment to modify the configurations", 400)
    req_data = request.json
    env_attr.update(req_data)
    return send_response("OK", 200)


@Environment.route('', methods=['PATCH'])
def modify_environment():
    if not request.headers['Content-Type'] == 'application/json':
        return send_response("Only json request is supported", 400)
    if not env_attr:
        return send_response("There is no environment configured to modified", 400)
    req_data = request.json
    env_attr.update(req_data)
    update_rover_status()
    return send_response("OK", 200)


from utils.rover_util import update_rover_status
