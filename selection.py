def left_upper_corner(creature):
    return creature.state['position'][0] < 100 and creature.state['position'][1] < 100

def middle(creature):
    x_middle = creature.config['world_parameters']['size'] / 2
    y_middle = creature.config['world_parameters']['size'] / 2
    return x_middle - 10 < creature.state['position'][0] < x_middle + 10 and \
        y_middle - 10 < creature.state['position'][1] < y_middle + 10


def is_selected(name, creature):
    return globals()[name](creature)