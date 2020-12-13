from constants import direction, max_battery_value, ope, priority
from routes.rover import rover_data, rover_state
from routes.environment import env_attr


def valid_move(input_direction, row, column, area_map):
    if (input_direction in direction[0:2] and ((row == (len(area_map)-1)) or row == 0)) or \
            (input_direction in direction[2:] and ((column == (len(area_map[row])-1)) or column == 0)):
        return {}
    if input_direction == direction[0]:
        row -= 1
    elif input_direction == direction[1]:
        row += 1
    elif input_direction == direction[2]:
        column -= 1
    elif input_direction == direction[3]:
        column += 1
    return {
        'row': row,
        'column': column
    }


def update_rover_status():
    if rover_data:
        if env_attr['solar-flare']:
            rover_data['initial-battery'] = max_battery_value
        if env_attr['storm']:
            for i, v in enumerate(rover_data['inventory']):
                if v['type'] == 'storm-shield':
                    if v['quantity'] == 1:
                        rover_data['inventory'].pop(i)
                    elif v['quantity'] > 1:
                        v['quantity'] -= 1
                    return True
            rover_state['life'] = 'dead'


def check_mobility(current_battery, battery_values=None):
    if battery_values:
        if ope[battery_values['conditions'][0]['operator']](current_battery, battery_values['conditions'][0]['value']):
            rover_state['mobility'] = 'immobile'


def update_inventory():
    value_name = None
    value_priority = None
    if env_attr['area-map'][rover_data['deploy-point']['row']][rover_data['deploy-point']['column']] == 'water':
        value_name = 'encountering-water'
        value_priority = priority['water_priority']
    elif env_attr['area-map'][rover_data['deploy-point']['row']][rover_data['deploy-point']['column']] == 'rock':
        value_name = 'encountering-rock'
        value_priority = priority['rock_priority']
    if value_name and value_priority:
        for ind, value in enumerate(rover_data['scenarios']):
            if value['name'] == value_name:
                inventory = rover_data['scenarios'][ind]['rover'][0]['performs']['collect-sample']
                inventory.update({"priority": value_priority})
                if not rover_data['inventory'] or rover_data['inventory'][0]['priority'] < inventory['priority']:
                    rover_data['inventory'] = inventory
