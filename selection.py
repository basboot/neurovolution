def left_upper_corner(creature):
    return creature.state['position'][0] < 100 and creature.state['position'][1] < 100, 1

def middle(creature):
    x_middle = creature.config['world_parameters']['size'] / 2
    y_middle = creature.config['world_parameters']['size'] / 2
    return x_middle - 10 < creature.state['position'][0] < x_middle + 10 and \
        y_middle - 10 < creature.state['position'][1] < y_middle + 10, 1

def at_breeding_ground(creature):
    y_border = creature.config['world_parameters']['size'] / 4 * 3
    return creature.state['position'][1] > y_border, creature.state['position'][1] * creature.state['position'][1]


def is_selected(name, creature):
    return globals()[name](creature)[0]

def get_selection_weight(name, creature):
    return globals()[name](creature)[1]