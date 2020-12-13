import operator
direction = ['up', 'down', 'left', 'right']
max_battery_value = 11

priority = {
       "storm-priority": 1,
       "water_priority": 2,
       "rock_priority": 3
}
ope = {"lte": operator.ge,
       "gte": operator.ge,
       "eq": operator.eq,
       "lt": operator.lt,
       "gt": operator.gt,
       "ne": operator.ne}
