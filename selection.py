def left_upper_corner(creature):
    return creature.state['position'][0] < 100 and creature.state['position'][1] < 100


def is_selected(name, creature):
    return globals()[name](creature)