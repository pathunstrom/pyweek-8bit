def stat(monster, target):
    if target == 'power':
        return power(monster)

    if target == 'defense':
        return defense(monster)

    if target == 'health':
        return health(monster)


def power(monster):
    return 20


def defense(monster):
    return 20


def health(monster):
    return 20