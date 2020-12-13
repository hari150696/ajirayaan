from flask import Blueprint, request
from constants import direction
from routes.environment import env_attr
from utils.response import send_response


Rover = Blueprint('rover', __name__, url_prefix="/api/rover")
rover_data = {}
rover_state = {
    "life": "active",
    "mobile": "normal"
}


@Rover.route('/configure', methods=['POST'])
def add_rover():
    if rover_state['life'] == 'active':
        if not request.headers['Content-Type'] == 'application/json':
            return send_response("Only json request is supported", 400)
        if not rover_data:
            req_data = request.json
            rover_data.update(req_data)
            return send_response("OK", 200)
        return send_response("The rover is already configured.", 400)
    else:
        return send_response("", 204)


@Rover.route('/move', methods=['POST'])
def move_rover():
    if not rover_data:
        return send_response("There is no rover configured", 400)
    from utils.rover_util import check_mobility, valid_move, update_inventory
    battery_values = None
    for ind, val in enumerate(rover_data['scenarios']):
        if val['name'] == 'battery-low':
            battery_values = rover_data['scenarios'][ind]
    check_mobility(rover_data['initial-battery'], battery_values)
    if rover_state['life'] == 'active' and rover_state["mobile"] == 'immobile':
        return send_response("The rover is immobile. It cannot move in this state", 428)
    elif rover_state['life'] == 'active' and rover_state["mobile"] == 'normal':
        if not request.json['direction'] or request.json['direction'] not in direction:
            return send_response("Request you to give proper directions", 400)
        if env_attr['storm']:
            return send_response("Cannot move during a storm", 428)
        input_direction = request.json['direction']
        if rover_data['initial-battery'] != 0:
            value = valid_move(input_direction, rover_data['deploy-point']['row'], rover_data['deploy-point']['column'],
                               env_attr['area-map'])
            if not value:
                return send_response("Can move only within mapped area", 428)
            rover_data['deploy-point']['row'] = value['row']
            rover_data['deploy-point']['column'] = value['column']
            steps = 0
            update_inventory()
            steps += 1
            rover_data['initial-battery'] = rover_data['initial-battery'] + 10 if steps % 10 == 0 else \
                rover_data['initial-battery'] - 1
        return send_response("OK", 200)
    else:
        return send_response("", 204)


@Rover.route('/status')
def get_rover_status():
    if rover_state['life'] == 'active':
        rover_status = {'rover': {
            'location': {
                'row': rover_data['deploy-point']['row'],
                'column': rover_data['deploy-point']['column']
            },
            'battery': rover_data['initial-battery'],
            'inventory': rover_data['inventory']
        }, 'environment': {
            'temperature': env_attr['temperature'],
            'humidity': env_attr['humidity'],
            'solar-flare': env_attr['solar-flare'],
            'storm': env_attr['storm'],
            'terrain': env_attr['area-map'][rover_data['deploy-point']['row']][rover_data['deploy-point']['column']]
        }}
        return rover_status, 200
    else:
        return send_response("", 204)
